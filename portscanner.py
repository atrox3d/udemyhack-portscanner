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
        # print(f'[-] Port {port} is closed, reason: {repr(e)}')
        pass

def scan(target):
    converted_ip = check_ip(target)
    ports = range(1, 100)

    print(f"[+] Target    : {target}")
    print(f"[+] Target ip : {converted_ip}")
    print(f"[+] Port range: {ports}")

    for port in ports:
        scan_port(converted_ip, port)


if not len(sys.argv) > 1:
    targets = input('[+] Enter target/s to scan (split multiple targets with comma): ')
else:
    targets = "".join(sys.argv[1:])

if ',' in targets:
    for target in targets.split(','):
        print(targets)
        scan(target.strip())
else:
    print(targets)
    scan(targets.strip())


