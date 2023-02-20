from datetime import datetime
import backtrader as bt
from dateutil.relativedelta import relativedelta


class TestStrategy(bt.Strategy):
    def __init__(self):
        self._next_buy_date = datetime(2010, 1, 5)

    def next(self):
        if self.data.datetime.date() >= self._next_buy_date.date():
            self._next_buy_date += relativedelta(months=1)
            self.buy(size=1)


cerebro = bt.Cerebro()
data = bt.feeds.YahooFinanceData(dataname='MSFT',
                                 fromdate=datetime(2010, 1, 1),
                                 todate=datetime(2018, 12, 31))

cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.broker.set_cash(cash=10000)
cerebro.run()
cerebro.plot() 