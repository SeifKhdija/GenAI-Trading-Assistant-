import streamlit as st
import requests

st.title("GenAI Trading Assistant")

if st.button("Analyze BTC"):
    response = requests.get('http://127.0.0.1:8000/analyze')

    data = response.json()

    st.write(data['analysis'])