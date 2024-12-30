import telnetlib
import time
import os

def send_cmd(tn, cmd):
    """
    QEMU 모니터 명령어를 실행하고 결과를 반환.
    """
    tn.write(cmd.encode('utf-8') + b'\n')
    return tn.read_until(b"(qemu) ").decode('utf-8')

def send_file_to_vm(file_path, vm_script):
    """
    호스트에서 VM으로 파일을 전달하고 VM 내부에서 스크립트 실행.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # QEMU 내부 실행 명령어 구성 (예: 파일 복사 후 스크립트 실행)
    vm_command = f"guest-exec --path=/usr/bin/python3 --arg={vm_script} --arg={file_path}"
    return vm_command

def fuzz_test(tn, snapshot_name, file_path, vm_script):
    """
    특정 스냅샷을 로드하고 파일을 전달하여 Fuzzing 작업 실행.
    """
    # 스냅샷 로드
    print(f"Loading snapshot: {snapshot_name}")
    load_result = send_cmd(tn, f"loadvm {snapshot_name}")
    print(f"Snapshot Load Result:\n{load_result}")

    # 파일 전달 및 Fuzzing 실행
    vm_command = send_file_to_vm(file_path, vm_script)
    print(f"Executing in VM: {vm_command}")
    execute_result = send_cmd(tn, vm_command)
    print(f"Execution Result:\n{execute_result}")

def main():
    HOST = "127.0.0.1"
    PORT = 4444

    # Fuzzing 테스트 파일 경로와 VM 내부 실행할 스크립트 경로
    test_file = "./fuzz_input.txt"
    vm_script = "/home/cfs-snapshot/jun/CAFuzz/CAFuzz/main.py"

    # Telnet 연결
    tn = telnetlib.Telnet(HOST, PORT)

    # 모니터 초기 프롬프트 수신
    output = tn.read_until(b"(qemu) ")
    print("Initial Monitor Output:\n", output.decode())

    # 스냅샷 목록 확인
    snaps = send_cmd(tn, "info snapshots")
    print("Snapshots:\n", snaps)

    # Fuzzing 테스트 반복 실행
    snapshots = ["snapshot-agent"]
    for i in range(10):  # 예: 10회 반복
        print(f"\n--- Fuzzing Iteration {i + 1} ---")
        for snapshot in snapshots:
            fuzz_test(tn, snapshot, test_file, vm_script)

    # Telnet 연결 종료
    tn.close()

if __name__ == "__main__":
    main()
