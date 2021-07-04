import sys
import getopt
import portscanner

try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        "ht:r:s:e:"
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
    elif opt in ['-s']:
        start = int(arg)
    elif opt in ['-e']:
        end = int(arg)

# target = 'youweb.bancobpm.it'
targets = args
kw = dict(start=start, end=end, timeout=timeout)
kwa = {k: v for k, v in kw.items() if v is not None}
for target in targets:
    portscanner.scan(target, **kwa)
