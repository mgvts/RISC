from .commands import Command16, Command32
from .commonFunc import *


class ParsedCommands:
    def __init__(self, num, command, offset):
        self.num = num
        self.command = command
        self.offset = offset


def get_command(number, command_length):
    bits = []
    s = []
    while number:
        bits.append(number % 2)
        number //= 2

    if command_length == 16:
        bits.extend([0] * (16 - len(bits)))
        sz = [[0, 1], [2, 6], [7, 11], [12, 12], [13, 15]]

        for elem in sz:
            a, b = elem[0], elem[1]
            s.append("".join(map(str, reversed(bits[a:b + 1]))))
        s.append("".join(map(str, bits[0:16])))
        return Command16(*s)

    elif command_length == 32:

        bits.extend([0] * (32 - len(bits)))
        sz = [[0, 6], [7, 11], [12, 14], [15, 19], [20, 31]]

        for elem in sz:
            a, b = elem[0], elem[1]
            s.append("".join(map(str, reversed(bits[a:b + 1]))))
        s.append("".join(map(str, bits[0:32])))
        return Command32(*s)
    else:
        print("only 16-bit or 32-bit instructions are allowed")
        exit()


def parse_command(start, offset_to_jump_command, has_offset):
    first_byte = get_bytes(start, 1)
    first_bits = (first_byte % 2) + (first_byte // 2) % 2

    if first_bits == 2:
        command = get_command(get_bytes(start, 4), 32)
        return *command.output_command32(offset_to_jump_command, has_offset), 4
        # it consists of 32 bits
    else:
        command = get_command(get_bytes(start, 4), 16)
        return *command.output_command16(offset_to_jump_command, has_offset), 2
        # it consists of 16 bits
