#!/bin/bash
set -e

if [ "$MODE" = "streamlit" ]; then
    echo "🌐 Starting Streamlit UI..."
    streamlit run ui/app_streamlit.py --server.port 8501 --server.address 0.0.0.0
else
    echo "⚡ Running full pipeline..."
    python run_full_pipeline.py
fi
