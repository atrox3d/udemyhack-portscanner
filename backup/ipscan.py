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
kw = dict(start=start, end=end, timeout=timeout, threaded=port_threading)
kwargs = {k: v for k, v in kw.items() if v is not None}

# if port_threading:
#     # def threaded(function):
#     #     def wrapper(*args, **kwargs):
#     #         thread = threading.Thread(target=function, name=function.__name__,  args=args, kwargs=kwargs)
#     #         thread.start()
#     #         return thread
#     #     return wrapper
#     #
#     # portscanner.scan_port = threaded(portscanner.scan_port)
#
#     def threaded_scan_ports_decorator(function):
#         def threaded_scan_ports(*args, **kwargs):
#
#             converted_ip, ports, timeout = args
#
#             threads = []
#             print(f"[+] starting port threads for {converted_ip}:{ports}")
#             for port in ports:
#                 new_args = converted_ip, port, timeout
#                 th = threading.Thread(
#                     target=portscanner.scan_port,
#                     name=f"scanport({', '.join(map(str,new_args))})",
#                     args=new_args,
#                     kwargs=kwargs)
#                 # print(f"[+] starting thread {th.getName()}")
#                 th.start()
#                 threads.append(th)
#             for th in threads:
#                 # print(f"[+] joining thread {th.getName()}")
#                 th.join()
#             print(f"[+] waiting port threads for {converted_ip}:{ports}")
#         return threaded_scan_ports
#
#     portscanner.scan_ports = threaded_scan_ports_decorator(portscanner.scan_ports)

LOGDIR = "logs"
targets = args

if target_threading:
    threads = []

    for target in targets:
        th = threading.Thread(target=portscanner.scan_target, name=target, args=(target,), kwargs=kwargs)
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
        portscanner.print = print_to_file_decorator(logfile)
        portscanner.scan_target(target, **kwargs)
