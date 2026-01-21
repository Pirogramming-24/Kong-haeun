from transformers import pipeline

# 1. 요약 모델
_summarizer = pipeline(
    "summarization", model="facebook/bart-large-cnn"
)

def summarize_text(user_input: str) -> str:
    if not user_input or not user_input.strip():
        return "Input text is empty."

    # (1) 모델 호출
    result = _summarizer(
        user_input.strip(),
        max_length=120,
        min_length=30,
        do_sample=False,
    )

    # (2) 결과 추출
    summary = result[0]["summary_text"].strip()

    # (3) fallback
    if not summary:
        return "I couldn't generate a summary."

    return summary
        

# 2. 감정 분석 모델
_sentiment = pipeline(
    "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(user_input: str) -> str:
    if not user_input or not user_input.strip():
        return "Input text is empty."

    # (1) 모델 호출
    result = _sentiment(user_input.strip())[0]

    # (2) 결과 추출
    label = result["label"]
    score = result["score"]

    return f"{label} (confidence: {score:.2f})"


# 3. 텍스트 생성 모델
_generator = pipeline(
    "text-generation", model="distilgpt2"
)

def generate_text(user_input: str) -> str:
    if not user_input or not user_input.strip():
        return "Input text is empty."
    
    prompt = (
        "Continue the following text naturally in English.\n"
        f"Text: {user_input.strip()}\n"
        "Continuation:"
    )

    # (1) 모델 호출
    result = _generator(
        prompt,
        max_new_tokens=60,

        # 반복 방지
        repetition_penalty=1.2,
        no_repeat_ngram_size=4,
        length_penalty=1.05,

        # 디코딩
        do_sample=True,
        temperature=0.5,
        top_p=0.9,

        return_full_text=True,
    )

    # (2) 결과 후처리
    text = result[0]["generated_text"]
    out = text.split("Continuation:", 1)[-1].strip()

    # (3) 불필요한 라벨 제거
    for stop in ["Text:", "User:", "Assistant:", "Question:"]:
        if stop in out:
            out = out.split(stop, 1)[0].strip()

    # (4) fallback
    if not out:
        return "I couldn't generate a good answer."

    return out
        