# tools/groq_tool.py
import requests
import logging
from config.settings import GROQ_API_KEY

class GroqTool:
    def __init__(self, model="openai/gpt-oss-120b"):  # Accept model here
        self.api_key = GROQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = model  # Set the model

    def generate_text(self, prompt: str):
        if not self.api_key:
            logging.warning("GroqTool: No API key set; returning placeholder")
            return f"[Placeholder itinerary for prompt: {prompt[:120]}...]"

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 400
            }

            r = requests.post(self.api_url, headers=headers, json=payload, timeout=20)

            if r.status_code != 200:
                logging.error(f"GroqTool error {r.status_code}: {r.text}")
                return f"[Error generating itinerary: {r.status_code}]"

            return r.json()["choices"][0]["message"]["content"].strip()

        except Exception as e:
            logging.error(f"GroqTool exception: {e}")
            return f"[Error generating itinerary: {e}]"

