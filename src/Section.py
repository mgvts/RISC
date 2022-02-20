from .commonFunc import *


class Section:
    def __init__(self, start):
        (self.sh_name, self.sh_type, self.sh_flags, self.sh_addr,
         self.sh_offset, self.sh_size, self.sh_link, self.sh_info,
         self.sh_addralign, self.sh_entsize) = get_param(start, [4] * 10)

    def __repr__(self):
        return f"{self.sh_name} {self.sh_type} {self.sh_flags} {self.sh_addr}" \
               f" {self.sh_offset} {self.sh_size} {self.sh_link} " \
               f"{self.sh_info} {self.sh_addralign} {self.sh_entsize}"

    def getNameSection(self, offset):
        i = self.sh_name + offset
        return get_name_start(i)
