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


def get_banner(sock: socket.socket):
    return sock.recv(1024)


def scan_port(ip, port, timeout=0.5):
    try:
        port = int(port)
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))
        try:
            banner = get_banner(sock)
            print(f'[+] Open Port {port}: {str(banner.decode().strip())}.')
        except:
            print(f'[+] Open Port {port}.')
    except Exception as e:
        # print(f'[-] Port {port} is closed, reason: {repr(e)}')
        pass


def scan(target, start=1, end=100, timeout=0.5):
    converted_ip = check_ip(target)
    ports = range(start, end)

    print(f"[+] Target    : {target}")
    print(f"[+] Target ip : {converted_ip}")
    print(f"[+] Port range: {ports}")

    for port in ports:
        scan_port(converted_ip, port)


if __name__ == '__main__':

    if not len(sys.argv) > 1:
        targets = input('[+] Enter target/s to scan (split multiple targets with comma): ')
    else:
        targets = "".join(sys.argv[1:])

    if ',' in targets:
        for target in targets.split(','):
            # print(targets)
            scan(target.strip())
    else:
        # print(targets)
        scan(targets.strip())
