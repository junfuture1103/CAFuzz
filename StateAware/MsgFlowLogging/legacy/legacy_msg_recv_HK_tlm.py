import socket
import logging
from datetime import datetime

# 수신할 IP와 포트 설정
UDP_IP = "127.0.0.1"
UDP_PORT = 1235

# 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 현재 날짜와 시간을 기반으로 로그 파일 생성
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"HK_tlm_logs/{current_time}.log"

# 로깅 설정
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}...")

count = 0

# 패킷 수신 및 출력
while True:
    data, addr = sock.recvfrom(1024)  # 버퍼 크기 1024 바이트
    hex_data = ' '.join(f'0x{byte:02X}' for byte in data)
    log_message = f"Received packet from {addr}: {hex_data}"
    print(log_message)
    print("count : ",count)
    count+=1
    logging.info(log_message)
