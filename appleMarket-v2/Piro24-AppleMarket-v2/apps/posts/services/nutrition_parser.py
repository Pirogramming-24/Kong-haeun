import re

NUTRI_KEYS = ["탄수화물", "단백질", "지방", "포화지방", "트랜스지방"]

def extract_block(text: str, key: str):
    """
    key 이후 다음 영양소 키 전까지만 잘라냄
    """
    idx = text.find(key)
    if idx == -1:
        return ""

    sub = text[idx + len(key):]
    end = len(sub)

    for k in NUTRI_KEYS:
        if k != key and k in sub:
            end = min(end, sub.find(k))

    return sub[:end]


def extract_number(block: str):
    """
    block 안에서 첫 숫자만 추출
    """
    m = re.search(r"(\d+(?:\.\d+)?)", block)
    if m:
        return float(m.group(1))
    return None


def parse_nutrition(texts: list[str]) -> dict:
    joined = " ".join(texts).lower()

    result = {
        "calorie": None,
        "carb": None,
        "protein": None,
        "fat": None,
    }

    
    # 1. 칼로리
    kcal_candidates = []

    for m in re.finditer(r"(\d{2,4})\s*kca[l!]*", joined):
        kcal = int(m.group(1))
        if kcal < 1000:
            kcal_candidates.append(kcal)

    if kcal_candidates:
        result["calorie"] = max(kcal_candidates)

    # 2. 탄수화물
    block = extract_block(joined, "탄수화물")
    result["carb"] = extract_number(block)

    # 3. 단백질
    block = extract_block(joined, "단백질")
    result["protein"] = extract_number(block)

    # 4. 지방 (포화/트랜스 제외)
    block = extract_block(joined, "지방")
    if "포화지방" not in block and "트랜스지방" not in block:
        result["fat"] = extract_number(block)

    return result
