from .commands.const import *
from .commonFunc import *


class SymtabEntry:
    def __init__(self, start, symtab_name_offset):
        sz = [4, 4, 4, 1, 1, 2]
        (self.st_name, self.st_value, self.st_size,
         self.st_info, self.st_other, self.st_shndx) = get_param(start, sz)

        # fields we get from st_info
        self.bind = binds[self.st_info >> 4]
        self.type = types[self.st_info & 0xf]

        # fields we get from st_other
        self.vis = vises[self.st_other & 0x3]

        # fields we get from index
        if self.st_shndx in special.keys():
            self.index = special[self.st_shndx]
        else:
            self.index = self.st_shndx

        self.name = get_name_start(self.st_name + symtab_name_offset)

    def get_res(self, num):
        Symbol = f"[{str(num).rjust(4)}]"
        Value = hex(self.st_value).ljust(17)
        Size = str(self.st_size).rjust(5)
        Type = self.type.ljust(8)
        Bind = self.bind.ljust(8)
        Vis = self.vis.ljust(8)
        Index = str(self.index).rjust(6)
        Name = self.name
        return f"{Symbol} {Value} {Size} {Type} {Bind} {Vis} {Index} {Name}"
