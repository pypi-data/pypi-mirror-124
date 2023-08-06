"""
Реализация классов, отвечающих за алгоритмы получения и сохранения токенов аутентификации
"""
from typing import Tuple, Any, Dict, Union, Optional

import aioredis

from vtb_http_interaction.http_utils import parse_authorization_header
from vtb_http_interaction.keycloak_gateway import KeycloakGateway, KeycloakConfig


class MemoryCache:
    memory_cache = {}

    async def set_value(self, cache_key: str, access_token: str, refresh_token: str) -> None:
        """ Установка значения токена """
        cache_value = {'access_token': access_token, 'refresh_token': refresh_token}
        if cache_key in self.memory_cache:
            self.memory_cache.pop(cache_key)

        self.memory_cache[cache_key] = cache_value

    async def get_value(self, cache_key: str) -> Tuple[Union[None, str], Union[None, str]]:
        """ Получение значения токена """
        if cache_key in self.memory_cache:
            result = self.memory_cache[cache_key]
            return result.get('access_token', None), result.get('refresh_token', None)

        return None, None


class RedisCache:
    """
    Класс, реализующий хранение access_token и refresh_token в redis
    Необходимая реализация протокола: set_value, get_value
    Необязательная реализация протокола: init, dispose
    """

    def __init__(self, redis_connection_string: str):
        self.redis_connection_string = redis_connection_string
        self.redis_pool = None

    async def set_value(self, cache_key: str, access_token: str, refresh_token: str) -> None:
        """ Установка значения токена """
        cache_value = {'access_token': access_token, 'refresh_token': refresh_token}
        key_exist = await self.redis_pool.exists(cache_key)
        if key_exist:
            await self.redis_pool.delete(cache_key)

        await self.redis_pool.hmset_dict(cache_key, **cache_value)

    async def get_value(self, cache_key: str) -> Tuple[Union[None, str], Union[None, str]]:
        """ Получение значения токена """
        key_exist = await self.redis_pool.exists(cache_key)
        if key_exist:
            result = await self.redis_pool.hgetall(cache_key, encoding='utf-8')
            return result.get('access_token', None), result.get('refresh_token', None)

        return None, None

    async def init(self):
        """ Инициализация ресурсов """
        self.redis_pool = await aioredis.create_redis_pool(self.redis_connection_string)

    async def dispose(self):
        """ Освобождение ресурсов """
        self.redis_pool.close()
        await self.redis_pool.wait_closed()


class ProcessAuthorizationHeader:
    """
    Обработка заголовка Authorization
    """

    def __init__(self,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: Optional[str] = None,
                 token_cache=None):
        self.refresh_token = None
        self.keycloak_config = keycloak_config
        self.cache_key = f"{keycloak_config.realm_name}_{keycloak_config.client_id}"
        if token_cache:
            self.token_cache = token_cache
        elif redis_connection_string:
            self.token_cache = RedisCache(redis_connection_string)
        else:
            raise ValueError('One of the parameters is required: redis_connection_string, token_cache.')

    async def prepare_header(self, **kwargs) -> Dict[Any, Any]:
        """
        Обработка заголовка Authorization перед вызовом session.request
        Алгоритм:
        0. Получение токена выполнять только, если его нет в заголовке. Если токен есть, то проверяем его срок жизни.
        1. Получаем refresh_token и access_token из Redis. Если токен есть, то проверяем его срок жизни.
        2. Если их нет, то запрашиваем их на основе логина/пароля. Кладем их в Redis
        3. Формируем заголовок к запросу 'Authorization': "Bearer {access_token}"
        :param kwargs: параметры запроса
        :return: обработанные параметры запроса
        """
        if not _authorization_header_exist(**kwargs):
            await self._init()

            try:
                access_token, self.refresh_token = await self.token_cache.get_value(self.cache_key)

                if self.refresh_token is None or access_token is None:
                    with KeycloakGateway(self.keycloak_config) as gateway:
                        access_token, self.refresh_token = gateway.obtain_token()

                    await self.token_cache.set_value(self.cache_key, access_token, self.refresh_token)
                else:
                    await self._validate_token_lifespan(access_token)
            finally:
                await self._dispose()

            if 'cfg' not in kwargs:
                kwargs['cfg'] = {}

            if 'headers' not in kwargs['cfg']:
                kwargs['cfg']['headers'] = {}

            if 'Authorization' not in kwargs['cfg']['headers']:
                kwargs['cfg']['headers']['Authorization'] = f'Bearer {access_token}'
        else:
            access_token = _parse_authorization_header(kwargs['cfg']['headers']['Authorization'])
            await self._validate_token_lifespan(access_token)

        return kwargs

    async def obtain_token(self, **kwargs) -> Dict[Any, Any]:
        """
        Обновление access_token
        Алгоритм:
        1. Обновляем access_token на основе refresh_token
        2. Кладем новые access_token и refresh_token в Redis
        :param kwargs: параметры запроса
        :return: обработанные параметры запроса
        """
        if self.refresh_token is None:
            raise ValueError('refresh_token is none')

        with KeycloakGateway(self.keycloak_config) as gateway:
            access_token, self.refresh_token = gateway.obtain_new_token(self.refresh_token)

        await self._init()
        try:
            await self.token_cache.set_value(self.cache_key, access_token, self.refresh_token)

            if _authorization_header_exist(**kwargs):
                del kwargs['cfg']['headers']['Authorization']
        finally:
            await self._dispose()

        return kwargs

    async def _validate_token_lifespan(self, access_token: str) -> bool:
        with KeycloakGateway(self.keycloak_config) as gateway:
            gateway.decode_token(token=access_token, key=gateway.public_key)

        return True

    async def _init(self):
        try:
            await self.token_cache.init()
        except AttributeError:
            pass

    async def _dispose(self):
        try:
            await self.token_cache.dispose()
        except AttributeError:
            pass


def _parse_authorization_header(authorization_header: str) -> str:
    key, token = parse_authorization_header(authorization_header)

    if key.lower() != 'bearer':
        raise Exception(f'Invalid token header "{authorization_header}".')

    return token


# async def _get_token_from_cache(redis_pool: aioredis.Redis, cache_key: str) -> \
#         Tuple[Union[None, str], Union[None, str]]:
#     """
#     Получаем refresh_token и access_token из Redis
#     """
#     key_exist = await redis_pool.exists(cache_key)
#     if key_exist:
#         result = await redis_pool.hgetall(cache_key, encoding='utf-8')
#         return result.get('access_token', None), result.get('refresh_token', None)
#
#     return None, None
#
#
# async def _set_token_into_cache(redis_pool: aioredis.Redis, cache_key: str,
#                                 cache_value: Dict[str, str]) -> None:
#     """
#     Кладем refresh_token и access_token в Redis
#     """
#     key_exist = await redis_pool.exists(cache_key)
#     if key_exist:
#         await redis_pool.delete(cache_key)
#
#     await redis_pool.hmset_dict(cache_key, **cache_value)


def _authorization_header_exist(**kwargs):
    """ Проверка наличия заголовка Authorization в запросе """
    if 'cfg' not in kwargs or 'headers' not in kwargs['cfg']:
        return False

    authorization = kwargs['cfg']['headers'].get('Authorization', None)

    return authorization is not None and str(authorization).lower().startswith('bearer')
