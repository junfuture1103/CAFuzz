#!/bin/bash

# QEMU 실행 경로
QEMU_DIR="/home/jun20/jun/kaist_research/CAFuzz/SnapshotFuzzing"
QEMU_CMD="qemu-system-x86_64 \\
  -enable-kvm \\
  -m 4096 \\
  -drive file=./qcow2/ubuntu_vm.qcow2,if=virtio,cache=writeback \\
  -netdev user,id=net0,hostfwd=udp::1234-:1234,hostfwd=udp::1235-:1235,hostfwd=udp::3000-:3000,hostfwd=udp::3001-:3001 \\
  -device e1000,netdev=net0 \\
  -monitor telnet:127.0.0.1:4444,server,nowait"

# Python 스크립트 경로
SCRIPT_DIR="/home/jun20/jun/kaist_research/CAFuzz/StateAware/MsgFlowLogging/async_send_recv/snapshot"

# QEMU 실행
echo "Starting QEMU..."
cd $QEMU_DIR || exit
gnome-terminal -- bash -c "$QEMU_CMD; exec bash" &

sleep 1

# Python 스크립트 실행
echo "Starting Python scripts..."
gnome-terminal -- bash -c "cd $SCRIPT_DIR && python3 get_cFS_stdout.py; exec bash" &
gnome-terminal -- bash -c "cd $SCRIPT_DIR && python3 get_cFS_msg_hex.py; exec bash" &
gnome-terminal -- bash -c "cd $SCRIPT_DIR && python3 async_send_recv_snapshot.py; exec bash" &

# 기다리지 않고 백그라운드 실행 유지
wait
