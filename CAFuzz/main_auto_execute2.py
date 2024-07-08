import subprocess
import time
import os
from datetime import datetime

def run_main_script():
    total_runs = 0
    error_count = 0

    try:
        while True:
            total_runs += 1
            try:
                # main.py 실행, stderr를 캡처하여 오류 발생 시 파일에 기록
                result = subprocess.run(['python3', 'main2.py'], check=True, stderr=subprocess.PIPE, text=True)
            except subprocess.CalledProcessError as e:
                error_count += 1

                # 현재 날짜와 시간을 포맷하여 문자열로 변환
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                error_filename = f"error_log_{timestamp}.txt"

                # error_log.txt가 이미 존재하면 새로운 이름의 파일 생성
                if os.path.exists('error_log.txt'):
                    os.rename('error_log.txt', error_filename)

                # 오류 내용을 파일에 기록
                with open('error_log.txt', 'a') as error_file:
                    error_file.write(f"main.py 실행 중 오류 발생: {e}\n")
                    error_file.write(f"stderr:\n{e.stderr}\n")

            # 필요한 경우 sleep을 통해 간격 조정
            time.sleep(0.05)  # 1초 대기 we dont need to wait ! it's fuzzing time!

    except KeyboardInterrupt:
        # 종료 시 총 실행 횟수와 오류 횟수 출력
        print(f"총 실행 횟수: {total_runs}")
        print(f"오류 횟수: {error_count}")

if __name__ == "__main__":
    run_main_script()
