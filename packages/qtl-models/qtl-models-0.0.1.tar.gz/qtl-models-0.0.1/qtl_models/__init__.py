from datetime import datetime
from dataclasses import dataclass, field

from mashumaro import DataClassMessagePackMixin

from .enums import Exchange, OrderType, Direction, Offset, OrderStatus, ProductClass


ACTIVE_ORDER_STATUSES = {
    OrderStatus.SUBMITTING,
    OrderStatus.NOTTRADED,
    OrderStatus.PARTTRADED
}


def datetime_field():
    return field(metadata={
        'serialize': lambda v: datetime.timestamp(v),
        'deserialize': lambda v: datetime.fromtimestamp(v),
    })


@dataclass
class Base(DataClassMessagePackMixin):
    pass


@dataclass
class Tick(Base):
    instrument_id: str
    exchange: Exchange
    volume: float
    turnover: float
    open_interest: float
    last_price: float
    limit_up: float
    limit_down: float
    open_price: float
    high_price: float
    low_price: float
    pre_close: float

    bid_price_1: float
    bid_volume_1: float
    ask_price_1: float
    ask_volume_1: float

    bid_price_2: float = None
    bid_price_3: float = None
    bid_price_4: float = None
    bid_price_5: float = None

    ask_price_2: float = None
    ask_price_3: float = None
    ask_price_4: float = None
    ask_price_5: float = None

    bid_volume_2: float = None
    bid_volume_3: float = None
    bid_volume_4: float = None
    bid_volume_5: float = None

    ask_volume_2: float = None
    ask_volume_3: float = None
    ask_volume_4: float = None
    ask_volume_5: float = None

    ts: datetime = datetime_field()

    def __post_init__(self):
        self.symbol = f'{self.exchange.value}.{self.instrument_id}'


@dataclass
class Bar(Base):
    instrument_id: str
    exchange: Exchange
    interval: str
    volume: float
    turnover: float
    open_interest: float
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    ts: datetime = datetime_field()

    def __post_init__(self):
        self.symbol = f'{self.exchange.value}.{self.instrument_id}'


@dataclass
class Order(Base):
    id: str
    instrument_id: str
    exchange: Exchange
    type: OrderType
    direction: Direction
    offset: Offset
    status: OrderStatus
    price: float
    volume: float
    traded: float
    reference: str
    ts: datetime = datetime_field()

    def __post_init__(self):
        self.symbol = f'{self.exchange.value}.{self.instrument_id}'


@dataclass
class Trade(Base):
    id: str
    order_id: str
    instrument_id: str
    exchange: Exchange
    direction: Direction
    offset: Offset
    price: float
    volume: float
    ts: datetime = datetime_field()

    def __post_init__(self):
        self.symbol = f'{self.exchange.value}.{self.instrument_id}'


@dataclass
class Position(Base):
    instrument_id: str
    exchange: Exchange
    direction: Direction
    volume: float
    frozen: float
    price: float
    pnl: float
    yd_volume: float

    def __post_init__(self):
        self.id = f'{self.instrument_id}.{self.direction.value}'
        self.symbol = f'{self.exchange.value}.{self.instrument_id}'


@dataclass
class Account(Base):
    id: str

    balance: float
    frozen: float
    available: float


@dataclass
class Instrument(Base):
    id: str
    exchange: Exchange
    name: str
    product_class: ProductClass
    volume_multiple: float
    price_tick: float

    def __post_init__(self):
        self.symbol = f'{self.exchange.value}.{self.id}'


@dataclass
class SubscribeRequest(Base):
    instrument_id: str
    exchange: Exchange

    def __post_init__(self):
        self.symbol = f'{self.exchange.value}.{self.instrument_id}'


@dataclass
class OrderRequest(Base):
    instrument_id: str
    exchange: Exchange
    direction: Direction
    order_type: OrderType
    offset: Offset
    volume: float
    price: float
    reference: str

    def __post_init__(self):
        self.symbol = f'{self.exchange.value}.{self.instrument_id}'


@dataclass
class CancelRequest(Base):
    order_id: str
    instrument_id: str
    exchange: Exchange

    def __post_init__(self):
        self.symbol = f'{self.exchange.value}.{self.instrument_id}'
