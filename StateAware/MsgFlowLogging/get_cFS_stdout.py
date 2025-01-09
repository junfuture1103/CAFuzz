import socket

# UDP 서버 설정
UDP_IP = "127.0.0.1"  # 수신할 IP 주소
UDP_PORT = 3001       # 수신할 포트 번호

# 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# SO_REUSEADDR 옵션 활성화 - Ignore : Address already in use 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")

# 무한 루프에서 데이터 수신
try:

    partial_buffer = ''     # 패킷 분할 처리 시 발생하는 누락 라인 임시 저장

    while True:
        # 데이터를 수신 (UDP는 연결 개념이 없으므로 계속 대기)
        data, addr = sock.recvfrom(65535)
        if not data:
            # 아무것도 수신하지 못했을 경우 계속 대기
            continue

        # 바이너리 -> 문자열 디코딩
        decoded = data.decode('utf-8', errors='replace')

        # 이전에 남아 있던 partial_buffer와 합쳐서 '\n' 기준으로 라인 분리
        lines = (partial_buffer + decoded).split('\n')

        # 마지막 요소가 완전한 라인이 아닐 수 있으므로 별도 보관
        partial_buffer = lines[-1]
        lines = lines[:-1]

        # 분리한 각 라인에 대해 처리
        for line in lines:
            # 콘솔 출력 & 로그 파일에 기록
            print("line printed : ", line)

except KeyboardInterrupt:
    print("\nTerminating UDP server.")
finally:
    sock.close()
