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