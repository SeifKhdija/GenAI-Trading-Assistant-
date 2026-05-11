import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

_model = None

def get_model():
    """Lazy load the model with fallback to alternative models."""
    global _model
    if _model is not None:
        return _model
    
    # Try available models in order of preference (with models/ prefix)
    models_to_try = [
        'models/gemini-2.5-flash',
        'models/gemini-2.5-pro',
        'models/gemini-2.0-flash',
        'models/gemini-pro-latest',
        'models/gemini-flash-latest'
    ]
    
    for model_name in models_to_try:
        try:
            test_model = genai.GenerativeModel(model_name)
            # Actually test if the model works
            test_model.generate_content("test")
            _model = test_model
            print(f"✓ Using model: {model_name}")
            return _model
        except Exception as e:
            print(f"⚠ Model {model_name} not available: {str(e)[:50]}")
            continue
    
    raise ValueError("No compatible Gemini model found. Please check your API key and plan.")


def ask_gemini(prompt):
    """Generate content using the selected Gemini model."""
    try:
        model = get_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = f"Error generating content: {str(e)}"
        print(f"✗ {error_msg}")
        return error_msg