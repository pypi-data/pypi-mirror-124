import typing as t
from httpx import Response
from dao.errors import ServiceError
from dataclasses import dataclass


@dataclass
class Result:

    _res: Response

    @property
    def raw(self):
        return self._res.content

    @property
    def result(self):
        if self.err:
            raise ServiceError(self.err)
        return self._res.json()

    @property
    def err(self):
        return int(self._res.json()["errorCode"])

    def __getitem__(self, key):
        return self.result.get(key)

    def eject(self) -> Response:
        return self._res


class ServiceMixin:
    def __getitem__(self):
        ...


class PicTrans(Result):
    @property
    def img_b64(self):
        return self.result.get("render_image")


class _TransResult(Result, ServiceMixin):

    __slots__ = (
        "basic",
        "web",
        "translation",
        "lang",
        "webdict",
        "speak_url",
        "t_speak_url",
        "ret_phrase",
    )
