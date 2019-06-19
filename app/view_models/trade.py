
class TradeInfo:
    def __init__(self, trades):
        self.total = len(trades)
        self.trades = self._parse(trades)

    def _parse(self, trades):
        return [self._map_to_trade(trade) for trade in trades]

    def _map_to_trade(self, single):
        return dict(
            user_name=single.user.nickname,
            time=single.create_datetime.strftime('%Y-%m-%d'),
            id=single.id
        )
