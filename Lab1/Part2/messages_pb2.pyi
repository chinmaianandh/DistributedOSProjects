from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LookupRequest(_message.Message):
    __slots__ = ("stock_name",)
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    stock_name: str
    def __init__(self, stock_name: _Optional[str] = ...) -> None: ...

class LookupResponse(_message.Message):
    __slots__ = ("status_code", "price", "volume")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    price: float
    volume: int
    def __init__(self, status_code: _Optional[int] = ..., price: _Optional[float] = ..., volume: _Optional[int] = ...) -> None: ...
