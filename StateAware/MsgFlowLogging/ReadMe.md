### async_send_recv.py

- 1~100 번의 반복 횟수를 정해서 랜덤 command를 전송 (랜덤 command 생성시 `CAFuzz/main.py` 이용)
- 이때 command msg의 처리가 완전히 끝난 후 다음 로직을 처리할 수 있게 보장하기 위해 1235 포트로 응답이 오면 다음 패킷을 전송함. 만약에 1초 이후에도 1235로 recv가 없는 경우 → 그냥 다시 보내줌 (timout : 1sec)
- 1~100번의 반복횟수가 완료되면 cFS를 kill. ⇒ ./testing.sh를 이용해서 cFS가 죽으면 자동으로 되살아나게 함. 되살아날때까지 기다린 후 되살아 나면 이후 전송 루틴 진행.

### msg_flow_recv_logfile_seperation.py
- logging cFS SB Msg Queue
- Every Msg Flow is recorded by this module.
- logs are appropriatly seperated & save in logs/