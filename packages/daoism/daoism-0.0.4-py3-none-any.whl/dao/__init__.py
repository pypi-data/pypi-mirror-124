import typing as t
from dao.config import Config
from dao.models import Result
from dao.api import Api, ensure_key_secret

api = Api()

# Maybe add somethng like server._post(*args,**kwd), then youdao
# call every service's _post method.


class YouDao:
    def __init__(self, key: t.Text = None, secret: t.Text = None) -> None:
        key, secret = ensure_key_secret(key, secret)
        self.key = key
        self.secret = secret

    @api('trans')
    def translate(self, q, config: Config = None, **kwd) -> Result:
        # TODO pass a config then change config_map config
        # NOTE maybe we dont need that
        ...

    @api('ocr')
    def ocr_upload(self, img, config: Config = None, **kwd) -> Result:
        ...

    @api('receipt')
    def ocr_receipt(self, q, **kwd):
        ...

    @api("pictrans")
    def pic_translate(self, q, **kwd):
        ...

    @api('table')
    def ocrtable_upload(self, q, config: Config = None, **kwd):
        ...

    # def pdf(self, wait_until_done=False):
    #     ...
