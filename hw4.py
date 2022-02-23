from src.ElfHeader import *
from src.Section import *
from src.SymtabEntry import *
from src.ParsCommands import *

hd = ElfHeader()
number_of_sections = hd.e_shnum
numberSymtabEntries = None

sections, symtabEntries, code = [], [], []

leftLabelDict, rightLabelDict = {}, {}

symtabNameOffset, symtabOffset, codeOffset = None, None, None

locCounter = 0

try:
    for i in range(hd.e_shnum):
        sections.append(Section(hd.e_shoff + i * SECTION_SIZE))

    nameTableSections = sections[hd.e_shstrndx]

    for sect in sections:
        name = sect.getNameSection(nameTableSections.sh_offset)
        if name == ".symtab":
            symtabOffset = sect.sh_offset
            numberSymtabEntries = sect.sh_size // 16

        if name == ".strtab":
            symtabNameOffset = sect.sh_offset

        if name == ".text":
            codeOffset = sect.sh_offset
            codeSize = sect.sh_size
            codeAddress = sect.sh_addr

    for weakPoint in [symtabNameOffset, symtabOffset, numberSymtabEntries]:
        if weakPoint is None:
            print("Elf file isn't correct")
            exit()

    for i in range(numberSymtabEntries):
        symtabEntries.append(SymtabEntry(symtabOffset + i * SYMTAB_ENTRY_SIZE, symtabNameOffset))
        if symtabEntries[i].name != "":
            leftLabelDict[symtabEntries[i].st_value] = symtabEntries[i].name

    i = codeOffset
    end = codeOffset + codeSize
    print(".text", file=out)
    cnt = 0

    offset_to_jump_command = 0
    has_offset = False

    parsedCode = []

    while i < end:
        leftLbl, rightLbl = False, False
        offset = None
        num = cnt + codeAddress
        res, offset_to_jump_command, has_offset, bits = parse_command(i, offset_to_jump_command, has_offset)

        if num in leftLabelDict.keys():
            leftLbl = leftLabelDict[num]

        if has_offset and (num + offset_to_jump_command) in leftLabelDict.keys():
            rightLabelDict[num] = leftLabelDict[num + offset_to_jump_command]

        if has_offset:
            offset = offset_to_jump_command

        parsedCode.append(ParsedCommands(num, res, offset))

        i += bits
        cnt += bits

    for code in parsedCode:
        command = code.command
        offset = code.offset
        num = code.num
        rightLabel = False
        leftLabel = False

        if not offset is None:
            num1 = num + offset

            if num1 in leftLabelDict.keys():
                rightLabelDict[num] = leftLabelDict[num1]

            elif not num1 in leftLabelDict.keys() and num in rightLabelDict.keys():
                leftLabelDict[num1] = rightLabelDict[num]

            else:
                rightLabelDict[num] = f"LOC_{hex(locCounter)[2:].rjust(5, '0')}"
                locCounter += 1
                leftLabelDict[num1] = rightLabelDict[num]

    for code in parsedCode:
        num = code.num
        res = code.command
        leftLbl, rightLbl = False, False

        if code.num in leftLabelDict.keys():
            leftLbl = leftLabelDict[num]

        if code.num in rightLabelDict.keys():
            rightLbl = rightLabelDict[num]

        if not leftLbl:
            leftLbl = ""
        else:
            leftLbl = leftLbl + ":"

        if not rightLbl:
            rightLbl = ""
        else:
            rightLbl = ", " + rightLbl

        print(f"{hex(num)[2:].rjust(8, '0')} {leftLbl.rjust(11, ' ')} {res}{rightLbl}", file=out)

    print(file=out)
    print(".symtab", file=out)
    print(f"Symbol Value{' ' * 14}Size Type{' ' * 5}Bind{' ' * 5}Vis{' ' * 7}Index Name", file=out)

    for i in range(len(symtabEntries)):
        print(symtabEntries[i].get_res(i), file=out)

    out.close()
except Exception as e:
    print("bad elf file or smth with commands", e)
