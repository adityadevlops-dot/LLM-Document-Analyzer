import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")

CHAT_URL = f"{BASE_URL}/chat/completions"

def ask_llm(context: str, question: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-5-nano",   # ✅ OpenAI model supported by AI Pipe
        "messages": [
            {
                "role": "system",
                "content": "Answer only from the given context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
    }

    response = requests.post(CHAT_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"AI Pipe Error: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]
