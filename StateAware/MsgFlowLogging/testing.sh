#!/bin/bash
LOG_FILE="/home/jun20/jun/kaist_research/CAFuzz/StateAware/MsgFlowLogging/logs/cFS_output_log/cFS_msg_log_generation.log"

# 프로그램이 종료될 때마다 재시작하는 무한 루프
while true; do
    echo "Starting Msg Log Generation process..."

    # 프로그램 실행 후 로그를 파일과 화면에 동시에 출력
    sudo ./core-cpu1 2>&1 | tee -a "$LOG_FILE"
    # 종료 시 메세지 출력 및 5초 대기 후 재시작
    echo "Msg Log Generation process terminated. Restarting..."
done
