import mediapipe as mp
import math, time
from mediapipe.tasks.python import vision
import cv2 as cv
from mediapipe.tasks.python.core.base_options import BaseOptions
from visualization import draw_manual, print_RSP_result

## 필요한 함수 작성

# 거리 계산 함수
def distance(a,b):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2+(a.z-b.z)**2)

# 손가락 펴짐 여부 판단 함수
def is_finger_open(landmarks,tip,pip):
    wrist = landmarks[0]
    return distance(landmarks[tip],wrist) > distance(landmarks[pip],wrist)

# 가위/바위/보 판별 함수
# 0: Rock, 1: Paper, 2: Scissors
def classify_rps(landmarks):
    # 손가락 상태
    fingers = [
        is_finger_open(landmarks,8,6),   # 검지
        is_finger_open(landmarks,12,10), # 중지
        is_finger_open(landmarks,16,14), # 약지
        is_finger_open(landmarks,20,18), # 소지
    ]

    # 펴진 손가락 개수
    open_count = sum(fingers) 

    if open_count == 0:
        return 0 # Rock
    elif open_count == 2 and fingers[0] and fingers[1]: # 검지와 중지가 펴진 경우
        return 2 # Scissors
    elif open_count >= 4:
        return 1 # Paper
    else:
        return None

if __name__ == "__main__":
    # 실행 로직

    # 1. MediaPipe HandLandmarker 설정
    options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path="Piro24-RPSGame/hand_landmarker.task"),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1
    )

    detector = vision.HandLandmarker.create_from_options(options)

    # 2. OpenCV 카메라 시작
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # 3. 실시간 프레임 처리
    while True:
        # 프레임 읽기
        ret, frame = cap.read()
 
        # 프레임을 정상적으로 읽었는지
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # OpenCV(BGR) -> MediaPipe(RGB) : 색상 공간 변환
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # MediaPipe 입력 객체 생성
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        # 타임스탬프 생성
        timestamp = int(time.time() * 1000)

        # 손 랜드마크 추론 실행
        result = detector.detect_for_video(mp_image, timestamp)
        
        # 기본 결과 초기화
        rps_result = None
        
        # 손이 인식된 경우만 처리
        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]
            rps_result = classify_rps(landmarks)

        # 4. 시각화
        frame = draw_manual(frame, result)
        frame = print_RSP_result(frame, rps_result)

        cv.imshow("RPS Game", frame)

        if cv.waitKey(1) == ord('q'):
            break
    
    # 5. 종료 처리
    cap.release()
    cv.destroyAllWindows()