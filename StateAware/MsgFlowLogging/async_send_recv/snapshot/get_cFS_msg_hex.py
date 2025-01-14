#!/usr/bin/env python3
import socket
import datetime
import os

def create_log_file(logdir):
    """새로운 로그 파일을 생성하고 파일 경로를 반환."""
    datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    logfile = os.path.join(logdir, f"hexorigin_{datestr}.log")
    return logfile

def main():
    # 포트 번호 설정
    PORT = 3000

    # 최상위 로그 디렉터리 생성
    BASE_LOGDIR = "./logs/cFS-hexorigin"
    os.makedirs(BASE_LOGDIR, exist_ok=True)

    # 세션별 디렉터리 생성
    session_dir = datetime.datetime.now().strftime("hexorigin_%Y-%m-%d_%H%M%S_session")
    LOGDIR = os.path.join(BASE_LOGDIR, session_dir)
    os.makedirs(LOGDIR, exist_ok=True)

    # 첫 번째 로그 파일 생성
    logfile = create_log_file(LOGDIR)

    print(f"Logs will be saved to {LOGDIR}")
    print(f"Starting UDP listener on port {PORT}...")

    # 패킷 카운트
    count = 0

    # 소켓 생성 및 바인딩
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # SO_REUSEADDR 옵션 활성화
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", PORT))

    # 로그 파일 열기
    with open(logfile, "a", encoding="utf-8") as f:
        while True:
            # 최대 65535바이트 수신
            data, addr = sock.recvfrom(65535)
            count += 1

            # 받은 데이터 디코딩
            data_str = data.decode("utf-8", errors="replace")

            # 터미널 출력
            print(f"[Packet #{count} from {addr}] {data_str}\n")

            # "one cycle done" 메시지가 있으면 로그 파일을 분리
            if "one cycle done" in data_str:
                print("[INFO] 'one cycle done' detected. Splitting log file.")
                f.close()  # 현재 로그 파일 닫기

                # 새로운 로그 파일 생성
                logfile = create_log_file(LOGDIR)
                f = open(logfile, "a", encoding="utf-8")

                print(f"[INFO] New log file created: {logfile}")

            # 로그 파일에 기록
            f.write(f"[Packet #{count} from {addr}] {data_str}\n\n")
            f.flush()

if __name__ == "__main__":
    main()
