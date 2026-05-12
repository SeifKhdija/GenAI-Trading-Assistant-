from backend.market.fetch_data import get_market_data
from backend.indicators.indicators import calculate_indicators
from backend.rag.chroma_store import search_context
from backend.llm.gemini_client import ask_gemini


def generate_market_analysis(symbol='BTC/USDT', timeframe='1h'):
    """
    Generate AI-powered market analysis for a given symbol.
    
    Args:
        symbol: Trading pair (e.g., 'BTC/USDT', 'ETH/USDT')
        timeframe: Candle timeframe (e.g., '1h', '4h', '1d')
    
    Returns:
        String with detailed market analysis
    """
    # Extract token name (e.g., 'BTC' from 'BTC/USDT')
    token_name = symbol.split('/')[0]
    
    df = get_market_data(symbol=symbol, timeframe=timeframe)

    if df.empty:
        return f"Error: Unable to fetch data for {symbol}"

    df = calculate_indicators(df)

    latest = df.iloc[-1]

    rsi = latest.get('rsi', 'N/A')
    macd = latest.get('macd', 'N/A')
    close = latest.get('close', 'N/A')

    query = f"{token_name} {symbol} RSI {rsi} MACD {macd} trend analysis"

    context = search_context(query)

    prompt = f'''
    Analyze {symbol} market conditions on {timeframe} timeframe.

    Current data:
    - Price: ${close}
    - RSI: {rsi}
    - MACD: {macd}

    Context:
    {context}

    Generate:
    1. Market Summary
    2. Bullish Scenario
    3. Bearish Scenario
    4. Risk Level
    5. Key Zones
    '''

    result = ask_gemini(prompt)

    return result