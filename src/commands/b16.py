from .const import *
from .utils import *


class Command16:
    def __init__(self, opcode, nzimm_1, rs, nzimm_2, funct3, full):
        self.opcode = opcode
        self.nzimm_1 = nzimm_1
        self.rs = rs
        self.nzimm_2 = nzimm_2
        self.funct3 = funct3
        self.full = full

    def get_bits(self, start, end):
        return "".join(reversed(self.full[start:end + 1]))

    def __repr__(self):
        return reversed(self.full)

    def opcode00(self, *args):
        rs2 = reg_rvc[int(self.get_bits(2, 4), 2)]
        rs1 = reg_rvc[int(self.get_bits(7, 9), 2)]
        uimm = int(self.get_bits(5, 5) + self.get_bits(10, 12) + self.get_bits(6, 6), 2) << 2
        d = {
            "010": "c.lw",
            "110": "c.sw"
        }

        if self.funct3 == "000":
            imm = int(self.get_bits(7, 10) + self.get_bits(11, 12) + self.get_bits(5, 5) + self.get_bits(6, 6), 2) << 2
            if imm == 0:
                return "unknown_command", *args
            rd = reg_rvc[int(self.get_bits(2, 4), 2)]
            return f"c.addi4spn {rd}, sp, {imm}", *args
        else:
            nm = d[self.funct3]
        if nm is None:
            return "unknown_command", *args

        return f"{nm} {rs2}, {uimm}({rs1})", *args

    def opcode01(self, *args):
        if self.funct3 == "000" and int(self.get_bits(7, 11), 2) == 0:
            return "c.nop", *args

        if self.funct3 == "000" and int(self.get_bits(7, 11), 2) == 0:
            rs1 = reg[int(self.get_bits(7, 11), 2)]
            imm = int(self.get_bits(2, 6), 2) - int(self.get_bits(12, 12)) << 5
            return f"c.addi {rs1}, {imm}", *args

        elif self.funct3 == "001":
            offset_to_jump_command = int(self.get_bits(8, 8) + self.get_bits(10, 10) +
                                         self.get_bits(9, 9) + self.get_bits(6, 6) + self.get_bits(7, 7) +
                                         self.get_bits(2, 2) + self.get_bits(11, 11) + self.get_bits(3, 5),
                                         2) * 2 - int(self.get_bits(12, 12)) << 11
            return "c.jal", offset_to_jump_command, True

        elif self.funct3 == "010":
            rd = reg[int(self.get_bits(7, 11), 2)]
            imm = int(self.get_bits(2, 6), 2) - int(self.get_bits(12, 12)) << 5
            return f"c.li {rd}, {imm}", *args

        elif self.funct3 == "011" and int(self.get_bits(7, 11), 2) == 2:
            nzimm = int(self.get_bits(3, 4) + self.get_bits(5, 5) + self.get_bits(
                2, 2) + self.get_bits(6, 6), 2) << 4 - int(self.get_bits(12, 12)) << 9
            return f"c.addi16sp sp, {nzimm}", *args

        elif self.funct3 == "011" and int(self.get_bits(7, 11), 2) == 0:

            return "unknown_command", *args

        elif self.funct3 == "011":
            nzimm = int(self.get_bits(12, 12) +
                        self.get_bits(2, 6), 2) << 12
            rd = reg[int(self.get_bits(7, 11), 2)]
            return f"c.lui {rd}, {nzimm}", *args

        elif self.funct3 == "100":
            nzuimm = int(self.get_bits(12, 12) + self.get_bits(2, 6), 2)
            rd = reg_rvc[int(self.get_bits(7, 9), 2)]
            imm = int(self.get_bits(2, 6), 2) - \
                  int(self.get_bits(12, 12)) << 5
            d = {
                "00": f"c.srli {rd}, {nzuimm}",
                "01": f"c.srai {rd}, {nzuimm}",
                "10": f"c.andi {rd}, {imm}"
            }

            if self.get_bits(10, 11) == "11":
                dd = {
                    "00": "c.sub",
                    "01": "c.xor",
                    "10": "c.or",
                    "11": "c.and"
                }
                rs2 = reg_rvc[int(self.get_bits(2, 4), 2)]
                rs1 = reg_rvc[int(self.get_bits(7, 9), 2)]
                return f"{dd[self.get_bits(5, 6)]} {rs1}, {rs2}", *args
            else:
                return d[self.get_bits(10, 11)], *args

        elif self.funct3 == "101":
            offset_to_jump_command = int(self.get_bits(8, 8) + self.get_bits(10, 10) +
                                         self.get_bits(9, 9) + self.get_bits(6, 6) + self.get_bits(7, 7) +
                                         self.get_bits(2, 2) + self.get_bits(11, 11) + self.get_bits(3, 5),
                                         2) * 2 - int(
                self.get_bits(12, 12)) << 11
            return "c.j", offset_to_jump_command, True

        elif self.funct3 == "110":
            offset_to_jump_command = int(self.get_bits(12, 12) + self.get_bits(5, 6) +
                                         self.get_bits(2, 2) + self.get_bits(10, 11) + self.get_bits(3, 4),
                                         2) * 2 - 2 * 256 * int(self.get_bits(12, 12))
            rs1 = reg_rvc[int(self.get_bits(7, 9), 2)]
            return f"c.beqz {rs1}", offset_to_jump_command, True

        elif self.funct3 == "111":
            offset_to_jump_command = int(self.get_bits(12, 12) + self.get_bits(5, 6) +
                                         self.get_bits(2, 2) + self.get_bits(10, 11) + self.get_bits(3, 4),
                                         2) * 2 - 2 * 256 * int(self.get_bits(12, 12))
            rs1 = reg_rvc[int(self.get_bits(7, 9), 2)]
            return f"c.bnez {rs1}", offset_to_jump_command, True
        else:
            return "unknown_command", *args

    def opcode10(self, *args):
        if self.funct3 == "000":
            rs1 = reg[int(self.get_bits(7, 11), 2)]
            nzuimm = int(self.get_bits(12, 12) + self.get_bits(2, 6), 2)
            return f"c.slli {rs1}, {nzuimm}", *args

        elif self.funct3 == "010":
            rd = reg[int(self.get_bits(7, 11), 2)]
            uimm = int(self.get_bits(2, 3) + self.get_bits(12, 12) + self.get_bits(4, 6), 2) * 4
            return f"c.lwsp {rd}, {uimm}(sp)", *args

        elif self.funct3 == "100" and int(self.get_bits(2, 6), 2) == 0 and int(self.get_bits(7, 11)) == 0:
            return "c.ebreak", *args

        elif self.funct3 == "100" \
                and int(self.get_bits(2, 6), 2) == 0 \
                and int(self.get_bits(7, 11)) != 0:
            rs1 = reg[int(self.get_bits(7, 11), 2)]
            if self.get_bits(12, 12) == "0":
                return f"c.jr {rs1}", *args
            else:
                return f"c.jalr {rs1}", *args

        elif self.funct3 == "100" and int(self.get_bits(2, 6), 2) != 0:
            rd = reg[int(self.get_bits(7, 11), 2)]
            rs2 = reg[int(self.get_bits(2, 6), 2)]
            if self.get_bits(12, 12) == "0":
                return f"c.mv {rd} {rs2}", *args
            else:
                return f"c.add {rd} {rs2}", *args

        elif self.funct3 == "110":
            uimm = int(self.get_bits(7, 8) + self.get_bits(9, 12), 2) * 4
            rs2 = reg[int(self.get_bits(2, 6), 2)]
            return f"c.swsp {rs2}, {uimm}(sp)", *args
        else:
            return "unknown_command", *args

    @decor_unknown_command
    def output_command16(self, offset_to_jump_command, has_offset):
        return self.__getattribute__(f'opcode{self.opcode}')(offset_to_jump_command, has_offset)
