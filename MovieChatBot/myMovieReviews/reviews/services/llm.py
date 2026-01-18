import os
import requests

UPSTAGE_API_URL = "https://api.upstage.ai/v1/chat/completions"

def ask_llm(question, context):
    api_key = os.getenv("UPSTAGE_API_KEY")
    if not api_key:
        raise RuntimeError("UPSTAGE_API_KEY가 설정되지 않았습니다.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "solar-1-mini-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "너는 영화 추천 전문가야. "
                    "아래 제공된 영화 정보와 리뷰를 바탕으로만 한국어로 대답해."
                    "추천 영화 제목과 이유를 같이 말하고 모르면 모른다고 말해."
                ),
            },
            {
                "role": "user",
                "content": f"""
질문:
{question}

참고 정보:
{context}
"""
            },
        ],
        "temperature": 0.7,
    }

    response = requests.post(
        UPSTAGE_API_URL,
        headers=headers,
        json=payload,
        timeout=20,
    )
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
