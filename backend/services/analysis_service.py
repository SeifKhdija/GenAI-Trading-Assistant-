from backend.market.fetch_data import get_market_data
from backend.indicators.indicators import calculate_indicators
from backend.rag.chroma_store import search_context
from backend.llm.gemini_client import ask_gemini


def generate_market_analysis():
    df = get_market_data()

    df = calculate_indicators(df)

    latest = df.iloc[-1]

    rsi = latest['rsi']
    macd = latest['macd']
    close = latest['close']

    query = f"RSI {rsi}, MACD {macd}, BTC trend"

    context = search_context(query)

    prompt = f'''
    Analyze BTC market conditions.

    Current data:
    - Price: {close}
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