import cv2
from ultralytics import YOLO

# YOLOv8 모델 로드 (pre-trained COCO 모델)
model = YOLO('yolov8n.pt')  # yolov8n은 Nano 모델로, 속도와 정확도 사이의 균형을 잡은 모델입니다.

# 카메라 캡처 초기화
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # YOLOv8 모델을 사용하여 객체 탐지 수행
    results = model(frame)

    # 결과에서 인식된 클래스 이름 추출 및 출력
    for result in results:
        for label in result.names.values():
            print(f"Detected: {label}")

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
