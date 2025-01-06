# 1. qcow2 디스크 이미지 생성
VM용 디스크 이미지를 qcow2 포맷으로 만든다.

``` bash
qemu-img create -f qcow2 ubuntu_vm.qcow2 20G
```

<br>

# 2. QEMU로 VM 실행
아래 예시는 ISO 파일로부터 설치를 진행하는 가상의 Ubuntu VM 실행 예시다.

### Initial Start & ReStart

```
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -hda ubuntu_vm.qcow2 \
  -cdrom ubuntu-20.04.iso \
  -boot d
```
설치가 끝나면 CD-ROM 관련 옵션(-cdrom, -boot d)을 제거하고, qcow2 파일만으로 부팅하도록 한다.

```
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -hda ubuntu_vm.qcow2
```

### Monitor Mode (telnet)
Most frequently Use
```
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -hda ./qcow2/ubuntu_vm.qcow2 \
  -monitor telnet:127.0.0.1:4444,server,nowait
```

Monitor Mode (socket)
```
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -hda ./qcow2/ubuntu_vm.qcow2 \
  -monitor unix:/tmp/qemu-mon_${VMNAME}.sock,server,nowait
```

### udp packet to guest
success!!(12.30)

```
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -hda ./qcow2/ubuntu_vm.qcow2 \
  -net nic \
  -net user,hostfwd=udp::1234-:1234 \
  -monitor telnet:127.0.0.1:4444,server,nowait
```

<br>

# * Snapshot Setting

### dependencies

```
sudo apt install git
sudo apt install make
sudo apt install cmake
sudo apt install python3-pip
```

### cFS setting

using the revised version of the cFS for CAFuzz Testing : 
https://github.com/junfuture1103/cFS

check the readme : 
https://github.com/junfuture1103/cFS


# port-forwarding
portforwarding for python script & input send


<br>

# 3. 스냅샷 생성 (savevm)
QEMU Monitor(기본적으로 Ctrl+Alt+2 혹은 Ctrl+Alt+Shift+2 단축키로 접근 가능)에서 다음 명령을 통해 현재 VM 상태를 스냅샷으로 저장한다:

```scss
(qemu) savevm snapshot1
```
snapshot1은 스냅샷 식별을 위한 임의의 이름이다.
필요한 시점마다 savevm snapshot2, savevm snapshot3 등 여러 개 저장 가능하다.
저장된 스냅샷 목록은 QEMU Monitor에서 다음 명령으로 확인한다:

```
(qemu) info snapshots
```
<br>

# 4. 스냅샷 되돌리기 (loadvm)
QEMU Monitor에서 다음 명령어로 특정 시점의 스냅샷으로 되돌린다:
```
(qemu) loadvm snapshot1
```

VM 상태가 해당 스냅샷이 찍혔던 시점으로 즉시 복원된다.

# Usage
1. qemu open
```
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -hda ./qcow2/ubuntu_vm.qcow2 \
  -net nic \
  -net user,hostfwd=udp::1234-:1234 \
  -monitor telnet:127.0.0.1:4444,server,nowait
```

2. execute python script

```bash
python3 main_audto_execute_for_snapshot_speed_test.py
```

```python

import subprocess
import time
import random
import os
from datetime import datetime
import telnetlib

snapshot_name = "snapshot-done"

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
```

# STDOUT Log 받는 법

QEMU의 User Networking(-net user 혹은 -netdev user) 모드는 내부적으로 SLiRP라는 가상 네트워킹 스택을 사용한다. 이때 SLiRP에서 정한 디폴트 라우터(게스트가 바라보는 게이트웨이) 주소가 10.0.2.2로 지정되어 있다. 즉, 게스트 측에서 보았을 때

게스트 IP: 10.0.2.15 (기본값)
게이트웨이(Gateway): 10.0.2.2
DNS 서버: 10.0.2.3
와 같은 식으로 미리 설정된 주소 할당 규칙을 따른다.

SLiRP는 원래 과거에 다이얼업(dial-up) 환경 등에서 “유저 공간”에서 동작하는 TCP/IP 스택을 제공하기 위해 사용되었는데, QEMU는 이를 응용해 호스트에서 별도의 커널 레벨 브리지 없이도 간단히 가상머신에 NAT 네트워킹을 제공하기 위해 SLiRP를 탑재했다. 그 결과 내부 IP 대역과 라우터 주소가 이렇게 고정된 디폴트를 갖게 된 것이다.

## 사용법

qemu 실행시 반드시 : 
```
qemu-system-x86_64 \
   -enable-kvm \
   -m 4096 \
   -hda ./qcow2/ubuntu_vm.qcow2 \
   -netdev user,id=net0,hostfwd=udp::1234-:1234,hostfwd=udp::1235-:1235,hostfwd=udp::3000-:3000 \
   -device e1000,netdev=net0 \
   -monitor telnet:127.0.0.1:4444,server,nowait
```

게스트에서 : 
```
sudo ./core-cpu1 | nc -u 10.0.2.2 3000
```

호스트에서 : 
```
nc -u -l 3000
```
