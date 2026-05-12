import ccxt
import pandas as pd

exchange = ccxt.binance()


def get_available_symbols(market_type='spot'):
    """
    Get all available trading symbols from Binance.
    
    Args:
        market_type: 'spot' or 'futures'
    
    Returns:
        List of available symbols (e.g., ['BTC/USDT', 'ETH/USDT', ...])
    """
    try:
        exchange.load_markets()
        symbols = exchange.symbols
        
        # Filter based on market type
        if market_type.lower() == 'futures':
            # Filter for perpetual futures (ending with :USDT or similar)
            symbols = [s for s in symbols if s.endswith(':USDT')]
        else:
            # Filter for spot trading
            symbols = [s for s in symbols if not s.endswith(':USDT')]
        
        # Sort and return
        return sorted(symbols)
    except Exception as e:
        print(f"Error fetching symbols: {e}")
        return []


def get_market_data(symbol='BTC/USDT', timeframe='1h', limit=200):
    """
    Fetch OHLCV data for a given symbol.
    
    Args:
        symbol: Trading pair (e.g., 'BTC/USDT', 'ETH/USDT')
        timeframe: Candle timeframe (e.g., '1h', '4h', '1d')
        limit: Number of candles to fetch
    
    Returns:
        DataFrame with OHLCV data
    """
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )

        return df
    except Exception as e:
        print(f"Error fetching market data for {symbol}: {e}")
        return pd.DataFrame()
