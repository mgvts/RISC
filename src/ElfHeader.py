from .commonFunc import *


class ElfHeader:
    def __init__(self):
        sz = [16, 2, 2, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2]
        (self.e_ident, self.e_type, self.e_machine, self.e_version,
         self.e_entry, self.e_phoff, self.e_shoff, self.e_flags,
         self.e_ehsize, self.e_phentsize, self.e_phnum,
         self.e_shentsize, self.e_shnum, self.e_shstrndx) = get_param(0, sz)
