from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import os
import requests

load_dotenv()

DEFAULT_API_BASE = "https://api.openai.com/v1"


def _headers(open_ai_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {open_ai_key}",
        "Content-Type": "application/json",
    }


def send_chat_completion(
    open_ai_key: str,
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-mini",
    api_base: str = DEFAULT_API_BASE,
    timeout: Optional[float] = 15.0,
) -> Dict[str, Any]:

    if not open_ai_key:
        raise RuntimeError("OPENAI_API_KEY is missing")

    url = f"{api_base}/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": 32,
    }

    resp = requests.post(
        url,
        headers=_headers(open_ai_key),
        json=payload,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def extract_text_from_response(response: Dict[str, Any]) -> str:
    try:
        return response["choices"][0]["message"]["content"]
    except Exception:
        return ""


if __name__ == "__main__":
    open_ai_key = os.getenv("OPEN_AI_KEY")

    sample_messages = [
        {"role": "system", "content": "You are an npc inside a game."},
        {"role": "user", "content": "Introduce yourself, explaining what are you."}
    ]

    try:
        resp = send_chat_completion(open_ai_key, sample_messages)
        print("Assistant:", extract_text_from_response(resp))
    except Exception as e:
        print("Request failed:", e)
