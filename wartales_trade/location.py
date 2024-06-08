from dataclasses import dataclass
from wartales_trade.trade_good import TradeGood


@dataclass
class Location:
    name: str
    trade_goods: list[TradeGood]
    buying: list[tuple[TradeGood, int]]

    def add_good(self, trade_good: TradeGood) -> None:
        self.trade_goods.append(trade_good)

    def get_price_for_trade_good(self, trade_good: TradeGood) -> int | None:
        for tg, price in self.buying:
            if tg == trade_good:
                return price
        return None
