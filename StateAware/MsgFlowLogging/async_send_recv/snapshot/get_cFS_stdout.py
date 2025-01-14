#!/usr/bin/env python3
import socket
import datetime
import os

def create_log_file(logdir):
    """새로운 로그 파일을 생성하고 파일 경로를 반환."""
    datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    logfile = os.path.join(logdir, f"stdout_{datestr}.log")
    return logfile

def main():
    # 포트 번호 설정
    PORT = 3001
    UDP_IP = "127.0.0.1"

    # 최상위 로그 디렉터리 생성
    BASE_LOGDIR = "./logs/cFS-stdout"
    os.makedirs(BASE_LOGDIR, exist_ok=True)

    # 세션별 디렉터리 생성
    session_dir = datetime.datetime.now().strftime("stdout_%Y-%m-%d_%H%M%S_session")
    LOGDIR = os.path.join(BASE_LOGDIR, session_dir)
    os.makedirs(LOGDIR, exist_ok=True)

    # 첫 번째 로그 파일 생성
    logfile = create_log_file(LOGDIR)

    print(f"Logs will be saved to {LOGDIR}")
    print(f"Starting UDP listener on {UDP_IP}:{PORT}...")

    # 패킷 카운트
    count = 0

    # 소켓 생성 및 바인딩
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # SO_REUSEADDR 옵션 활성화
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((UDP_IP, PORT))

    partial_buffer = ''  # 패킷 분할 처리 시 발생하는 누락 라인 임시 저장

    try:
        with open(logfile, "a", encoding="utf-8") as f:
            while True:
                # 최대 65535바이트 수신
                data, addr = sock.recvfrom(65535)
                count += 1

                # 받은 데이터 디코딩
                decoded = data.decode("utf-8", errors="replace")

                # 이전에 남아 있던 partial_buffer와 합쳐서 '\n' 기준으로 라인 분리
                lines = (partial_buffer + decoded).split('\n')

                # 마지막 요소가 완전한 라인이 아닐 수 있으므로 별도 보관
                partial_buffer = lines[-1]
                lines = lines[:-1]

                # 분리한 각 라인에 대해 처리
                for line in lines:
                    # "one cycle done" 메시지가 있으면 로그 파일을 분리
                    if "one cycle done" in line:
                        print("[INFO] 'one cycle done' detected. Splitting log file.")
                        f.close()  # 현재 로그 파일 닫기

                        # 새로운 로그 파일 생성
                        logfile = create_log_file(LOGDIR)
                        f = open(logfile, "a", encoding="utf-8")

                        print(f"[INFO] New log file created: {logfile}")

                    # 로그 파일에 기록
                    f.write(f"[Packet #{count} from {addr}] {line}\n")
                    f.flush()

                    # 콘솔 출력
                    print(f"line printed : {line}")

    except KeyboardInterrupt:
        print("\nTerminating UDP server.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
