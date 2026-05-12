import streamlit as st
import requests

st.set_page_config(page_title="GenAI Trading Assistant", layout="wide")
st.title("🚀 GenAI Trading Assistant")

# API base URL
API_BASE_URL = "http://127.0.0.1:8000"

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Market type selection
    market_type = st.radio(
        "Market Type",
        options=["spot", "futures"],
        help="Choose between spot or futures trading"
    )
    
    # Load available symbols
    @st.cache_data(ttl=300)
    def fetch_symbols(market_type):
        try:
            response = requests.get(
                f"{API_BASE_URL}/symbols",
                params={"market_type": market_type},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('symbols', [])
            return []
        except Exception as e:
            st.error(f"Error loading symbols: {e}")
            return []
    
    symbols = fetch_symbols(market_type)
    
    if symbols:
        st.info(f"📊 {len(symbols)} trading pairs available")
        
        # Search box for filtering
        search_term = st.text_input(
            "🔍 Search token",
            placeholder="e.g., BTC, ETH, SOL",
            help="Search for a specific trading pair"
        )
        
        # Filter symbols based on search
        if search_term:
            filtered_symbols = [s for s in symbols if search_term.upper() in s]
            st.caption(f"Found {len(filtered_symbols)} matches")
        else:
            filtered_symbols = symbols
        
        # Symbol selection
        selected_symbol = st.selectbox(
            "Select Token",
            options=filtered_symbols,
            index=0 if filtered_symbols else 0,
            help="Choose a trading pair to analyze"
        )
        
        # Timeframe selection
        selected_timeframe = st.selectbox(
            "Timeframe",
            options=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"],
            index=4,  # Default to 1h
            help="Select the candle timeframe"
        )
        
        st.divider()
        st.info(f"📊 Analyzing {selected_symbol} on {selected_timeframe}")
    else:
        st.warning("Failed to load symbols. Make sure the backend is running.")
        selected_symbol = "BTC/USDT"
        selected_timeframe = "1h"

# Main content area
col1, col2 = st.columns([3, 1])

with col2:
    analyze_button = st.button(
        "🔍 Analyze Market",
        type="primary",
        use_container_width=True
    )

if analyze_button:
    with st.spinner(f"Analyzing {selected_symbol}..."):
        try:
            response = requests.get(
                f"{API_BASE_URL}/analyze",
                params={
                    "symbol": selected_symbol,
                    "timeframe": selected_timeframe
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis = data.get('analysis', 'No analysis available')
                
                st.subheader(f"📈 Analysis for {selected_symbol} ({selected_timeframe})")
                st.markdown(analysis)
                
                # Show metadata
                with st.expander("📋 Details"):
                    st.write(f"**Symbol:** {data.get('symbol')}")
                    st.write(f"**Timeframe:** {data.get('timeframe')}")
            else:
                st.error(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The analysis might still be processing.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Make sure it's running on http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🤖 Powered by Gemini AI")
with col2:
    st.caption("📊 Data from Binance")
with col3:
    st.caption("💡 Technical Analysis with Pandas-TA")