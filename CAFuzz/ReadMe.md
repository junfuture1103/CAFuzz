# Overview

본 자료는 cFS GroundStation의 SendPacket을 분리해낸 자료입니다.
cFS Packet 구조에 맞게 패킷을 자동으로 전송할 수 있습니다.

이를 활용해 command-aware fuzzing을 할 수 있습니다.


[cFS SendPacket Code-level Structure](https://www.figma.com/design/kuDif3l4WQJSQMEiSyHNuX/cFS-SendPacket-Analysis?node-id=0-1&t=LWIzHor5SrPntLuC-1)에서 cFS SendPacket 함수의 동작 순서와 구조를 확인할 수 있습니다.

Quick start cFS fuzzing using AFL++
```
AFL_CUSTOM_MUTATOR_LIBRARY=/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/AFLCustomMutator/cFS_send_udp.so AFL_CUSTOM_MUTATOR_LATE_SEND=1 CUSTOM_SEND_READ=1 AFL_DEBUG=1 CUSTOM_SEND_IP=127.0.0.1 CUSTOM_SEND_PORT=1234 \
/AFLplusplus/afl-fuzz -i in -o out -t 4000 -- ./core-cpu1
```