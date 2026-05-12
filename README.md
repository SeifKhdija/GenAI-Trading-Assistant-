# GenAI Trading Assistant 🚀

An AI-powered trading assistant that analyzes real-time market data, retrieves financial context using RAG (Retrieval-Augmented Generation), and generates structured trading insights automatically using LLMs.

---

# Features

- 📈 Real-time crypto market analysis
- 🤖 AI-generated trading insights
- 🧠 RAG-based financial context retrieval
- 📊 Technical indicators (RSI, MACD, EMA)
- 🔍 Vector database for contextual memory
- ⚡ FastAPI backend
- 💬 Streamlit AI dashboard
- 🪙 Binance market integration
- 🧩 Modular AI architecture

---

# Tech Stack

## Backend
- Python
- FastAPI

## AI / GenAI
- LangChain
- Gemini API / Ollama
- Sentence Transformers

## Vector Database
- ChromaDB

## Market Data
- Binance API
- CCXT

## Indicators
- Pandas
- Pandas TA

## Frontend
- Streamlit

---

# Architecture

```text
Market APIs
(Binance / CoinGecko)
        ↓
Market Data Engine
        ↓
Technical Indicators
(RSI, MACD, EMA)
        ↓
RAG Layer
(ChromaDB + Embeddings)
        ↓
LLM
(Gemini / Llama3)
        ↓
AI Trading Insight Generator
        ↓
Frontend Dashboard
```

---

# Example AI Output

```json
{
  "market_summary": "BTC shows bullish momentum with increasing volume.",
  "bullish_scenario": "Breakout above resistance could continue upward trend.",
  "bearish_scenario": "Failure near resistance may trigger short-term pullback.",
  "risk_level": "Medium",
  "confidence": 74
}
```

---

# Project Structure

```text
project/
│
├── backend/
│   ├── api/
│   ├── indicators/
│   ├── llm/
│   ├── market/
│   ├── rag/
│   └── services/
│
├── frontend/
│
├── vector_db/
│
└── datasets/
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/genai-trading-assistant.git

cd genai-trading-assistant
```

---

# Create Virtual Environment

## Windows

```bash
python -m venv venv

venv\Scripts\activate
```

## Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
```

---

# Run Backend

```bash
uvicorn backend.api.main:app --reload
```

---

# Run Frontend

```bash
streamlit run frontend/app.py
```
