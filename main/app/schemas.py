from typing import Any

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict
import datetime


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ReceiptBase(BaseModel):
    receipt_num: str
    registration_num: str
    total: str
    created_at: datetime.datetime


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptDelete(ReceiptBase):
    id: int


class Receipt(ReceiptBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
