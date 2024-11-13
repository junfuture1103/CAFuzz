import socket

# 대상 IP와 포트 설정
target_ip = "127.0.0.1"
target_port = 1234

# 헥스 문자열을 입력으로 받아 바이트 배열로 변환하는 함수
def parse_hex_string(hex_string):
    hex_values = hex_string.split()  # 공백으로 각 헥스 값을 분리
    return bytes(int(value, 16) for value in hex_values)  # 각 값을 16진수로 변환하여 바이트 배열 생성

# 사용자로부터 헥스 문자열 입력
hex_string = "18 09 C0 00 00 01 00 00"  # 예시로 들어가는 문자열
hex_data = parse_hex_string(hex_string)  # 헥스 문자열을 바이트 배열로 변환

# 소켓 생성 및 데이터 전송
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    udp_socket.sendto(hex_data, (target_ip, target_port))

print("데이터가 전송되었습니다.")
