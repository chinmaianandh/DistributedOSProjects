from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TradeAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRADE_BUY: _ClassVar[TradeAction]
    TRADE_SELL: _ClassVar[TradeAction]
TRADE_BUY: TradeAction
TRADE_SELL: TradeAction

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

class TradeRequest(_message.Message):
    __slots__ = ("stock_name", "num_of_items", "trade_type")
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_OF_ITEMS_FIELD_NUMBER: _ClassVar[int]
    TRADE_TYPE_FIELD_NUMBER: _ClassVar[int]
    stock_name: str
    num_of_items: int
    trade_type: TradeAction
    def __init__(self, stock_name: _Optional[str] = ..., num_of_items: _Optional[int] = ..., trade_type: _Optional[_Union[TradeAction, str]] = ...) -> None: ...

class TradeResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("stock_name", "price")
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    stock_name: str
    price: float
    def __init__(self, stock_name: _Optional[str] = ..., price: _Optional[float] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
