import socket

def send_hex_data_to_vm(host, port, hex_data):
    """
    Sends hex data to the specified host and port.
    
    Args:
        host (str): The IP address of the VM.
        port (int): The port number on the VM.
        hex_data (str): Hex data as a string (e.g., "0x18 0x03 0xC0 0x00 0x00 0x19 0x09 0x34").
    """
    # Convert the hex string to bytes
    data_bytes = bytes(int(byte, 16) for byte in hex_data.split())
    
    # Create a socket and send the data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print(f"Sending data to {host}:{port}: {data_bytes}")
        sock.sendall(data_bytes)
        print("Data sent successfully!")

# Define the VM's host and port
vm_host = "127.0.0.1"  # Replace with the VM's IP address
vm_port = 1234

# Hex data to send
hex_data = "0x18 0x03 0xC0 0x00 0x00 0x19 0x09 0x34"

# Send the data
send_hex_data_to_vm(vm_host, vm_port, hex_data)
