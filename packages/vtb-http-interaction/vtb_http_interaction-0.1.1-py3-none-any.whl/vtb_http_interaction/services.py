# pylint: disable=too-few-public-methods
import logging
import warnings
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Tuple, Dict, Optional

from aiohttp import ClientSession, ContentTypeError
from aiohttp.web_exceptions import HTTPUnauthorized
from jose import exceptions

from vtb_http_interaction.errors import MaxRetryError
from vtb_http_interaction.keycloak_gateway import KeycloakConfig
from vtb_http_interaction.process_authorization_header import ProcessAuthorizationHeader
from vtb_py_logging.request_id import get_context_request_id


class OnErrorResult(Enum):
    """
    SILENT - проигнорировать ошибку
    THROW - возбудить ошибку
    REFRESH - при ошибке выполнить действие повторно
    """
    SILENT = 1
    THROW = 2
    REFRESH = 3


class BaseService(ABC):
    """
    Abstract service
    """

    def __init__(self, max_retry: Optional[int] = 5):
        self.logger = logging.getLogger(__name__)
        self.current_step = 0
        self.max_retry = max_retry

    @abstractmethod
    async def _send(self, *args, **kwargs) -> Any:
        """
        Abstract _send
        """
        raise NotImplementedError("Not implemented _send method")

    async def send_request(self, *args, **kwargs) -> Any:
        """
        Вызов внешнего сервиса
        """

        try:
            args, kwargs = await self._before_send(*args, **kwargs)
            self.logger.debug("Send request %s: %s; %s", self.current_step, args, kwargs)
            response = await self._send(*args, **kwargs)
            self.logger.debug("Response %s: %s", self.current_step, response)

            return response
        except Exception as ex:
            on_error_result = await self._on_error(ex, *args, **kwargs)

            if on_error_result == OnErrorResult.THROW:
                self._raise_exception(ex)
            if on_error_result == OnErrorResult.SILENT:
                self.logger.exception(ex)
                return None
            if on_error_result == OnErrorResult.REFRESH:
                return await self._resend_request(ex, *args, **kwargs)

            raise NotImplementedError(f"on_error_result \"{on_error_result}\" not implemented") from ex

    def _raise_exception(self, ex: Exception) -> None:
        self.logger.exception(ex)
        raise ex

    async def _before_send(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """
        Действие перед вызовом
        """
        return args, kwargs

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:  # pylint: disable=unused-argument
        """
        Действие на возникновение ошибки.
        SILENT - продолжить работу без возникновения ошибки
        THROW - выкинуть исключение дальше
        REFRESH - сделать повторный вызов сервиса
        """
        return OnErrorResult.THROW

    async def _resend_request(self, ex: Exception, *args, **kwargs) -> Any:
        """ Повторная отправка запроса """
        self.current_step += 1

        self.logger.debug('Repeat request #%s.', self.current_step)

        if self.current_step >= self.max_retry:
            raise MaxRetryError(f'Exceeded the maximum number of attempts {self.max_retry}') from ex

        return await self.send_request(*args, **kwargs)


class HttpService(BaseService):
    """
    Вызов по протоколу http
    """

    async def _send(self, *args, **kwargs) -> Any:
        method = kwargs.get('method', 'get')

        url = kwargs.get('url', None)
        if url is None:
            raise ValueError("Url is none")
        url = str(url)

        cfg = kwargs.get('cfg', {})
        assert isinstance(cfg, dict)

        if url.lower().startswith('https://') and 'ssl' not in cfg:
            cfg['ssl'] = False

        async with ClientSession() as session:
            async with session.request(method, url, **cfg) as response:
                status = response.status
                if status == 401:
                    response_content = response.text()
                    self.logger.info("Unauthorized response %s: %s", self.current_step, response_content)
                    raise HTTPUnauthorized()

                # ContentTypeError
                try:
                    response_data = await response.json()
                except ContentTypeError:
                    response_data = await response.text()

                return status, response_data


class RestService(HttpService):
    """
    Вызов rest сервисов
    """

    def __init__(self, url: str, item_url_postfix: Optional[str] = '', max_retry: Optional[int] = 5):
        super().__init__(max_retry=max_retry)
        if url is None:
            raise ValueError("url is none.")

        self.url = url
        self.item_url_postfix = item_url_postfix

    async def post(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP POST request.
        """
        kwargs['method'] = "POST"
        kwargs['url'] = self.url

        return await self.send_request(*args, **kwargs)

    async def get(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP GET request.
        """

        kwargs['method'] = "GET"
        kwargs['url'] = self._prepare_item_url(kwargs['item_id']) if 'item_id' in kwargs else self.url

        return await self.send_request(*args, **kwargs)

    async def put(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP PUT request.
        """

        kwargs['method'] = "PUT"
        kwargs['url'] = self._prepare_item_url(kwargs.get('item_id', None))

        return await self.send_request(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP DELETE request.
        """

        kwargs['method'] = "DELETE"
        kwargs['url'] = self._prepare_item_url(kwargs.get('item_id', None))

        return await self.send_request(*args, **kwargs)

    def _prepare_item_url(self, item_id: str) -> str:
        if item_id is None:
            raise ValueError('Request must contain an id.')

        item_id = str(item_id)

        if item_id.startswith('/'):
            item_id = item_id[1:]

        url = self.url
        if url.endswith('/'):
            url = url[:-1]

        return f"{url}/{item_id}{self.item_url_postfix}"


# noinspection PyClassHasNoInit
class PrepareHeaderMixin:
    async def prepare_header(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        return args, kwargs

    async def _before_send(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        return await self.prepare_header(*args, **kwargs)


# noinspection PyClassHasNoInit
class RequestIdHeaderMixin(PrepareHeaderMixin):
    async def prepare_header(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        request_id = get_context_request_id()
        if request_id:
            headers = kwargs.setdefault("cfg", {}).setdefault("headers", {})
            headers["X-Request-Id"] = request_id
        args, kwargs = await super().prepare_header(*args, **kwargs)
        return args, kwargs


class HttpServiceWithRequestId(RequestIdHeaderMixin, HttpService):
    pass


class RestServiceWithRequestId(RequestIdHeaderMixin, RestService):
    pass


# noinspection PyClassHasNoInit
class AuthorizationPrepareHeaderMixin(PrepareHeaderMixin):
    """Обработка заголовка Authorization"""
    process_authorization_header = None

    async def prepare_header(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """ Действие перед вызовом """
        args, kwargs = await super().prepare_header(*args, **kwargs)
        kwargs = await self.process_authorization_header.prepare_header(**kwargs)

        return args, kwargs

    async def obtain_token(self, ex: Exception, **kwargs) -> OnErrorResult:
        """
        Действие на возникновение ошибки ExpiredSignatureError (access_token просрочен)
        В случае обновления токена возвращаем OnErrorResult.REFRESH для повторного вызова сервиса с новым заголовком
        На все остальные ошибки вернуть OnErrorResult.THROW
        """
        if isinstance(ex, exceptions.ExpiredSignatureError):
            # Повторные вызовы (а значит обновление access_token) запрещены, либо нет refresh_token
            if not self.max_retry or not self.process_authorization_header.refresh_token:
                self._raise_exception(HTTPUnauthorized())

            # Есть refresh_token и можно попытаться обновить access_token
            await self.process_authorization_header.obtain_token(**kwargs)
            return OnErrorResult.REFRESH

        return OnErrorResult.THROW


# Группа сервисов, реализующих логику получения токена из keycloak и сохранения его в редис
class AuthorizationHttpService(RequestIdHeaderMixin, AuthorizationPrepareHeaderMixin, HttpService):
    """ Вызов http сервисов под УЗ пользователя Keycloak """

    def __init__(self,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: Optional[str] = None,
                 token_cache=None,
                 max_retry: Optional[int] = 5):
        super().__init__(max_retry=max_retry)
        self.process_authorization_header = ProcessAuthorizationHeader(keycloak_config,
                                                                       redis_connection_string=redis_connection_string,
                                                                       token_cache=token_cache)

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:
        return await self.obtain_token(ex, **kwargs)


class AuthorizationService(RequestIdHeaderMixin, AuthorizationPrepareHeaderMixin, RestService):
    """ Вызов rest сервисов под УЗ пользователя Keycloak """

    def __init__(self,
                 url: str,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: Optional[str] = None,
                 token_cache=None,
                 item_url_postfix: Optional[str] = '',
                 max_retry: Optional[int] = 5):
        # TODO: Удалить класс в версии 1.0.0
        warnings.warn(
            "class AuthorizationService is deprecated, use AuthorizationRestService instead. "
            "The class will be removed in version 1.0.0.",
            DeprecationWarning, stacklevel=2
        )
        super().__init__(url, item_url_postfix, max_retry=max_retry)
        self.process_authorization_header = ProcessAuthorizationHeader(keycloak_config,
                                                                       redis_connection_string=redis_connection_string,
                                                                       token_cache=token_cache)

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:
        return await self.obtain_token(ex, **kwargs)


AuthorizationRestService = AuthorizationService
