"""
modelogic.py
-------------
Model adapter for dialogue intent classification.

Responsibility:
- Receive a prompt string
- Ask the LLM
- Return a single classification label (string)

"""

# from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")
_client = OpenAI()
# DEFAULT_API_BASE = "https://api.openai.com/v1"
_MODEL_NAME = "gpt-4o-mini"
_TEMPERATURE = 0.0
_MAX_TOKENS = 16

def generateOutput(prompt: str, system_prompt: str) -> str:
    """
    Given a fully-formed classification prompt,
    returns a single intent label as a string.
    """

    response = _client.chat.completions.create(
        model=_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=_TEMPERATURE,
        max_tokens=_MAX_TOKENS,
    )

    raw_output = response.choices[0].message.content.strip()

    # Minimal sanitization: take first token / line
    classification = raw_output.split()[0]

    return classification


def generateOutputAnswer(prompt: str, system_prompt: str) -> str:
    """
    Given a fully-formed classification prompt,
    returns a single intent label as a string.
    """

    response = _client.chat.completions.create(
        model=_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=_TEMPERATURE,
        max_tokens=_MAX_TOKENS,
    )
    # print("response")
    # print(response)
    # raw_output = response.choices[0].message.content.strip()

    # # Minimal sanitization: take first token / line
    # classification = raw_output.split()[0]

    # return response
    print(response)
    return {
        "id": response.id,
        "model": response.model,
        "created": response.created,
        "choices": [
            {
                "index": c.index,
                "finish_reason": c.finish_reason,
                "message": {
                    "role": c.message.role,
                    "content": c.message.content
                }
            }
            for c in response.choices
        ],
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
    }

    # return {
    # "content": response.choices[0].message.content,
    # "finish_reason": response.choices[0].finish_reason,
    # "usage": {
    #     "prompt_tokens": response.usage.prompt_tokens,
    #     "completion_tokens": response.usage.completion_tokens,
    #     "total_tokens": response.usage.total_tokens,
    #     }
    # }



# def _headers(open_ai_key: str) -> Dict[str, str]:
#     return {
#         "Authorization": f"Bearer {open_ai_key}",
#         "Content-Type": "application/json",
#     }


# def send_chat_completion(
#     open_ai_key: str,
#     messages: List[Dict[str, str]],
#     model: str = "gpt-4o-mini",
#     api_base: str = DEFAULT_API_BASE,
#     timeout: Optional[float] = 15.0,
# ) -> Dict[str, Any]:



    # url = f"{api_base}/chat/completions"
    # payload = {
    #     "model": model,
    #     "messages": messages,
    #     "temperature": 0,
    #     "max_tokens": 32,
    # }

    # resp = requests.post(
    #     url,
    #     headers=_headers(open_ai_key),
    #     json=payload,
    #     timeout=timeout,
    # )
    # resp.raise_for_status()
    return resp.json()


# def extract_text_from_response(response: Dict[str, Any]) -> str:
#     try:
#         return response["choices"][0]["message"]["content"]
#     except Exception:
#         return ""

# def generateResponse(response: Dict[str, Any]) -> str:
#     return ""

# def generateClassification(response: Dict[str, Any]) -> str:
#     if not open_ai_key:
#         raise RuntimeError("OPENAI_API_KEY is missing")
#     model = "gpt-4o-mini",
#     timeout = 15.0,
#     # sample_messages = [
#     #     {"role": "system", "content": "You are an npc inside a game."},
#     #     {"role": "user", "content": "Introduce yourself, explaining what are you."}
#     # ]

#     return ""


