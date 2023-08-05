"""
Утилитарный класс работы с HTTP
"""
import datetime
import decimal
import json
import uuid
from typing import Tuple

from vtb_http_interaction import errors


def parse_authorization_header(authorization_header: str) -> Tuple[str, str]:
    """
    Парсинг значения заголовка Authorization
    Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
    auth = authorization_header.split()

    len_auth = len(auth)

    if len_auth == 0:
        raise errors.InvalidToken('Invalid token header. No token provided.')

    if len_auth == 1:
        raise errors.InvalidToken('Invalid token header. No credentials provided.')

    if len_auth > 2:
        raise errors.InvalidToken('Invalid token header. Token string should not contain spaces.')

    return auth[0], auth[1]


def default_encoder(obj):
    """ Default JSON encoder """
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

    if isinstance(obj, (uuid.UUID, decimal.Decimal)):
        return str(obj)

    return obj


def dumps(*args, **kwargs):
    return json.dumps(*args, **kwargs, default=default_encoder)