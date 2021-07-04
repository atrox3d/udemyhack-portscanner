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


threads, timeout, start, end, args = parse_options()

LOGDIR = "logs"
targets = args
kw = dict(start=start, end=end, timeout=timeout)
kwargs = {k: v for k, v in kw.items() if v is not None}

if threads:
    # create_threads(targets, portscanner.scan, args, kwargs)
    threads = []

    for target in targets:
        th = threading.Thread(target=portscanner.scan, name=target, args=(target,), kwargs=kwargs)
        print(f"[+] starting thread {th.getName()}")
        th.start()
        threads.append(th)

    for th in threads:
        th.join()
else:
    for target in targets:
        logfile = open(os.path.join("logs", f"{target}.log"), "w")
        portscanner.print = print_to_file_decorator(logfile)
        portscanner.scan(target, **kwargs)
