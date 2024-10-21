import socket
import struct
import logging
from datetime import datetime

def main():
    host = '127.0.0.1'
    port = 3000

    msg_count = 0
    new_ground_command = 0

    # 현재 날짜와 시간을 기반으로 로그 파일 이름 생성
    log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_log.txt')
    path = "./logs/"+log_filename
    # 로깅 설정: 파일과 콘솔에 동시에 출력
    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        handlers=[
                            logging.FileHandler(path, encoding='utf-8'),
                            logging.StreamHandler()
                        ])

    # 소켓 객체 생성
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 포트에 바인딩
    serversocket.bind((host, port))

    # 클라이언트의 접속을 기다림
    serversocket.listen(5)
    logging.info(f"Server listening on {host}:{port}")

    while True:
        # 연결 수락
        clientsocket, addr = serversocket.accept()
        logging.info(f"Got a connection from {addr}")

        try:
            # MsgSize 수신 (4바이트)
            raw_size = clientsocket.recv(4)
            if len(raw_size) < 4:
                logging.info("Failed to receive MsgSize")
                clientsocket.close()
                continue

            # MsgSize 언패킹
            MsgSize = struct.unpack('!I', raw_size)[0]
            logging.info(f"Received MsgSize: {MsgSize}")

            # 메시지 데이터 수신
            data = b''
            while len(data) < MsgSize:
                packet = clientsocket.recv(MsgSize - len(data))
                if not packet:
                    break
                data += packet

            if len(data) < MsgSize:
                logging.info("Failed to receive complete message data")
                clientsocket.close()
                continue

            # 원하는 형식으로 데이터 로깅
            logging.info("Received Data:")
            for i in range(0, len(data), 8):
                line_data = data[i:i+8]
                hex_line = ' '.join(f"0x{byte:02X}" for byte in line_data)
                logging.info(hex_line)

            logging.info(hex(data[0]))

            if new_ground_command == 1:
                logging.info("\n========== Ground Command Was ==========\n")
                new_ground_command = 0

            if data[0] == 0xAA:
                logging.info("======START INGEST PACKET PROCESS ======")
                msg_count += 1
                new_ground_command = 1
                

            # if data[0] == 0xFF:
            #     logging.info("======ENDINGEST PACKET PROCESS ======")
                    
        finally:
            clientsocket.close()
            logging.info("Connection closed msg count = ${}\n\n".format(msg_count))

if __name__ == "__main__":
    main()
