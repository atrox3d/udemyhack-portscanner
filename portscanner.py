import os
import sys
import socket
import threading
import logging
import time

from IPy import IP
import termcolor
import colorama
colorama.init()

logging.basicConfig(level=logging.NOTSET, format="")
rootlogger = logging.getLogger()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")


def check_ip(ip):
    """check ip address or hostname, returns ipaddress on success"""
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)


def get_banner(sock: socket.socket):
    """reads the first 1024 bytes from socket"""
    return sock.recv(1024)


def decode_banner(bytebanner):
    """decode first 1024 bytes to string"""
    # converted = str(banner, 'ascii')
    converted = bytebanner.decode()
    return converted


def clean_banner(text_banner):
    """try to remove non printable chars from banner"""
    text_banner = ''.join([c for c in text_banner if c.isprintable()])
    return text_banner


def scan_port(ip, port, timeout=0.5, logger=rootlogger):
    """scans selected port from ip and tries to extract banner"""
    ip_padding = 15
    port_padding = 5

    # try to connect
    try:
        port = int(port)
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))

        # try to extract banner
        try:
            banner = get_banner(sock)
            text_banner = decode_banner(banner)

            decode_warning = False
            if not all(map(str.isprintable, text_banner)):
                # found non printable chars
                text_banner = clean_banner(text_banner)
                decode_warning = True

            if not all(map(str.isprintable, text_banner)):
                # found AGAIN non printable chars
                logger.critical(
                    "[!] found non-printable inside banner, "
                    "cannot fix, EXITING")
                return

            if decode_warning:
                # assume the banner is not normal text
                print(
                    termcolor.colored(
                        f'[+] Open Port {ip:{ip_padding}} {port:>{port_padding}}: '
                        f'banner (binary)       : *b{{{text_banner}}}.'
                        'yellow'
                    )
                )
                logger.info(
                    f'[+] Open Port {ip:{ip_padding}} {port:>{port_padding}}: '
                    f'banner (binary)       : *b{{{text_banner}}}.'
                )
            else:
                print(
                    termcolor.colored(
                        f'[+] Open Port {ip:{ip_padding}} {port:>{port_padding}}: '
                        f'banner (text)         : *t[{text_banner}].',
                        'green'
                    )
                )
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
            print(
                termcolor.colored(
                    f'[+] XOpen Port {ip:{ip_padding}} {port:>{port_padding}}. ',
                    'green'
                )
            )
            logger.info(
                termcolor.colored(
                    f'[+] XOpen Port {ip:{ip_padding}} {port:>{port_padding}}. '
                )
            )
        except Exception as e:
            # unknown error receving banner
            logger.info(
                f'[+] Open Port {ip:{ip_padding}} {port:>{port_padding}}: '
                f'error receiving banner: {type(e)} "{e}".'
            )
    except KeyboardInterrupt:
        print(f"CRTL-C: exit scanport {ip}:{port}")
        raise KeyboardInterrupt
    except Exception as e:
        # port closed
        pass


def progress(value, max, char='.'):
    if not value % max:
        print('\r', end="", flush=True)
        print(" " * max, end="", flush=True)
        print('\r', end="", flush=True)
        # print()
    print(char, end="", flush=True)


def scan_ports(converted_ip, ports, timeout, threaded=True, logger=rootlogger):
    """scan multiple ports for ip threaed or not"""

    if threaded:
        # threaded loop
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
            time.sleep(0.5)

        try:
            print(f"[+] starting port threads for {converted_ip} {ports}")
            for port in ports:
                th = threading.Thread(
                    target=scan_port,
                    name=f"scan_port {converted_ip:{15}} {port}",
                    args=(converted_ip, port, timeout),
                    kwargs=dict(logger=logger)
                )
                # print(f"[+] starting thread {th.getName()}")
                th.start()
                thread_count += 1
                progress(thread_count, 80)
                threads.append(th)
                time.sleep(0.5)

            # join loop
            print(f"[+] waiting port threads for {converted_ip}:{ports}")
            for th in threads:
                print(f"[+] joining thread {th.getName()}")
                th.join()
        except KeyboardInterrupt:
            print("CTRL-C: join and exit")
            for th in threads:
                print(f"[+] joining thread {th.getName()}")
                th.join()
            exit()
        except Exception as e:
            print(repr(e))
            print(f"{thread_count=}")
            return
    else:
        count = 0
        try:
            # non threaded loop
            for port in ports:
                # logger.debug(f"scan_port({dict(converted_ip=converted_ip, port=port, timeout=timeout, logger=logger)})")
                scan_port(converted_ip, port, timeout, logger=logger)
                count += 1
                progress(count, 80)
        except KeyboardInterrupt:
            print("CTRL-C: exit")
            exit()


def scan_target(target, start=1, end=100, timeout=0.5, port_threading=True, logdir=LOG_DIR):
    """scan single ip"""

    # setup logger
    logger = logging.getLogger(target)
    logger.setLevel(logging.NOTSET)
    # setup file handler
    logfile = os.path.join(logdir, f"{target}.log")
    filehandler = logging.FileHandler(logfile, mode="w")
    logger.addHandler(filehandler)
    # setup stream handler
    # logger.addHandler(logging.StreamHandler(stream=sys.stdout))

    # get ip
    try:
        converted_ip = check_ip(target)
    except Exception as e:
        logger.error(f"[-] invalid address/domain: {target}")
        return False

    # select port range
    ports = range(start, end + 1)

    # show process params
    params = dict(
        target=target,
        start=start,
        end=end,
        timeout=timeout,
        port_threading=port_threading,
        logdir=logdir
    )
    logger.debug(f"[+] scan_target({params})):")
    logger.info(f"[+] Target    : {target}")
    logger.info(f"[+] Target ip : {converted_ip}")
    logger.info(f"[+] Port range: {start}-{end}")
    logger.info(f"[+] timeout   : {timeout}")

    # scan ports
    print("call scan_ports")
    scan_ports(converted_ip, ports, timeout, port_threading, logger=rootlogger)
    return True


def scan_targets(*targets, start, end, timeout, target_threading, port_threading):
    """scan multuiple ips"""

    # extract kwargs for scan_target function
    kwargs = dict(
        start=start,
        end=end,
        timeout=timeout,
        threaded=port_threading
    )

    if target_threading:
        threads = []
        thread_count = 0

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
            time.sleep(0.5)

        for th in threads:
            print(f"[+] joining target thread {th.getName()}")
            th.join()
        print(f"[+] waiting for target threads")
    else:
        # non threaded loop
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
