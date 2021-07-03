import socket
from IPy import IP

ipaddress = input('[+] Enter target to scan:')
port = int(input('[+] Enter port to scan:'))
# port = 80

try:
    sock = socket.socket()
    sock.connect((ipaddress, port))
    print(f'[+] Port {port} is open.')
except Exception as e:
    print(f'[-] Port {port} is closed.')
    print(f'[-] {repr(e)}')
