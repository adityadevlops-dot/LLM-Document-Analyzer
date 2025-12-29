import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AI_PIPE_API_KEY")
API_URL = os.getenv("AI_PIPE_URL")

print("DEBUG API_URL:", API_URL)


def ask_llm(context: str, question: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",   # ✅ OpenAI-compatible auth
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-1.5-flash",
        "messages": [
            {
                "role": "system",
                "content": "Answer only from the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"AI Pipe Error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]
