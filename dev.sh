#!/bin/sh
# Start the API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 &

# Start the UI
streamlit run ui/01_🏠_Home.py --server.port 8501
