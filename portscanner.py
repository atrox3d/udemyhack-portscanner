import os
import sys
import socket
import threading
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
        pad = 15
        try:
            banner = get_banner(sock)
            print(f'[+] Open Port {ip:{pad}} {port}: {str(banner.decode().strip())}.')
        except:
            print(f'[+] Open Port {ip:{pad}} {port}.')
    except Exception as e:
        # print(f'[-] Port {port} is closed, reason: {repr(e)}')
        pass


def scan_ports(converted_ip, ports, timeout, threaded=True):
    if threaded:
        print(f"[+] starting port threads for {converted_ip} {ports}")
        threads = []
        for port in ports:
            th = threading.Thread(
                target=scan_port,
                name=f"scan_port {converted_ip:{15}} {port}",
                args=(converted_ip, port, timeout),
            )
            # print(f"[+] starting thread {th.getName()}")
            th.start()
            threads.append(th)

        print(f"[+] waiting port threads for {converted_ip}:{ports}")
        for th in threads:
            # print(f"[+] joining thread {th.getName()}")
            th.join()
    else:
        for port in ports:
            scan_port(converted_ip, port, timeout)


def scan_target(target, start=1, end=100, timeout=0.5, threaded=True):
    try:
        converted_ip = check_ip(target)
    except Exception as e:
        print(f"[-] invalid address/domain: {target}")
        return False
    ports = range(start, end + 1)

    print(f"[+] Target    : {target}")
    print(f"[+] Target ip : {converted_ip}")
    print(f"[+] Port range: {start}-{end}")
    print(f"[+] timeout   : {timeout}")

    scan_ports(converted_ip, ports, timeout, threaded)
    return True


def scan_targets(*targets, start, end, timeout, target_threading, port_threading):
    kwargs = dict(
        start=start,
        end=end,
        timeout=timeout,
        threaded=port_threading
    )

    if target_threading:
        threads = []

        for target in targets:
            th = threading.Thread(
                target=scan_target,
                name=target,
                args=(target,),
                kwargs=kwargs
            )
            print(f"[+] starting thread {th.getName()}")
            th.start()
            threads.append(th)

        for th in threads:
            print(f"[+] joining target thread {th.getName()}")
            th.join()
        print(f"[+] waiting for target threads")
    else:
        for target in targets:
            logfile = open(os.path.join("logs", f"{target}.log"), "w")
            # portscanner.print = print_to_file_decorator(logfile)
            scan_target(target, **kwargs)


if __name__ == '__main__':

    if not len(sys.argv) > 1:
        targets = input('[+] Enter target/s to scan (split multiple targets with comma): ')
    else:
        targets = "".join(sys.argv[1:])

    if ',' in targets:
        for target in targets.split(','):
            # print(targets)
            scan_target(target.strip())
    else:
        # print(targets)
        scan_target(targets.strip())
