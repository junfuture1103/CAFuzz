import subprocess
import time
import random
import os
from datetime import datetime
import telnetlib

# snapshot_name = "snapshot-done"
snapshot_name = "snapshot-fuzzing-cFS"

# 현재 날짜와 시간을 포맷하여 문자열로 변환
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
error_path = "./error_logs"
error_filename = f"error_log_{timestamp}.txt"

total_runs = 0
total_cycles = 0
error_count = 0

def send_cmd(tn, cmd):
    """
    QEMU 모니터 명령어를 실행하고 결과를 반환.
    """
    tn.write(cmd.encode('utf-8') + b'\n')
    return tn.read_until(b"(qemu) ").decode('utf-8')

def run_main_script():
    global total_runs, error_count

    random_attempts = random.randint(0, 100)
    attempt_count = 0

    while True:
        if attempt_count >= random_attempts:
            break

        total_runs += 1
        attempt_count += 1

        try:
            # main.py 실행, stderr를 캡처하여 오류 발생 시 파일에 기록
            result = subprocess.run(['python3', 'main.py'],
                                    check=True,
                                    stderr=subprocess.PIPE,
                                    text=True)
        except subprocess.CalledProcessError as e:
            error_count += 1
        

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 4444
    # Telnet 연결
    tn = telnetlib.Telnet(HOST, PORT)

    # 모니터 초기 프롬프트 수신
    output = tn.read_until(b"(qemu) ")
    print("Initial Monitor Output:\n", output.decode())

    # 스냅샷 목록 확인
    snaps = send_cmd(tn, "info snapshots")
    print("Snapshots:\n", snaps)

    try:
        while True:
            # re-load the snapshot after 1 test cycle
            print(f"Loading snapshot: {snapshot_name}")
            load_result = send_cmd(tn, f"loadvm {snapshot_name}")
            print(f"Snapshot Load Result:\n{load_result}")

            run_main_script()
            total_cycles += 1

    except KeyboardInterrupt:
        # 종료 시 총 실행 횟수와 오류 횟수 출력
        print(f"총 실행 횟수: {total_runs}")
        print(f"총 cycle 실행 횟수: {total_cycles}")
        print(f"오류 횟수: {error_count}")
