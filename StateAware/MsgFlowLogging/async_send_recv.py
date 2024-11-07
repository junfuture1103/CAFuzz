import socket
import select
import time
import random
import subprocess
import os

# cFS Exit
final_message = bytes([0x18, 0x06, 0xc0, 0x00, 0x00, 0x03, 0x02, 0x22, 0x02, 0x00])

# Tlm enable
initial_message = bytes([0x18, 0x80, 0xC0, 0x00, 0x00, 0x11, 0x06, 0x9B, 
                            0x31, 0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 0x2E, 
                            0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

def udp_communication(attempt_num):
    # 설정 부분
    listen_ip = "127.0.0.1"
    listen_port = 1235

    send_port = 1234
    # 0~100 사이의 랜덤 횟수 정하기
    random_attempts = random.randint(0, 100)
    attempt_count = 0

    # core-cpu1 실행 여부 확인 및 실행
    while True:
        try:
            result = subprocess.run(['pgrep', '-f', 'core-cpu1'], stdout=subprocess.PIPE, text=True)
            if not result.stdout:
                print("core-cpu1 is not running. Starting core-cpu1...")
                time.sleep(5)  # 프로세스가 실행될 시간을 주기 위해 2초 대기
            else:
                print("core-cpu1 is running.")
                break
        except subprocess.CalledProcessError:
            print("No core-cpu1 processes found. Waiting core-cpu1...")
            time.sleep(5)  # 프로세스가 실행될 시간을 주기 위해 2초 대기

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_socket.sendto(initial_message, (listen_ip, send_port))
    print(f"Tlm init cFS message sent to port {send_port}")
    send_socket.close()

    while True:
        # 수신 소켓 설정
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_socket.bind((listen_ip, listen_port))

        # 송신 소켓 설정
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 1초 동안 수신 대기
        recv_socket.setblocking(0)
        ready = select.select([recv_socket], [], [], 1)

        if ready[0]:
            # 응답이 오면 바로 1234 포트로 데이터 전송
            data, addr = recv_socket.recvfrom(1024)
            print(f"Received message: {data} from {addr}")
            # send_socket.sendto(message_to_send, (listen_ip, send_port))
            # print(f"Message sent to port {send_port} after timeout")

            result = subprocess.run(['python3', '/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/main.py'], check=True, stderr=subprocess.PIPE, text=True)
        else:
            # 1초 동안 응답이 없으면 자동으로 1234 포트로 데이터 전송
            print("No response received within 1 second.")
            time.sleep(1)  # 1초 대기 후 전송
            # send_socket.sendto(message_to_send, (listen_ip, send_port))
            # print(f"Message sent to port {send_port} after timeout")
            
            result = subprocess.run(['python3', '/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/main.py'], check=True, stderr=subprocess.PIPE, text=True)
        
        attempt_count += 1
        # 랜덤 횟수만큼 반복한 경우 루프 탈출
        if attempt_count >= random_attempts:
            print(f"Reached random attempt count: {random_attempts}. Exiting loop.")
            break

        # 소켓 닫기
        recv_socket.close()
        send_socket.close()

    # 마지막으로 1234 포트에 특정 메시지 전송
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_socket.sendto(final_message, (listen_ip, send_port))
    print(f"exit cFS message sent to port {send_port}")
    send_socket.close()

    print(f"udp_communication attempt {attempt_num} finished. Waiting 5 seconds before next attempt...")
    time.sleep(5)

if __name__ == "__main__":
    attempt_number = 1
    while True:
        print(f"Starting udp_communication attempt number: {attempt_number}")
        
        # Check if core-cpu1 processes are running and kill them
        try:
            result = subprocess.run(['pgrep', '-f', 'core-cpu1'], stdout=subprocess.PIPE, text=True)
            if result.stdout:
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    os.system(f"sudo kill -9 {pid}")
                    print(f"Killed process core-cpu1 with PID: {pid}")
                    print("wait for 5 sec...")
                    time.sleep(5)
        except subprocess.CalledProcessError:
            print("No core-cpu1 processes found running.")
        
        udp_communication(attempt_number)
        attempt_number += 1
