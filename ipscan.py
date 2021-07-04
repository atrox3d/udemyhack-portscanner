import sys
import getopt
import portscanner


def show_help():
    # options_string = " ".join([f"[-{option}]" for option in options if option != ":"])
    print(f"syntax: {sys.argv[0]} [-h] [-t timeout] [-r port range start-end] [-s port start] [-e port end]")


options = "ht:r:s:e:"
try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        options
    )
    print(f"{opts=}")
    print(f"{args=}")
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
        print(f"set timeout to: {timeout}")
    elif opt in ['-r']:
        try:
            start, end = map(int, arg.split("-"))
            print(f"set port range start to: {start}-{end}")
        except Exception as e:
            print(f"ERROR| invalid range format {arg}")
            exit(1)
    elif opt in ['-s']:
        start = int(arg)
        print(f"set port range start to: {start}")
    elif opt in ['-e']:
        end = int(arg)
        print(f"set port range end to: {end + 1}")
    elif opt in ['-h']:
        show_help()
        exit()

targets = args
kw = dict(start=start, end=end, timeout=timeout)
kwa = {k: v for k, v in kw.items() if v is not None}
for target in targets:
    portscanner.scan(target, **kwa)
