## 서버 ##
import socket
from picamera2 import Picamera2, Preview
import cv2
from ultralytics import YOLO

# Socket server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))
server_socket.listen(1)

print("Server is waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Load YOLOv8 model
model = YOLO('/home/pi/models/yolov8s.pt')

# Initialize Picamera2 and start the camera
picam2 = Picamera2()
picam2.start()

try:
    while True:
        frame = picam2.capture_array()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        # Perform object detection
        results = model(frame_rgb)

        for result in results:
            # `result.boxes` should be an iterable of detected objects
            for obj in result.boxes:
                # Debugging output to check the type and value of obj.cls and obj.conf
                print(f"Type of obj.cls: {type(obj.cls)}, value: {obj.cls}")
                print(f"Type of obj.conf: {type(obj.conf)}, value: {obj.conf}")

                try:
                    # Ensure proper extraction of values
                    class_id = int(obj.cls.item())  # Convert the class ID to an integer
                    class_name = model.names[class_id]
                    confidence = obj.conf.item()
                    bbox = obj.xyxy.tolist()

                    # Create a string with class name and confidence
                    detection_info = f"{class_name} {confidence:.2f}"
                    
                    # Send detected class and confidence information to the client
                    conn.sendall(detection_info.encode())

                    # Drawing bounding box and label (optional)
                    cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
                    label = f"{class_name} {confidence:.2f}"
                    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), 
                                  (int(bbox[0]) + label_size[0], int(bbox[1]) - label_size[1]), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, label, (int(bbox[0]), int(bbox[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                except Exception as e:
                    print(f"An error occurred: {e}")

        # Display the frame (optional)
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
