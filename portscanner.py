import os
import sys
import socket
import threading
import logging

from IPy import IP

logging.basicConfig(level=logging.NOTSET, format="")
rootlogger = logging.getLogger()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")


def check_ip(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)


def get_banner(sock: socket.socket):
    return sock.recv(1024)


def decode_banner(banner):
    # converted = str(banner, 'ascii')
    converted = banner.decode()
    return converted


def clean_banner(text_banner):
    text_banner = ''.join([c for c in text_banner if c.isprintable()])
    return text_banner


def scan_port(ip, port, timeout=0.5, logger=rootlogger):
    try:
        port = int(port)
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))
        ip_padding = 15
        port_padding = 5
        try:
            banner = get_banner(sock)
            text_banner = decode_banner(banner)

            decode_warning = False
            if not all(map(str.isprintable, text_banner)):
                text_banner = clean_banner(text_banner)
                decode_warning = True
            if not all(map(str.isprintable, text_banner)):
                logger.critical(
                    "[!] found non-printable inside banner, "
                    "cannot fix, EXITING")
                return
            if decode_warning:
                logger.info(
                    f'[+] Open Port {ip:{ip_padding}} {port:>{port_padding}}: '
                    f'banner (binary)       : *b{{{text_banner}}}.'
                )
            else:
                logger.info(
                    f'[+] Open Port {ip:{ip_padding}} {port:>{port_padding}}: '
                    f'banner (text)         : *t[{text_banner}].'
                )
        except (
                socket.timeout,
                ConnectionError,
                ConnectionResetError,
                ConnectionAbortedError,
                ConnectionRefusedError,
        ):
            logger.info(
                f'[+] Open Port {ip:{ip_padding}} {port:>{port_padding}}. '
            )
        except Exception as e:
            logger.info(
                f'[+] Open Port {ip:{ip_padding}} {port:>{port_padding}}: '
                f'error receiving banner: {type(e)} "{e}".'
            )
    except Exception as e:
        # port closed
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
            th.join()
    else:
        for port in ports:
            scan_port(converted_ip, port, timeout, logger=logger)


def scan_target(target, start=1, end=100, timeout=0.5, port_threading=True, logdir=LOG_DIR):
    logger = logging.getLogger(target)

    logfile = os.path.join(logdir, f"{target}.log")
    filehandler = logging.FileHandler(logfile, mode="w")
    logger.addHandler(filehandler)

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
        scan_target(targets.strip(), port_threading=False)
