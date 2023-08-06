import os
import time
import uuid
import httpx
import hashlib
import typing as t
from dao.models import Result
from functools import cached_property
from dao.config import Config
from collections.abc import MutableMapping
from dao.errors import *

ParamField = t.Literal["url", "headers", "params"]


class P(MutableMapping):
    def __init__(
        self,
        _type: t.Literal['json', 'data'],
        url: t.Text,
        headers: t.Dict,
        params: t.Dict,
    ) -> None:
        self.__dict__[_type] = params
        self.url = url
        self.headers = headers

    def drop_data(self, name: str):
        ...

    def drop_field(self, field: ParamField):
        del self[field]

    def add(self):
        # add some new k-v stuff
        ...

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, k):
        return self.__dict__[k]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]


sign_keys = ("sign", "curtime", "salt", "signType", "appKey")


class Signer:
    @cached_property
    def time(self):
        return str(int(time.time()))

    @cached_property
    def salt(self):
        return str(uuid.uuid1())

    def __init__(self, key, secret) -> None:
        self.key = key
        self.secret = secret

    def _truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10 : size]

    def sign(self, q):
        time = self.time
        salt = self.salt
        signStr = f"{self.key}{self._truncate(q)}{salt}{time}{self.secret}"
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode("utf-8"))

        return {
            "sign": hash_algorithm.hexdigest(),
            'curtime': time,
            "salt": salt,
            "signType": "v3",
            "appKey": self.key,
        }


def get_p(
    s: Signer,
    q: t.Any,
    config: t.Type[Config],
    _type: t.Literal['data', 'json'] = 'data',
    **kwd,
):
    query = {config.Q: q}
    return P(
        _type=_type,
        url=config.API,
        params={**config.CONFIG, **s.sign(q), **query, **kwd},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def ensure_key_secret(key=None, secret=None):
    if not key or not secret:
        try:
            key = os.environ["YOUDAO_AI_KEY"]
            secret = os.environ["YOUDAO_AI_SECRET"]
        except KeyError as e:
            raise InitError(e, "To use YouDao Api you need APP_KEY and APP_SECRET ")
    return key, secret


class Api:
    def __init__(
        self, key: str = None, secret: str = None, config_map: t.Dict = None
    ) -> None:
        if config_map:
            self.config_map = config_map
        else:
            from dao.config import config_map as cfg_map

            self.config_map = cfg_map

    def __call__(self, name):
        _config = self.config_map[name]

        # NOTE The problem here is, only can get q from args

        def inner(func: t.Callable):
            def youdao_ins(youdao, *args, **kwd) -> Result:
                # key'n secret come from YouDao instance
                signer = Signer(key=youdao.key, secret=youdao.secret)
                param = get_p(s=signer, config=_config, q=args[0], **kwd)
                res = httpx.post(**param)
                return Result(res)

            def func_ins(*args, **kwd) -> Result:
                key, secret = ensure_key_secret()
                signer = Signer(key=key, secret=secret)
                param = get_p(s=signer, config=_config, q=args[0], **kwd)
                res = httpx.post(**param)
                return Result(res)

            if not "YouDao" in func.__qualname__.split("."):
                return func_ins

            return youdao_ins

        return inner
