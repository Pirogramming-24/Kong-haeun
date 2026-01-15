from paddleocr import PaddleOCR
import cv2
import os
import tempfile
import numpy as np

# PaddleOCR 객체 생성
ocr = PaddleOCR(
    lang="korean",
    use_angle_cls=True
)

def run_ocr(image_path: str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"이미지 파일이 존재하지 않습니다: {image_path}")

    # 1. 이미지 로드
    with open(image_path, "rb") as f:
        file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("이미지를 OpenCV가 읽지 못했습니다")

    # 2. 전처리
    # Grayscale 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize (글자 확대)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Threshold (이진화)
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # 임시 파일로 저장 (전처리 결과)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        temp_path = tmp.name
        cv2.imwrite(temp_path, thresh)

    # 3. OCR 실행 (전처리된 이미지 사용)
    # PaddleOCR 결과 구조:
    # result -> [ [ [box, (text, confidence)], ... ] ]
    result = ocr.ocr(temp_path)

    texts = []
    for line in result:
        for word_info in line:
            texts.append(word_info[1][0]) # 실제 인식된 문자열

    os.remove(temp_path) # 임시 파일 제거
    return texts
