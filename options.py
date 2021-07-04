import getopt
import sys


def show_help():
    # options_string = " ".join([f"[-{option}]" for option in options if option != ":"])
    print(f"syntax: {sys.argv[0]} [-h] [-t timeout] [-r port range start-end] [-s port start] [-e port end]")


def parse_options():
    options = "ht:r:s:e:"
    options = "hTt:r:s:e:"

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

    threads = False
    timeout = None
    start = None
    end = None
    for opt, arg in opts:
        if opt in ['-t']:
            timeout = float(arg)
            print(f"GETOPT| set timeout to: {timeout}")
        elif opt in ['-T']:
            threads = True
            print(f"GETOPT| enable threading")
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
    return threads, timeout, start, end, args
