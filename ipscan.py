import os
import sys
import portscanner
import threading

from options import parse_options


def create_threads(iplist, function):
    threads = []

    for ip in iplist:
        th = threading.Thread(target=function, args=(ip,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()


def print_to_file_decorator(file):
    def print_decorator(*args, **kwargs):
        print(*args, **kwargs)
        kwargs.update(file=file)
        print(*args, **kwargs)

    return print_decorator


target_threading, port_threading,  timeout, start, end, args = parse_options()

LOGDIR = "logs"
targets = args
kw = dict(start=start, end=end, timeout=timeout)
kwargs = {k: v for k, v in kw.items() if v is not None}

if target_threading:
    target_threading = []

    for target in targets:
        th = threading.Thread(target=portscanner.scan, name=target, args=(target,), kwargs=kwargs)
        print(f"[+] starting thread {th.getName()}")
        th.start()
        target_threading.append(th)

    for th in target_threading:
        print(f"[+] joining thread {th.getName()}")
        th.join()
    print(f"[+] waiting for threads")
else:
    for target in targets:
        logfile = open(os.path.join("logs", f"{target}.log"), "w")
        portscanner.print = print_to_file_decorator(logfile)
        portscanner.scan(target, **kwargs)
