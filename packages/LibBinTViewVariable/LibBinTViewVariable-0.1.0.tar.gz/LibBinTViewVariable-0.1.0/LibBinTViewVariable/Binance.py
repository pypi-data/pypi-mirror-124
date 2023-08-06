from enum import Enum, unique


@unique
class FUTURE_ORDER_TYPES(Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP = 'STOP'
    STOP_MARKET = 'STOP_MARKET'
    TAKE_PROFIT = 'TAKE_PROFIT'
    TAKE_PROFIT_MARKET = 'TAKE_PROFIT_MARKET'
    LIMIT_MAKER = 'LIMIT_MAKER'


@unique
class ORDER_STATUS(Enum):
    NEW = 'NEW'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    FILLED = 'FILLED'
    CANCELED = 'CANCELED'
    PENDING_CANCEL = 'PENDING_CANCEL'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'


@unique
class ORDER_TYPES(Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP_LOSS = 'STOP_LOSS'
    STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    TAKE_PROFIT = 'TAKE_PROFIT'
    TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    LIMIT_MAKER = 'LIMIT_MAKER'


@unique
class SIDE(Enum):
    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'


@unique
class TIME_IN_FORCE(Enum):
    GTC = 'GTC'  # Good till cancelled
    IOC = 'IOC'  # Immediate or cancel
    FOK = 'FOK'  # Fill or kill
