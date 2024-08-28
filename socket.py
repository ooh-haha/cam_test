## 서버 ##
import socket

# 서버 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))
server_socket.listen(1)

print("Server is waiting for connection...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    # 가상 환경에서 실행된 값을 전송
    detected_object = "bottle:0.95"  # 예시 데이터
    conn.sendall(detected_object.encode())
    
    # 잠시 대기
    time.sleep(1)


## 클래스 값 전달 서버 ##
import socket
from picamera2 import Picamera2, Preview
import cv2
from ultralytics import YOLO

# 소켓 서버 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))
server_socket.listen(1)

print("Server is waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# YOLOv8 모델 로드
model = YOLO('/home/pi/models/yolov8s.pt')

# Picamera2 초기화 및 카메라 시작
picam2 = Picamera2()
picam2.start()

try:
    while True:
        frame = picam2.capture_array()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        # 객체 탐지 수행
        results = model(frame_rgb)

        for obj in results.boxes.data:
            class_id = int(obj[5])
            class_name = model.names[class_id]
            confidence = obj[4].item()
            bbox = obj[0:4].tolist()

            # 클래스 이름과 신뢰도를 문자열로 만들기
            detection_info = f"{class_name} {confidence:.2f}"
            
            # 탐지된 클래스와 신뢰도 정보를 클라이언트에 전송
            conn.sendall(detection_info.encode())

            # 바운딩 박스와 라벨을 그리는 코드 (생략 가능)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
            label = f"{class_name} {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), 
                          (int(bbox[0]) + label_size[0], int(bbox[1]) - label_size[1]), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, label, (int(bbox[0]), int(bbox[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # 화면에 프레임 출력 (옵션)
        cv2.imshow("YOLOv8 Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()


## 클라이언트 ##
import socket

# 클라이언트 소켓 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('<라즈베리파이5의 IP>', 65432))

while True:
    # 서버로부터 데이터 수신
    data = client_socket.recv(1024)
    if data:
        print(f"Received data: {data.decode()}")
