import sys
import getopt
import socket
from IPy import IP


def check_ip(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)


def scan_port(ip, port):
    try:
        port = int(port)
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ip, port))
        print(f'[+] Port {port} is open.')
    except Exception as e:
        print(f'[-] Port {port} is closed, reason: {repr(e)}')


if not len(sys.argv) > 1:
    ipaddress = input('[+] Enter target to scan: ')
else:
    ipaddress = sys.argv[1]

converted_ip = check_ip(ipaddress)

# port = 80
# port = int(input('[+] Enter port to scan:'))
ports = range(75, 85)

print(f"[+] Target ip : {converted_ip}")
print(f"[+] Port range: {ports}")

for port in ports:
    # print(f"[+] scanning {ip}:{port}")
    scan_port(converted_ip, port)
