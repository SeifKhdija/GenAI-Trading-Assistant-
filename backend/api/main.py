from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.rag.chroma_store import load_knowledge
from backend.services.analysis_service import generate_market_analysis
from backend.market.fetch_data import get_available_symbols

app = FastAPI()

load_knowledge()


@app.get('/')
def home():
    return {'message': 'GenAI Trading Assistant Running'}


@app.get('/symbols')
def get_symbols(market_type: str = 'spot', search: str = ''):
    """
    Get available trading symbols from Binance.
    
    Args:
        market_type: 'spot' or 'futures'
        search: Optional search term to filter symbols (e.g., 'BTC', 'ETH')
    
    Returns:
        List of available symbols (all symbols returned, can be filtered by search)
    """
    try:
        symbols = get_available_symbols(market_type=market_type)
        
        # Filter by search term if provided
        if search:
            search_upper = search.upper()
            symbols = [s for s in symbols if search_upper in s]
        
        return {
            'market_type': market_type,
            'search_filter': search if search else None,
            'count': len(symbols),
            'symbols': symbols  # Return all (or filtered) symbols
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'error': str(e)}
        )


@app.get('/analyze')
def analyze_market(symbol: str = 'BTC/USDT', timeframe: str = '1h'):
    """
    Analyze market for a given symbol.
    
    Args:
        symbol: Trading pair (e.g., 'BTC/USDT', 'ETH/USDT')
        timeframe: Candle timeframe (e.g., '1h', '4h', '1d')
    
    Returns:
        Market analysis from AI
    """
    try:
        result = generate_market_analysis(symbol=symbol, timeframe=timeframe)
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'analysis': result
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'error': str(e), 'symbol': symbol}
        )