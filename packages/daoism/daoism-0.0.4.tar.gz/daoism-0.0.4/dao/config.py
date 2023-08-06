import typing as t


class Config:

    Q: t.Text
    API: t.Text
    CONFIG: t.Dict[str, str]

    def __init__(self, q: t.Text = None, api: t.Text = None, config: t.Dict = None):
        self.Q = q and q or self.Q
        self.API = api and api or self.API
        self.CONFIG = config and config or self.CONFIG

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)

    @classmethod
    def set(cls, q: t.Text = None, api: t.Text = None, config: t.Dict = None):
        self = cls()
        self.Q = q and q or cls.Q
        self.API = api and api or cls.API
        self.CONFIG = config and config or cls.CONFIG

        return self


class OCRConfig(Config):
    Q = "img"
    API = "https://openapi.youdao.com/ocrapi"
    CONFIG = {
        "detectType": "10012",
        "langType": "auto",
        "imageType": "1",
        "docType": "json",
    }


class TransConfig(Config):
    Q = "q"
    API = "https://openapi.youdao.com/api/"
    CONFIG = {"from": "auto", "to": "auto", "vocabId": ""}


class OCRTableConfig(Config):
    Q = "q"
    API = "https://openapi.youdao.com/ocr_table"
    CONFIG = {"docType": "excel", "type": "1"}


class OCRReceipt(Config):
    Q = 'q'
    API = "https://openapi.youdao.com/iocr"
    CONFIG = {
        "templateId": "73C0D6E0DDBD4050AA8CD2C1D29AB55D",
        "format": "img",
        "generalOcr": "false",
    }


class OCRPicTrans(Config):
    Q = 'q'
    API = "https://openapi.youdao.com/ocrtransapi"
    CONFIG = {"type": "1", "from": "auto", "to": "auto", "render": "1"}


class Pdf2WordConfig(Config):
    Q = "q"
    API = "https://openapi.youdao.com/file_convert/upload"
    CONFIG = {"docType": "json"}

    @classmethod
    def query_config(cls, flownum: t.Text) -> Config:
        self = cls()
        self.__dict__.pop("Q")
        self.API = "https://openapi.youdao.com/file_convert/query"
        return self

    @classmethod
    def download_config(cls, flownum: t.Text) -> Config:
        self = cls()
        self.__dict__.pop("Q")
        self.API = "https://openapi.youdao.com/file_convert/download"
        return self


config_map = {
    "trans": TransConfig,
    'ocr': OCRConfig,
    "pdf": Pdf2WordConfig,
    "table": OCRTableConfig,
    "receipt": OCRReceipt,
    "pictrans": OCRPicTrans,
}


class ConfigMapMixin:
    def __getitem__(self, k):
        try:
            val = self.__dict__[k]
        except KeyError:
            val = self.__class__.__dict__[k]
        return val


class ConfigMap(ConfigMapMixin):
    trans = TransConfig
    ocr = OCRConfig
    pdf = Pdf2WordConfig
    table = OCRTableConfig
    receipt = OCRReceipt
    pictrans = OCRPicTrans
