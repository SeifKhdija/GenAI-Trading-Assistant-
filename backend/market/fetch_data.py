import ccxt
import pandas as pd

exchange = ccxt.binance()


def get_market_data(symbol='BTC/USDT', timeframe='1h', limit=200):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    df = pd.DataFrame(
        ohlcv,
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
    )

    return df