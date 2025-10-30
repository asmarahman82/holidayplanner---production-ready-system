# tools/huggingface_tool.py
import os, requests, logging
from config.settings import HUGGINGFACE_API_KEY

class HuggingFaceTool:
    def __init__(self):
        self.api_key = HUGGINGFACE_API_KEY
        # default summarization endpoint (can be changed)
        self.endpoint = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    def summarize(self, text: str):
        if not self.api_key:
            logging.warning("HuggingFaceTool: No API key; returning truncated text")
            return text[:300] + ("..." if len(text) > 300 else "")
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            r = requests.post(self.endpoint, headers=headers, json={"inputs": text}, timeout=12)
            r.raise_for_status()
            out = r.json()
            if isinstance(out, list) and "summary_text" in out[0]:
                return out[0]["summary_text"]
            # sometimes HF returns dict with generated_text
            if isinstance(out, dict) and "generated_text" in out:
                return out["generated_text"]
            return str(out)
        except Exception as e:
            logging.error(f"HuggingFaceTool error: {e}")
            return text[:300] + ("..." if len(text) > 300 else "")
