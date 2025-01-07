#!/usr/bin/env python3
import socket
import datetime
import os

def main():
    # 포트 번호 설정
    PORT = 3000

    # 로그 디렉터리 및 파일 생성
    DATESTR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    LOGDIR = "./logs"
    os.makedirs(LOGDIR, exist_ok=True)
    LOGFILE = os.path.join(LOGDIR, f"hexorigin_{DATESTR}.log")

    print(f"Logs will be saved to {LOGFILE}")
    print(f"Starting UDP listener on port {PORT}...")

    # 패킷 카운트
    count = 0

    # 소켓 생성 및 바인딩
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # SO_REUSEADDR 옵션 활성화 - Ignore : Address already in use 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("", PORT))

    # 로그 파일 열기
    with open(LOGFILE, "a", encoding="utf-8") as f:
        while True:
            # 최대 65535바이트 수신 (UDP의 최대 페이로드 크기)
            data, addr = sock.recvfrom(65535)
            count += 1

            # 받은 데이터 디코딩 (에러 발생 시 대체 문자)
            data_str = data.decode("utf-8", errors="replace")

            # 터미널 출력
            print(f"[Packet #{count} from {addr}] {data_str}\n")

            # 로그 파일에도 동일하게 기록
            f.write(f"[Packet #{count} from {addr}] {data_str}\n\n")
            f.flush()

if __name__ == "__main__":
    main()
