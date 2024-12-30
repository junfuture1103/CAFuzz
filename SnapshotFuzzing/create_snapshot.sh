# using .qcow2 to make snapshot

# qemu-system-x86_64 \                                 
#   -enable-kvm \
#   -m 4096 \
#   -hda ./qcow2/ubuntu_vm.qcow2 \
#   -net nic \                                                
#   -net user,hostfwd=udp::1234-:1234 \
#   -monitor telnet:127.0.0.1:4444,server,nowait

# cFS build -> execute -> savevm