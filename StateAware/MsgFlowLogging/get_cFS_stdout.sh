#!/bin/bash

# In guest -> Use below .sh command
# sudo ./core-cpu1 2>&1 | tee /dev/tty | nc -u 10.0.2.2 3001

# PORT == 3001 Two have to be same

# 현재 날짜/시간을 로그 파일 이름에 반영 (예: 2025-01-06_150150)
DATESTR=$(date +%Y-%m-%d_%H%M%S)

# 로그 디렉터리 및 파일명 설정
LOGDIR="./logs"
mkdir -p "${LOGDIR}"
LOGFILE="${LOGDIR}/netcat_${DATESTR}.log"

PORT=3001

# -u: UDP 모드
# -l: 리스너(서버) 모드
# -k: 연결이 끊겨도 종료되지 않고 계속 수신
# tee: 터미널에 출력하면서 동시에 파일에 기록
echo "Logs will be saved to ${LOGFILE}"
echo "Starting Netcat on port ${PORT} ..."

nc -u -l -k "${PORT}" | tee "${LOGFILE}"
