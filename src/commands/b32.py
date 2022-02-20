from .const import *
from .utils import *
from .command_const import *


class Command32:
    def __init__(self, opcode, rd, funct3, rs1, imm, full):
        self.opcode = opcode
        self.rd = int(rd, 2)
        self.funct3 = funct3
        self.rs1 = int(rs1, 2)
        self.imm = imm
        self.full = full

    def get_bits(self, start, end):
        return "".join(reversed(self.full[start:end + 1]))

    def __repr__(self):
        return reversed(self.full)

    def opcode110111(self, *args):
        temp_imm = int(self.get_bits(12, 31), 2) << 12
        return f"lui {reg[self.rd]}, {temp_imm}", *args

    def opcode0010111(self, *args):
        temp_imm = int(self.get_bits(12, 30), 2) << 12 - int(self.get_bits(31, 31)) << 31
        return f"auipc {reg[self.rd]}, {temp_imm}", *args

    def opcode1101111(self, *args):
        temp_imm = int(self.get_bits(31, 31) + self.get_bits(12, 19) +
                       self.get_bits(20, 20) + self.get_bits(21, 30), 2) * 2 - (1 << 21) * int(
            self.get_bits(31, 31))
        return f"jal {reg[self.rd]}", temp_imm, True

    def opcode1100111(self, *args):
        return f"jalr {reg[self.rd]}, {int(self.imm, 2) - 2 << 11 * int(self.get_bits(31, 31))}({reg[self.rs1]})", *args

    def opcode1100011(self, *args):
        temp_imm = int(self.get_bits(31, 31) + self.get_bits(7, 7)
                       + self.get_bits(25, 30) + self.get_bits(8, 11), 2) * 2 - 4096 * 2 * int(
            self.get_bits(31, 31))
        rs2 = int(self.get_bits(20, 24), 2)
        return f"{opcode1100011[self.funct3]} {reg[self.rs1]}, {reg[rs2]}", temp_imm, True

    def opcode0000011(self, *args):
        imm = int(self.imm, 2) - int(self.get_bits(31, 31)) << 12
        return f"{opcode0000011[self.funct3]} {reg[self.rd]}, {imm}({reg[self.rs1]})", *args

    def opcode0100011(self, *args):
        temp_imm_1 = -(int(self.get_bits(31, 31)) << 12) + int(self.get_bits(25, 31) + self.get_bits(7, 11), 2)
        rs2 = int(self.get_bits(20, 24), 2)
        return f"{opcode0100011[self.funct3]} {reg[rs2]}, {temp_imm_1}({reg[self.rs1]})", *args

    def opcode0010011(self, *args):
        imm = int(self.imm, 2) - int(self.get_bits(31, 31)) << 12
        if self.funct3 == "101":
            if self.get_bits(30, 30) == "0":
                nm = "srli"
                imm = int(self.get_bits(20, 25), 2)
            else:
                nm = "srai"
                imm = int(self.get_bits(20, 25), 2)
        else:
            nm = opcode0010011[self.funct3]

        return f"{nm} {reg[self.rd]}, {reg[self.rs1]}, {imm}", *args

    def opcode0110011(self, *args):
        rs2 = int(self.get_bits(20, 24), 2)
        if self.get_bits(25, 31) == "0000001":
            nm = opcode0110011[self.funct3]
        else:
            nm = opcode0110011_2[self.funct3]
            if type(nm) != str:
                nm = opcode0110011_2[self.funct3](self)

        return f"{nm} {reg[self.rd]}, {reg[self.rs1]}, {reg[rs2]}", *args

    def opcode1110011(self, *args):
        uimm = self.rs1
        csr = int(self.get_bits(20, 31), 2)
        if self.funct3 == "000":
            return f"{opcode1110011[self.funct3](self)}", *args

        elif self.funct3[0] == "1":
            return f"{opcode1110011[self.funct3]} {reg[self.rd]}, {reg_csr[csr]}, {uimm}", *args
        else:
            return f"{opcode1110011[self.funct3]} {self.rd}, {csr}, {reg[uimm]}", *args

    @decor_unknown_command
    def output_command32(self, offset_to_jump_command, has_offset=False):
        return self.__getattribute__(f'opcode{self.opcode}')(offset_to_jump_command, has_offset)
