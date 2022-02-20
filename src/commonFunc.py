import sys


def get_param(start, sz):
    try:
        s = []
        for i in range(len(sz)):
            s.append(get_bytes(start, sz[i]))
            start += sz[i]
        return s
    except IndexError:
        print("Incorrect elf file")
        exit()


def get_bytes(start, length):
    res = 0
    for i in range(start + length - 1, start - 1, -1):
        res <<= 8
        res += stream[i]
    return res


def get_name_start(start):
    nm = ""
    i = start
    while True:
        if stream[i] == 0:
            return nm
        else:
            nm += chr(stream[i])
        i += 1


try:
    with open(sys.argv[1], "rb") as file:
        stream = file.read()
    out = open(sys.argv[2], "w")
except FileNotFoundError:
    print(f"file: {sys.argv[1]} is not found")
    exit()
except IndexError:
    print(f"u doesnt put files")
    exit()
