# 1. QEMU VM start
start the vm using .qcow2 file (if you don't have it, make it first)
```sh
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -hda ./qcow2/ubuntu_vm.qcow2 \
  -netdev user,id=net0,hostfwd=udp::1234-:1234,hostfwd=udp::1235-:1235,hostfwd=udp::3000-:3000,hostfwd=udp::3001-:3001 \
  -device e1000,netdev=net0 \
  -monitor telnet:127.0.0.1:4444,server,nowait
```
savevm
```
TBD
```


# 2. Modified cFS install into the QEMU VM
```sh
git clone https://github.com/junfuture1103/cFS
cd cFS
./vm-setup.sh
```

# 3. Start Original Hex Packet Receiver (Have to be execute VM first)
```python
python3 MsgFlowLogging/msg_flow_recv_logfile_seperation.py
```

# 4. Start Getting stdout of the VM cFS (Have to execute VM first)
```
./get_cFS_stdout.sh
```

# 5. Start Mutate & Sending (Have to execute VM first)
```python
python3 MsgFlowLogging/async_send_recv_snapshot_version.py
```
