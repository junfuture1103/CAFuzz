#!/bin/bash

# 프로그램이 종료될 때마다 재시작하는 무한 루프
while true; do
    echo "Starting AFL fuzzing process..."

    # 커맨드 실행
    sudo AFL_CUSTOM_MUTATOR_LIBRARY=/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/AFLCustomMutator/cFS_send_udp_command_aware.so \
    AFL_CUSTOM_MUTATOR_LATE_SEND=1 \
    CUSTOM_SEND_READ=1 \
    AFL_DEBUG=1 \
    CUSTOM_SEND_IP=127.0.0.1 \
    CUSTOM_SEND_PORT=1234 \
    /AFLplusplus/afl-fuzz -i in -o out -t 4000 -- ./core-cpu1

    # 종료 시 메세지 출력 및 5초 대기 후 재시작
    echo "AFL fuzzing process terminated. Restarting in 5 seconds..."
    sleep 5
done

