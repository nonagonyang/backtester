import backtrader
from datetime import date, datetime, time, timedelta
from constants import logs

# Create a Stratey

class BuySlightDipStrategy(backtrader.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        logs.append('%s, %s' % (dt.isoformat(), txt))
        # print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order=None
    
    def notify_order(self,order):
        if order.status in [order.Submitted, order.Accepted]:
            return 
        if order.status in[order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED{}".format(order.executed.price))

            elif order.issell():
                self.log("SELL EXECUTED{}".format(order.executed.price))
            self.bar_executed = len(self)
        self.order=None

# Buying buying slight dips

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order=self.buy()
        else:
            if(len(self))>=(self.bar_executed +5):
                self.log("SELL CREATED {}".format(self.dataclose[0]))
                self.order=self.sell()




#opening range breakout
class OpeningRangeBreakout(backtrader.Strategy):
    params = dict(
        num_opening_bars=15
    )

    def __init__(self):
        self.opening_range_low = 0
        self.opening_range_high = 0
        self.opening_range = 0
        self.bought_today = False
        self.order = None
    
    def log(self, txt, dt=None):
        # if dt is None:
        #     dt = self.datas[0].datetime.datetime()
        # logs.append('%s, %s' % (dt.isoformat(), txt))
        # print('%s, %s' % (dt, txt))
        dt = dt or self.datas[0].datetime.date(0)
        logs.append('%s, %s' % (dt.isoformat(), txt))
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        if order.status in [order.Completed]:
            order_details = f"{order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}"

            if order.isbuy():
                self.log(f"BUY EXECUTED, Price: {order_details}")
            else:  # Sell
                self.log(f"SELL EXECUTED, Price: {order_details}")
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        current_bar_datetime = self.data.num2date(self.data.datetime[0])
        previous_bar_datetime = self.data.num2date(self.data.datetime[-1])

        if current_bar_datetime.date() != previous_bar_datetime.date():
            self.opening_range_low = self.data.low[0]
            self.opening_range_high = self.data.high[0]
            self.bought_today = False
        
        opening_range_start_time = time(9, 30, 0)
        dt = datetime.combine(date.today(), opening_range_start_time) + timedelta(minutes=self.p.num_opening_bars)
        opening_range_end_time = dt.time()

        if current_bar_datetime.time() >= opening_range_start_time \
            and current_bar_datetime.time() < opening_range_end_time:           
            self.opening_range_high = max(self.data.high[0], self.opening_range_high)
            self.opening_range_low = min(self.data.low[0], self.opening_range_low)
            self.opening_range = self.opening_range_high - self.opening_range_low
        else:
            if self.order:
                return
            
            if self.position and (self.data.close[0] > (self.opening_range_high + self.opening_range)):
                self.close()
                
            if self.data.close[0] > self.opening_range_high and not self.position and not self.bought_today:
                self.order = self.buy()
                self.bought_today = True

            if self.position and (self.data.close[0] < (self.opening_range_high - self.opening_range)):
                self.order = self.close()

            if self.position and current_bar_datetime.time() >= time(15, 45, 0):
                self.log("RUNNING OUT OF TIME - LIQUIDATING POSITION")
                self.close()

    def stop(self):
        self.log('(Num Opening Bars %2d) Ending Value %.2f' %
                 (self.params.num_opening_bars, self.broker.getvalue()))

        if self.broker.getvalue() > 130000:
            self.log("*** BIG WINNER ***")

        if self.broker.getvalue() < 70000:
            self.log("*** MAJOR LOSER ***") 







#based on simple moving average
class SmaStrategy(backtrader.Strategy):
    params = (('ma_period', 20), )

    def __init__(self):
        self.data_close = self.datas[0].close

        self.order = None
        self.price = None
        self.comm = None

        self.sma = backtrader.ind.SMA(self.datas[0],
                              period=self.params.ma_period)

        
    def log(self, txt,dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logs.append('%s, %s' % (dt.isoformat(), txt))
        # print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED --- Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Commission: {order.executed.comm:.2f}')
                self.price = order.executed.price
                self.comm = order.executed.comm
            else:
                self.log(f'SELL EXECUTED --- Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Commission: {order.executed.comm:.2f}')

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin,
                              order.Rejected]:
            self.log('Order Failed')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log(f'OPERATION RESULT --- Gross: {trade.pnl:.2f}, Net: {trade.pnlcomm:.2f}')

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.data_close[0] > self.sma[0]:
                self.log(f'BUY CREATED --- Price: {self.data_close[0]:.2f}')
                self.order = self.buy()
        else:
            if self.data_close[0] < self.sma[0]: 
                self.log(f'SELL CREATED --- Price: {self.data_close[0]:.2f}')
                self.order = self.sell()


