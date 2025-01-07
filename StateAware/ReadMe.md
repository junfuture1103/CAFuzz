# MSG Flow 수집 테스팅 가이드

### 1. QEMU VM start
start the vm using .qcow2 file (if you don't have it, make it first)
1234 : Command Host -> Guest
1235 : Telemetry Guest -> Host
3000 : Orig Hex Guest -> Host
3001 : stdout Guest -> Host

```sh
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -hda ./qcow2/ubuntu_vm.qcow2 \
  -netdev user,id=net0,hostfwd=udp::1234-:1234,hostfwd=udp::1235-:1235,hostfwd=udp::3000-:3000,hostfwd=udp::3001-:3001 \
  -device e1000,netdev=net0 \
  -monitor telnet:127.0.0.1:4444,server,nowait
```

using cache

```sh
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -drive file=./qcow2/ubuntu_vm.qcow2,if=virtio,cache=writeback \
  -netdev user,id=net0,hostfwd=udp::1234-:1234,hostfwd=udp::1235-:1235,hostfwd=udp::3000-:3000,hostfwd=udp::3001-:3001 \
  -device e1000,netdev=net0 \
  -monitor telnet:127.0.0.1:4444,server,nowait
```

#### savevm
telnet (4444 port) connection
```
telnet 127.0.0.1 4444
```

save vm command
```
(qemu) savevm snapshot-fuzzing
```

check info snapshots
```
(qemu) info snapshots
```

delete snapshot
```
(qemu) delvm snapshot-fuzzing
```


### 2. Modified cFS install into the QEMU VM
```sh
git clone https://github.com/junfuture1103/cFS
cd cFS
./vm-setup.sh
```

vm-setup.sh
```
# git clone https://github.com/nasa/cFS.git
# cd cFS
git checkout origin/msg-flow-log

git submodule init
git submodule update

cp cfe/cmake/Makefile.sample Makefile
cp -r cfe/cmake/sample_defs sample_defs

make SIMULATION=native prep
make
make install
cd build/exe/cpu1/
```

start cFS
```
sudo ./core-cpu1 2>&1 | tee >(nc -u 10.0.2.2 3001)
```

### 3. Start Original Hex Packet Receiver (Have to be execute VM first)
```sh
python3 get_cFS_msg_hex.py
```

### 4. Start Getting stdout of the VM cFS (Have to execute VM first)
```sh
./get_cFS_stdout.sh
```
```sh
# get_cFS_stdout.sh
#!/bin/bash

# In guest -> Use below .sh command
# sudo ./core-cpu1 2>&1 | tee /dev/tty | nc -u 10.0.2.2 3001

# PORT == 3001 Two have to be same

# 현재 날짜/시간을 로그 파일 이름에 반영 (예: 2025-01-06_150150)
DATESTR=$(date +%Y-%m-%d_%H%M%S)

# 로그 디렉터리 및 파일명 설정
LOGDIR="./logs"
mkdir -p "${LOGDIR}"
LOGFILE="${LOGDIR}/stdout_${DATESTR}.log"

PORT=3001

# -u: UDP 모드
# -l: 리스너(서버) 모드
# -k: 연결이 끊겨도 종료되지 않고 계속 수신
# tee: 터미널에 출력하면서 동시에 파일에 기록
echo "Logs will be saved to ${LOGFILE}"
echo "Starting Netcat on port ${PORT} ..."

nc -u -l -k "${PORT}" | tee "${LOGFILE}"
```

### 5. Start Mutate & Sending (Have to execute VM first)

async send
```sh
python3 MsgFlowLogging/async_send_recv_snapshot_version.py
```

random testing
```sh
python3 main_auto_execute_for_snapshot.py
```
