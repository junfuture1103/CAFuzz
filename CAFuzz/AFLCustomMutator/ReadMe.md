build custom mutator
```
cc -O3 -shared -fPIC -o cFS_send_udp.so -I /AFLplusplus/include cFS_send_udp_custom_mutator.c
```

Instrumentation cFS
```
export CC=/AFLplusplus/afl-gcc-fast
export CXX=/AFLplusplus/afl-gcc-fast++

make SIMULATION=native prep
make
make install

sudo afl-fuzz -i in -o out -s 123 -t 1000 ./core-cpu1 @@
```


start AFL++
```
# in the cFS directory
AFL_CUSTOM_MUTATOR_LIBRARY=/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/AFLCustomMutator/cFS_send_udp.so AFL_CUSTOM_MUTATOR_LATE_SEND=1 CUSTOM_SEND_READ=1 AFL_DEBUG=1 CUSTOM_SEND_IP=127.0.0.1 CUSTOM_SEND_PORT=1234 \
/AFLplusplus/afl-fuzz -i in -o out -t 4000 -- ./core-cpu1
```

(20241101) You have to start CAFuzz/StateAware/MsgFlowLogging/msg_flow_recv.py
if you have a socket connect error in port 3000, then every input by AFL++ be TIMEOUT!

custom mutator "must" have cFS terminate command after send FUZZ input
```C
    // cFS terminate command
    const char modified_buffer[10] = {0x18, 0x06, 0xc0, 0x00, 0x00, 0x03, 0x02, 0x22, 0x02, 0x00};
    send_file_data(modified_buffer, 10, "127.0.0.1", 1234);
```
