# using .qcow2 to make snapshot

# qemu-system-x86_64 \                                 
#   -enable-kvm \
#   -m 4096 \
#   -hda ./qcow2/ubuntu_vm.qcow2 \
#   -net nic \                                                
#   -net user,hostfwd=udp::1234-:1234 \
#   -monitor telnet:127.0.0.1:4444,server,nowait

# qemu-system-x86_64 \
#   -enable-kvm \
#   -m 4096 \
#   -hda ./qcow2/ubuntu_vm.qcow2 \
#   -netdev user,id=net0,hostfwd=udp::1234-:1234,hostfwd=udp::1235-:1235,hostfwd=udp::3000-:3000 \
#   -device e1000,netdev=net0 \
#   -monitor telnet:127.0.0.1:4444,server,nowait

# cFS build -> execute -> savevm