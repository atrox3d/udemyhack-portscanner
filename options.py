import getopt
import sys


def show_help():
    # options_string = " ".join([f"[-{option}]" for option in options if option != ":"])
    print(
        f"syntax: {sys.argv[0]} "
        f"[-h]                     : display help and exit"
        f"[-T]                     : enable target threading"
        f"[-P]                     : enable port threading"
        f"[-t timeout]             : set timeout (default 0.5)"
        f"[-r port range start-end]: set port range start-end (default(1-100)"
        f"[-s port start]          : set port start (default 1)"
        f"[-e port end]            : set port end (default 100)"
    )


def parse_options():
    options = "hTPt:r:s:e:"

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            options
        )
        print(f"GETOPT| {opts=}")
        print(f"GETOPT| {args=}")
    except getopt.GetoptError as goe:
        print(repr(goe))
        exit(1)

    target_threading = False
    port_threading = False
    timeout = None
    start = None
    end = None
    for opt, arg in opts:
        if opt in ['-t']:
            timeout = float(arg)
            print(f"GETOPT| set timeout to: {timeout}")
        elif opt in ['-T']:
            target_threading = True
            print(f"GETOPT| enable target threading")
        elif opt in ['-P']:
            port_threading = True
            print(f"GETOPT| enable port threading")
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
    return target_threading, port_threading, timeout, start, end, args
