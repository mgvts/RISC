opcode1100011 = {
    "000": "beq",
    "001": "bne",
    "100": "blt",
    "101": "bge",
    "110": "bltu",
    "111": "bgeu"
}

opcode0000011 = {
    "000": "lb",
    "001": "lh",
    "010": "lw",
    "100": "lbu",
    "101": "lhu"
}

opcode0100011 = {
    "000": "sb",
    "001": "sh",
    "010": "sw"
}

opcode0010011 = {
    "000": "addi",
    "001": "slli",
    "010": "slti",
    "011": "sltiu",
    "100": "xori",
    "110": "ori",
    "111": "andi",
}

opcode0110011 = {
    "000": "mul",
    "001": "mulh",
    "010": "mulhsu",
    "011": "mulhu",
    "100": "div",
    "101": "divu",
    "110": "rem",
    "111": "remu"
}

opcode0110011_2 = {
    "000": lambda self: "add" if self.get_bits(30, 30) == "0" else "sub",
    "001": "sll",
    "010": "slt",
    "011": "sltu",
    "100": "xor",
    "101": lambda self: "srl" if self.get_bits(30, 30) == "0" else "sra",
    "110": "or",
    "111": "and"
}

opcode1110011 = {
    "000": lambda self: "ecall" if self.get_bits(20, 20) == "0" else "ebreak",
    "001": "csrrw",
    "010": "csrrs",
    "011": "csrrc",
    "101": "csrrwi",
    "110": "csrrsi",
    "111": "csrrci"
}
