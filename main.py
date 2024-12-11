import pyupbit
from pkg.validTickers import *

daily_ohlcv = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")

print(daily_ohlcv)