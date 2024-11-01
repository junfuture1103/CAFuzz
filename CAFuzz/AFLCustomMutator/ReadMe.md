### cFS_send_udp : custom mutator
build custom mutator
```
cc -O3 -shared -fPIC -o cFS_send_udp.so -I /AFLplusplus/include cFS_send_udp_custom_mutator.c
```

Instrumentation cFS
```
# Please use these commands Step-by-Step
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

### cFS_send_udp_command_aware : custom mutator using python command generation
cFS_send_udp_command_aware.so is using python script(../generate_command_not_send.py)command that can generate cFS command-Aware input
```
cc -O3 -shared -fPIC -o cFS_send_udp_command_aware.so -I /AFLplusplus/include cFS_send_udp_command_aware_custom_mutator.c
```

start command
```sh
# in the cFS Directory
sudo AFL_CUSTOM_MUTATOR_LIBRARY=/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/AFLCustomMutator/cFS_send_udp_command_aware.so AFL_CUSTOM_MUTATOR_LATE_SEND=1 CUSTOM_SEND_READ=1 AFL_DEBUG=1 CUSTOM_SEND_IP=127.0.0.1 CUSTOM_SEND_PORT=1234 \
/AFLplusplus/afl-fuzz -i in -o out -t 4000 -- ./core-cpu1

or you can use :
./testing.sh
```

When you use ./testing.sh, you can auto-restart if there is no meaningful input(We can't instrumentation yet!)
Here is the Code : 
```sh
#!/bin/bash

# infinite loop that restart Fuzzer whenever it die
while true; do
    echo "Starting AFL fuzzing process..."

    # execute command
    sudo AFL_CUSTOM_MUTATOR_LIBRARY=/home/jun20/jun/kaist_research/CAFuzz/CAFuzz/AFLCustomMutator/cFS_send_udp_command_aware.so \
    AFL_CUSTOM_MUTATOR_LATE_SEND=1 \
    CUSTOM_SEND_READ=1 \
    AFL_DEBUG=1 \
    CUSTOM_SEND_IP=127.0.0.1 \
    CUSTOM_SEND_PORT=1234 \
    /AFLplusplus/afl-fuzz -i in -o out -t 4000 -- ./core-cpu1

    # When fuzzer die, print error msg & just re-start
    echo "AFL fuzzing process terminated. Restarting in 5 seconds..."
    sleep 5
done
```


## Warning!
(20241101) You have to start CAFuzz/StateAware/MsgFlowLogging/msg_flow_recv.py
if you have a socket connect error in port 3000, then every input by AFL++ be TIMEOUT!

custom mutator "must" have cFS terminate command after send FUZZ input
```C
    // cFS terminate command
    const char modified_buffer[10] = {0x18, 0x06, 0xc0, 0x00, 0x00, 0x03, 0x02, 0x22, 0x02, 0x00};
    send_file_data(modified_buffer, 10, "127.0.0.1", 1234);
```
