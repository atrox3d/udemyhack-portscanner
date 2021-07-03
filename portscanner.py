import sys
import getopt
import socket
from IPy import IP


def scan_port(ipaddress, port):
    try:
        port = int(port)
        sock = socket.socket()
        sock.connect((ipaddress, port))
        print(f'[+] Port {port} is open.')
    except Exception as e:
        print(f'[-] Port {port} is closed.')
        print(f'[-] {repr(e)}')


if not len(sys.argv) > 1:
    ipaddress = input('[+] Enter target to scan: ')
else:
    ipaddress = sys.argv[1]

# port = 80
# port = int(input('[+] Enter port to scan:'))
ports = range(1, 10)
print(f"[+] Target ip : {ipaddress}")
print(f"[+] Port range: {ports}")
for port in ports:
    print(f"[+] scanning {ipaddress}:{port}")
    scan_port(ipaddress, port)
