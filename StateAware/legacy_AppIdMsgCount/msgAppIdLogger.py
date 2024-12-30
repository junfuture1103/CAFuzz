import re
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime

CIRCLE_SIZE = 10

# 로그 파일 읽기 함수
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# 로그 데이터 파싱 함수
def parse_log(log_data):
    pattern = re.compile(r"(\d{4}-\d{3}-\d{2}:\d{2}:\d{2}\.\d{5}) .*StreamId\[0\]=0x(\w+), StreamId\[1\]=0x(\w+), msgidval=0x(\w+)")
    matches = pattern.findall(log_data)

    data = []
    for match in matches:
        time_str = match[0]
        timestamp = datetime.strptime(time_str, "%Y-%j-%H:%M:%S.%f")
        stream_id1 = match[1]
        stream_id2 = match[2]
        msg_id = match[3]
        data.append([timestamp, stream_id1, stream_id2, msg_id])
    
    return pd.DataFrame(data, columns=['Timestamp', 'StreamId1', 'StreamId2', 'MsgId'])

# 파일 경로 설정
log_file_path = 'msgAppIdLogDatasets/log_file1.txt'

# 로그 파일 읽기
log_data = read_log_file(log_file_path)

# 로그 데이터 프레임 생성
df = parse_log(log_data)

# AppID는 MsgId로 정의
df['AppID'] = df['MsgId']

# AppID별 메시지 수 카운팅
df_count = df['AppID'].value_counts()

# 네트워크 그래프 생성
G = nx.Graph()

# 모듈(AppID)을 노드로 추가하고 메시지 수에 따라 크기 조정
for app_id, count in df_count.items():
    G.add_node(app_id, size=count * 100)  # 크기 조정: 곱을 늘려서 더 크게 설정

# 네트워크 레이아웃 설정 (원형 레이아웃)
pos = nx.spring_layout(G, seed=42)

# 네트워크 그래프 그리기
plt.figure(figsize=(10, 10))

# 노드 크기 설정 (메시지 수에 따라 크기)
node_sizes = [G.nodes[node]['size']*CIRCLE_SIZE for node in G.nodes]

# 네트워크 그래프 그리기
nx.draw(G, pos, with_labels=False, node_size=node_sizes, node_color='skyblue', alpha=0.8, font_size=12)

# 노드 안에 메시지 수(count)를 라벨로 추가
labels = {app_id: f'{app_id}\n{count}' for app_id, count in df_count.items()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=12, font_color='black')

# 제목 설정
plt.title('Message Count per AppID (Size and Labels represent the number of messages)', fontsize=15)
plt.show()
