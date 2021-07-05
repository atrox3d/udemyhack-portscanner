import os
import sys
import socket
import threading
import logging
from IPy import IP

logging.basicConfig(level=logging.NOTSET, format="")
rootlogger = logging.getLogger()


def check_ip(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)


def get_banner(sock: socket.socket):
    return sock.recv(1024)


def get_basic_logger(name):
    logging.basicConfig(level=logging.NOTSET)
    return logging.getLogger(name)


def scan_port(ip, port, timeout=0.5, logger=rootlogger):
    try:
        port = int(port)
        sock = socket.socket()
        sock.settimeout(timeout)
        # print(f"CONNECT| {ip}:{port} | {sock.gettimeout()=}")
        sock.connect((ip, port))
        # print(f"CONNECT| {ip}:{port}| OK")
        pad = 15
        try:
            banner = get_banner(sock)
            logger.info(f'[+] Open Port {ip:{pad}} {port}: {str(banner.decode().strip())}.')
        except:
            logger.info(f'[+] Open Port {ip:{pad}} {port}.')
    except Exception as e:
        # print(f"CONNECT| {ip}:{port}| FAIL")
        # print(f"CONNECT| {repr(e)}")
        pass


def scan_ports(converted_ip, ports, timeout, threaded=True, logger=rootlogger):
    if threaded:
        print(f"[+] starting port threads for {converted_ip} {ports}")
        threads = []
        for port in ports:
            th = threading.Thread(
                target=scan_port,
                name=f"scan_port {converted_ip:{15}} {port}",
                args=(converted_ip, port, timeout),
                kwargs=dict(logger=logger)
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
            scan_port(converted_ip, port, timeout, logger=logger)


def scan_target(target, start=1, end=100, timeout=0.5, port_threading=True, logdir="logs"):
    # logging.basicConfig(level=logging.NOTSET, format="")
    logger = logging.getLogger(target)

    logfile = os.path.join("logs", f"{target}.log")
    filehandler = logging.FileHandler(logfile, mode="w")
    logger.addHandler(filehandler)

    # stderrhandler = logging.StreamHandler(sys.stderr)
    # stderrhandler = logging.StreamHandler()
    # logger.addHandler(stderrhandler)

    print(f"{logger.name=}")
    logger.info(f"{socket.getdefaulttimeout()=}")

    try:
        converted_ip = check_ip(target)
    except Exception as e:
        logger.error(f"[-] invalid address/domain: {target}")
        return False
    ports = range(start, end + 1)

    logger.info(f"[+] Target    : {target}")
    logger.info(f"[+] Target ip : {converted_ip}")
    logger.info(f"[+] Port range: {start}-{end}")
    logger.info(f"[+] timeout   : {timeout}")

    scan_ports(converted_ip, ports, timeout, port_threading, logger=logger)
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
            # logfile = open(os.path.join("logs", f"{target}.log"), "w")
            # portscanner.print = print_to_file_decorator(logfile)
            scan_target(target, **kwargs)


if __name__ == '__main__':

    if not len(sys.argv) > 1:
        targets = input('[+] Enter target/s to scan (split multiple targets with space): ')
    else:
        targets = "".join(sys.argv[1:])

    if ' ' in targets:
        for target in targets.split(' '):
            scan_target(target.strip(), port_threading=False)
    else:
        # print(targets)
        scan_target(targets.strip(), port_threading=False)
