import os
import threading
import time

import portscanner
from options import parse_options


def create_threads(iplist, function):
    threads = []

    for ip in iplist:
        th = threading.Thread(target=function, args=(ip,))
        print(f"starting thread {th.getName()}")
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


target_threading, port_threading, timeout, start, end, args = parse_options()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")

kwargs_dict = dict(
    start=start,
    end=end,
    timeout=timeout,
    port_threading=port_threading,
    logdir=LOG_DIR
)
kwargs = {k: v for k, v in kwargs_dict.items() if v is not None}

print(kwargs)

targets = args

if target_threading:
    try:
        threads = []
        thread_count = 0

        for target in targets:
            th = threading.Thread(
                target=portscanner.scan_target,
                name=target,
                args=(target,),
                kwargs=kwargs
            )
            print(f"[+] starting thread {th.getName()}")
            th.start()
            thread_count += 1
            threads.append(th)
            time.sleep(0.5)

        for th in threads:
            print(f"[+] joining target thread {th.getName()}")
            th.join()
        print(f"[+] waiting for target threads")
    except Exception as e:
        print(repr(e))
        print(f"{thread_count=}")
else:
    for target in targets:
        portscanner.scan_target(target, **kwargs)
