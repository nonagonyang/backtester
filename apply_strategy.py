import backtrader
from alpaca_trade_api.rest import TimeFrame
import alpaca_trade_api as tradeapi
from config import API_KEY_ID,SECRET_KEY,BASE_URL
from constants import logs
from strategies import *

api=tradeapi.REST(API_KEY_ID,
                SECRET_KEY,
                BASE_URL)


# apply_strategy(cash_amount,stock_symbol,strategy_name,start_date,end_date):

def apply_strategy(cash_amount,stock_symbol,strategy_name,start_date,end_date):
    cerebro=backtrader.Cerebro()
    cerebro.broker.setcash(cash_amount)
    cerebro.addsizer(backtrader.sizers.PercentSizer, percents=95)
    # Create a Data Feed, download stock price historical data from alpaca API as panda dataframe
    if strategy_name=="OpeningRangeBreakout":
        dataframe= api.get_bars(stock_symbol, TimeFrame.Minute, start_date, end_date, adjustment='raw').df
    else:
        dataframe= api.get_bars(stock_symbol, TimeFrame.Day, start_date, end_date, adjustment='raw').df

    # dataframe= api.get_bars("AAPL", TimeFrame.Day, "2021-01-01", "2022-01-01", adjustment='raw').df
    # dataframe= api.get_bars("AAPL", TimeFrame.Minute, "2022-01-01", "2022-04-01", adjustment='raw').df


    # Add the Data Feed to Cerebro
    data = backtrader.feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)

    # Add strategy to Cerebro
    if strategy_name=="BuySlightDipStrategy":
        cerebro.addstrategy(BuySlightDipStrategy)
    if strategy_name=="OpeningRangeBreakout":
        cerebro.addstrategy(OpeningRangeBreakout)
    if strategy_name=="SmaStrategy":
        cerebro.addstrategy(SmaStrategy)
    if strategy_name=="VIXStrategy":
        cerebro.addstrategy(VIXStrategy)
    if strategy_name=="FearGreedStrategy":
        cerebro.addstrategy(FearGreedStrategy)
    if strategy_name=="PutCallStrategy":
        cerebro.addstrategy(PutCallStrategy)



    print("starting portfolio value %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    # runstrats=cerebro.run()
    print("ending portfolio value %.2f" % cerebro.broker.getvalue())
    return [cerebro.broker.getvalue(),logs]




