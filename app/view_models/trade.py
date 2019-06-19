from app.view_models.book import BookViewModel


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


# todo 改写 MyTradesViewModel
class MyTrades:
    def __init__(self, my_trades, my_trade_count):
        self.my_trades = my_trades
        self.my_trade_count = my_trade_count
        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.my_trades:
            count = self.my_trade_count.get(trade.isbn, 0)
            r = {
                'id': trade.id,
                'count': count,
                'book': BookViewModel(trade.book)
            }
            temp_trades.append(r)

        return temp_trades

