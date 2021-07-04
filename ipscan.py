import os
import sys
import getopt
import portscanner


def print_to_file_decorator(file):
    def print_decorator(*args, **kwargs):
        print(*args, **kwargs)
        kwargs.update(file=file)
        print(*args, **kwargs)

    return print_decorator


def show_help():
    # options_string = " ".join([f"[-{option}]" for option in options if option != ":"])
    print(f"syntax: {sys.argv[0]} [-h] [-t timeout] [-r port range start-end] [-s port start] [-e port end]")


options = "ht:r:s:e:"
try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        options
    )
    print(f"GETOPT| {opts=}")
    print(f"GETOPT| {args=}")
    # print(f"{sys.argv[1:]=}")
except getopt.GetoptError as goe:
    print(repr(goe))
    exit(1)

timeout = None
start = None
end = None
for opt, arg in opts:
    if opt in ['-t']:
        timeout = float(arg)
        print(f"GETOPT| set timeout to: {timeout}")
    elif opt in ['-r']:
        try:
            start, end = map(int, arg.split("-"))
            print(f"GETOPT| set port range start to: {start}-{end}")
        except ValueError as e:
            print(f"GETOPT| ERROR| invalid range format {arg}")
            print(f"GETOPT| ERROR| {repr(e)}")
            exit(1)
    elif opt in ['-s']:
        start = int(arg)
        print(f"GETOPT| set port range start to: {start}")
    elif opt in ['-e']:
        end = int(arg)
        print(f"GETOPT| set port range end to: {end + 1}")
    elif opt in ['-h']:
        show_help()
        exit()

LOGDIR = "logs"
targets = args
kw = dict(start=start, end=end, timeout=timeout)
kwargs = {k: v for k, v in kw.items() if v is not None}
for target in targets:
    logfile = open(os.path.join("logs", f"{target}.log"), "w")
    portscanner.print = print_to_file_decorator(logfile)
    portscanner.scan(target, **kwargs)
