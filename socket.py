# 서버
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

# 클라이언트
import socket

# 클라이언트 소켓 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('<라즈베리파이5의 IP>', 65432))

while True:
    # 서버로부터 데이터 수신
    data = client_socket.recv(1024)
    if data:
        print(f"Received data: {data.decode()}")
