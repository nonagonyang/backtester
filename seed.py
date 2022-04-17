
from models import db, Stock,StockPrice,Strategy,Test,User
from app import app
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import config
from constants import *


db.drop_all()
db.create_all()

Stock.query.delete()
StockPrice.query.delete()
Test.query.delete()
User.query.delete()


#populate the stocks table in database by using alpaca api
#only include those in QQQ (NASDAQ 100) due to personal interest and running time consideration 
api=tradeapi.REST(config.API_KEY_ID,
                config.SECRET_KEY,
                base_url=config.BASE_URL)
active_assets = api.list_assets(status='active')
nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']

for asset in nasdaq_assets:
    try:
        if asset.tradable and asset.symbol in qqq_symbols :
            stock=Stock(symbol=asset.symbol, name=asset.name, exchange=asset.exchange)
            db.session.add(stock)
    except: 
        pass
db.session.commit()


stocks=Stock.query.all()
stock_dict={}
for stock in stocks:
    stock_dict[stock.symbol]=stock.id



#populate the stockprices table in database by using alpaca api

#if we need to populate more than 10000 stocks, loop through the stocks in chunk sizes at a time 
    # chunk_size=200
    # for i in range(0,len(symbollist),chunk_size):
    #     symbol_chunk=symbollist[i:i+chunk_size]
    #due to the limitation of my alpaca account, I cannot get the current day's first 15 minutes data.

for symbol in qqq_symbols: 
    day_bars=api.get_bars(symbol,TimeFrame.Day,"2022-04-01",yesterday,adjustment='raw').df  
    
    for index, row in day_bars.iterrows():
        try:
            stockprice=StockPrice(stock_id=stock_dict[symbol],
                                date=index.tz_localize(None).isoformat(),
                                open=row["open"],
                                high=row["high"],
                                low=row["low"],
                                close=row["close"],
                                volume=row["volume"]
                                )
            
            db.session.add(stockprice)
        except:
            pass
            
db.session.commit()




 


#populate the strategies table in database manually

strategies=["OpeningRangeBreakout","BuySlightDipStrategy","SmaStrategy"]
for strategy in strategies:
    strategy=Strategy(name=strategy)
    db.session.add(strategy)
db.session.commit()
 