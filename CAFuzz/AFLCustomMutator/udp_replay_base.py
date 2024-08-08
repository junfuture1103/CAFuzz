import os
import socket
import time

# PATH = "./queue"
PATH = "./ex_commands"
# PATH = "./test"

# 디렉터리 경로와 UDP 설정
directory = PATH  # 파일들이 있는 디렉터리 경로
udp_ip = '127.0.0.1'
udp_port = 1234

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 디렉터리 내의 모든 파일 읽기
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    
    # 파일이 실제 파일인지 확인
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as file:
            data = file.read()
            # 데이터 UDP로 전송
            sock.sendto(data, (udp_ip, udp_port))
            print(f"Sent data from {filename} to {udp_ip}:{udp_port}")
            time.sleep(0.5)  # 1초 대기

sock.close()