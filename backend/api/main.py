from fastapi import FastAPI

from backend.rag.chroma_store import load_knowledge
from backend.services.analysis_service import generate_market_analysis

app = FastAPI()

load_knowledge()


@app.get('/')
def home():
    return {'message': 'GenAI Trading Assistant Running'}


@app.get('/analyze')
def analyze_market():
    result = generate_market_analysis()

    return {
        'analysis': result
    }