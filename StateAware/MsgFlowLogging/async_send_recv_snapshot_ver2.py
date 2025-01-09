import socket
import select
import time
import random
import subprocess
import os
import struct
import telnetlib

# cFS Exit
# final_message = bytes([0x18, 0x06, 0xc0, 0x00, 0x00, 0x03, 0x02, 0x22, 0x02, 0x00])
final_message = bytes([102, 105, 110, 105, 115, 104, 32, 49, 32, 99, 121, 99, 108, 101])

# Tlm enable -> 127.0.0.1 X 10.0.2.2 O (in VM)
# 127.0.0.1
# initial_message = bytes([0x18, 0x80, 0xC0, 0x00, 0x00, 0x11, 0x06, 0x9B, 
#                             0x31, 0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 0x2E, 
#                             0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

# 10.0.2.2
initial_message = bytes([0x18, 0x80, 0xC0, 0x00, 0x00, 0x11, 0x06, 0xaf, 
                            0x31, 0x30, 0x2E, 0x30, 0x2E, 0x32, 0x2E, 
                            0x32, 0x00, 0x00, 0x00, 0x00,  0x00, 0x00, 0x00, 0x00])



# Do not use! Just use send_cFS_exit_pkt
# def kill_process_by_name(name):
#     try:
#         # core-cpu1 이름의 프로세스를 찾아서 종료
#         subprocess.run(["pkill", "-f", name])
#         print(f"Process {name} killed.")
#     except Exception as e:
#         print(f"Failed to kill process {name}: {e}")

def send_tlm_init_pkt(listen_ip = "127.0.0.1", send_port = 1234):
    # Tlm init start
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_socket.sendto(initial_message, (listen_ip, send_port))
    print(f"Tlm init cFS message sent to port {send_port}")
    send_socket.close()

# def send_cFS_exit_pkt(listen_ip = "127.0.0.1", send_port = 3001):
#     # maybe we don't need this!
#     send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     send_socket.sendto(final_message, (listen_ip, send_port))
#     print(f"exit cFS message sent to port {send_port}")
#     send_socket.close()


#     print(f"Loading snapshot: {snapshot_name}")
#     load_result = send_cmd(tn, f"loadvm {snapshot_name}")
#     print(f"Snapshot Load Result:\n{load_result}")
#     # send_cFS_exit_to_msg_flow_recv()

def send_cFS_exit_to_msg_flow_recv():
    host = '127.0.0.1'
    port = 3001

    # 소켓 객체 생성
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 서버에 연결
        clientsocket.connect((host, port))
        
        # 보낼 메시지 데이터 (예: "EXIT"라는 패턴을 포함)
        message = b'\x18\x06\xC0\x00\x00\x03\x02\x22\x02\x00'  # cFS 종료 패킷 패턴
        MsgSize = len(message)
        packed_size = struct.pack('!I', MsgSize)

        # 메시지 전송
        clientsocket.sendall(packed_size)
        clientsocket.sendall(message)

    finally:
        clientsocket.close()

# def start_server(ip, port):
#     # 소켓 생성 및 바인딩
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # SO_REUSEADDR 옵션 설정
#     server_socket.bind((ip, port))
#     server_socket.listen(1)
#     print(f"Listening on {ip}:{port}...")

#     while True:
#         # accept 타임아웃 
#         timeout = 5
#         server_socket.settimeout(timeout)

#         try:
#             conn, addr = server_socket.accept()
#             print(f"Connection established with {addr}")

#             server_socket.settimeout(None)

#             # 메시지 길이 먼저 수신
#             msg_length_data = conn.recv(4)
#             if not msg_length_data:
#                 print("Failed to receive message length.")
#                 conn.close()
#                 continue

#             msg_length = struct.unpack('!I', msg_length_data)[0]
#             print(f"Message length received: {msg_length}")

#             # 실제 메시지 수신
#             message = conn.recv(msg_length).decode()
#             print(f"Message received: {message}")
#             return True
        
#         # cFS already started
#         except socket.timeout:
#             print("No response from cFS within timeout period.")
#             # 타임아웃 발생 시 core-cpu1 프로그램 종료
#             send_cFS_exit_pkt()

#         except Exception as e:
#             print(f"An error occurred: {e}")
#         finally:
#             if 'conn' in locals():
#                 conn.close()
#                 print("Connection closed.")


def udp_communication():
    # 설정 부분
    listen_ip = "127.0.0.1"
    listen_port = 1235

    send_port = 1234
    # 0~100 사이의 랜덤 횟수 정하기
    random_attempts = random.randint(0, 100)
    attempt_count = 0

    # Wait until cFS Operation Start (not just process start)
    # if(start_server(listen_ip, listen_port)):
    #     print("start msg sending routine!!")
    #     send_tlm_init_pkt()


    while True:
        # 수신 소켓 설정
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # SO_REUSEADDR 옵션 활성화 - Ignore : Address already in use 
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        recv_socket.bind((listen_ip, listen_port))

        # 1초 동안 수신 대기
        recv_socket.setblocking(0)
        ready = select.select([recv_socket], [], [], 2)

        if ready[0]:
            # 응답이 오면 바로 1234 포트로 데이터 전송
            print("TLM message recv!")
            data, addr = recv_socket.recvfrom(1024)
            print(f"Received Tlm message: {data} from {addr}")
            result = subprocess.run(['python3', '/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/main.py'], check=True, stderr=subprocess.PIPE, text=True)
        else:
            # 1초 동안 응답이 없으면 자동으로 1234 포트로 데이터 전송
            print("No response received within 5 second.")
            result = subprocess.run(['python3', '/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/main.py'], check=True, stderr=subprocess.PIPE, text=True)
   
        attempt_count += 1
        
        print("attempt_count : ", attempt_count)

        # 랜덤 횟수만큼 반복한 경우 루프 탈출
        if attempt_count >= random_attempts:
            print(f"Reached random attempt count: {random_attempts}. Exiting loop.")
            break

        # 소켓 닫기
        recv_socket.close()

    # 마지막으로 1234 포트에 특정 메시지 전송
    send_cFS_exit_to_msg_flow_recv()

    print(f"udp_communication attempt {attempt_count} finished. Waiting next attempt...")

def send_cmd(tn, cmd):
    """
    QEMU 모니터 명령어를 실행하고 결과를 반환.
    """
    tn.write(cmd.encode('utf-8') + b'\n')
    return tn.read_until(b"(qemu) ").decode('utf-8')

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

    # Fuzzing 테스트 반복 실행
    snapshot_name = "snapshot-fuzzing-cFS"

    attempt_number = 1

    while True:
        # re-load the snapshot after 1 test cycle
        print(f"Loading snapshot: {snapshot_name}")
        load_result = send_cmd(tn, f"loadvm {snapshot_name}")
        print(f"Snapshot Load Result:\n{load_result}")

        send_tlm_init_pkt()
        udp_communication()
