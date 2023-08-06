
from datetime import datetime
from typing import Union, List
from pydantic import BaseModel

from .trades import Transaction
from .report import TradeReport


class Lote(BaseModel):
    status: str
    origin_market: Union[str, None]
    origin_exchange: Union[str, None]
    target_market: str
    target_exchange: str
    total_amount: float
    collected: float
    filled: float
    remaining: float
    order_type: str
    time: float
    date: datetime
    currency: str
    order_ids: List[str]
    trade_ids: List[str]
    transaction_ids: List[str]

    def update_position(self, new_transaction: Transaction):
        if new_transaction.id not in self.transaction_ids:
            self.collected += new_transaction.currency_value
            self.filled += new_transaction.pair_currency_value
            self.remaining = self.total_amount - self.filled
            self.transaction_ids.append(new_transaction.id)

    def update_trade(self, new_trade: TradeReport):
        if new_trade.trade_id not in self.trade_ids:
            self.trade_ids.append(new_trade.trade_id)

    def is_full(self):
        return (self.total_amount - self.filled) / self.total_amount >= 0.8

    @classmethod
    def new_lote(cls, origin_market: str, origin_exchange: str, target_market: str, target_exchange: str, currency: str, total_amount: float, order_type: str):
        return cls(
            origin_exchange=origin_exchange,
            origin_market=origin_market,
            target_market=target_market,
            target_exchange=target_exchange,
            currency=currency,
            total_amount=total_amount,
            order_type=order_type,
            filled=0.0,
            remaining=total_amount,
            collected=0.0,
            order_ids=[],
            trade_ids=[],
            transaction_ids=[])

    def __str__(self):
        out = "\n"
        out += f"\t Lote for Origin: {self.origin_market} - Target {self.target_market} Markets Updated:\n"
        out += f"\t\t**Total Amount**: {self.total_amount}\n"
        out += f"\t\t**Filled**: {self.filled}\n"
        out += f"\t\t**Remaning**: {self.remaining}\n"
        out += f"\t\t**Status**: {self.status}\n"
        return out
