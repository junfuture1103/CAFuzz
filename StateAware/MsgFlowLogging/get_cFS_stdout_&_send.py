#!/usr/bin/env python3

import socket
import sys
import os
from datetime import datetime
import time
import subprocess

total_runs = 0
total_cycles = 0
error_count = 0

def send_cFS_cmd():
    global total_runs, error_count

    total_runs += 1
    try:
        # main.py 실행, stderr를 캡처하여 오류 발생 시 파일에 기록
        result = subprocess.run(['python3', '/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/main.py'],
                                check=True,
                                stderr=subprocess.PIPE,
                                text=True)
    except subprocess.CalledProcessError as e:
        error_count += 1

def main():

    # 사용자 설정
    PORT = 3001
    LOGDIR = "./logs"

    # 로그 파일 생성
    datestr = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)
    logfile_path = os.path.join(LOGDIR, f"stdout_{datestr}.log")

    print(f"Logs will be saved to {logfile_path}")
    print(f"Starting UDP server on port {PORT} ...")

    # 로그 파일 오픈
    with open(logfile_path, 'w', encoding='utf-8') as logf:
        
        # 소켓 생성 및 바인딩
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
        # SO_REUSEADDR 옵션 활성화 - Ignore : Address already in use 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('', PORT))

        accumulated_data = []  # 수신 라인 임시 저장
        newline_count = 0       # 연속 빈 줄 카운트
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
                logf.write(line + '\n')
                logf.flush()

                # 빈 줄(공백 문자까지 제거)인지 판별
                if not line.strip():
                    newline_count += 1
                    print("newLine : ", newline_count)
                    if newline_count >= 1:
                        # ===== Double Newline Detected =====
                        # make signal to Send New Command

                        # print("=====  New Msg Detected =====")
                        # logf.write("=====  New Msg Detected =====\n")

                        # 지금까지 누적된 블록( accumulated_data ) 출력
                        block_str = '\n'.join(accumulated_data)
                        # print("[Captured Block]")
                        print(block_str)
                        
                        # logf.write("[Captured Block]\n")
                        logf.write(block_str + '\n')
                        logf.flush()

                        # 블록 및 카운트 리셋
                        accumulated_data.clear()
                        newline_count = 0

                        # time.sleep(0.2)
                        # send_cFS_cmd()
                    else:
                        # 아직 두 줄 연속은 아니므로 누적
                        accumulated_data.append('')
                else:
                    # 빈 줄이 아니면 카운트 리셋 후 누적
                    newline_count = 0
                    accumulated_data.append(line)

        # 이 부분은 이론상 도달하기 어려우나(while True) 종료 시 처리를 원하면 추가
        # sock.close()

if __name__ == "__main__":
    main()
