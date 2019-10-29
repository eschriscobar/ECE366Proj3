# Author(s): 
# Supported instrs:
# LUI, ORI, ADDIU, MULTU, MFHI, MFLO

# register[4] = $LO
# reg
def sim(program):
    # Machine Code to Simulation

    finished = False        # Is the simulation finished?
    PC = 0                  # Program Counter
    register = [0] * 7     # Let's initialize 32 empty registers
    mem = [0] * 12288       # Let's initialize 0x3000 or 12288 spaces in memory.

    DIC = 0                 # Dynamic Instr Count
    while (not (finished)):

        if PC == len(program) - 1:
            finished = True
            register[26] = PC + 1       # which register will be PC ? 

        fetch = program[PC]
        DIC += 1

        # LUI (I) - Sim
        if fetch[0:4] == '0000': 
            PC += 1
            rx = int(fetch[4:6], 2)
            imm = int(fetch[6:], 2)
            #imm = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)

            register[rx] = imm

        # ORI (I) - Sim
        elif fetch[0:4] == '0001': 
            PC += 1
            rx = int(fetch[4:6], 2)
            imm = int(fetch[6:], 2)

            register[rx] = register[rx] | imm

        # ADDIU (I) - Sim
        elif fetch[0:4] == '0010': 
            PC += 1
            rx = int(fetch[4:6], 2)
            imm = int(fetch[6:], 2)

            register[rx] = register[rx] + imm

        # MULTU (R) - Sim
        elif fetch[0:4] == '0011': 
            PC += 1
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:], 2)

            register[4] = register[rx] * register[ry]

        # MFHI (?) - Sim
        elif fetch[0:6] == '010011': 
            PC += 1
            rx = int(fetch[6:], 2)

            register[rx] = register[5] # $HI

        # ORI (R) - Sim
        elif fetch[0:6] == '010111': 
            PC += 1
            rx = int(fetch[6:], 2)

            register[rx] = register[4] # $LO

        # XOR (R) - Sim
        elif fetch[0:4] == '0110': 
            PC += 1
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:], 2)

            register[rx] = register[rx] ^ register[ry]

        # SRL (I) - Sim
        elif fetch[0:4] == '0111': 
            PC += 1
            rx = int(fetch[4:6], 2)
            imm = int(fetch[6:], 2)

            register[rx] = register[rx] >> imm

        # ADDU (R) - Sim
        elif fetch[0:4] == '0110': 
            PC += 1
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:], 2)

            register[rx] = register[rx] + register[ry]

        # ANDI (R) - Sim
        elif fetch[0:4] == '1001': 
            PC += 1
            rx = int(fetch[4:6], 2)
            imm = int(fetch[6:], 2)

            register[rx] = register[rx] & imm

        # ST (R) - Sim
        elif fetch[0:4] == '1010': 
            PC += 1
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:], 2)

            mem[ry] = register[rx]

        # LD (R) - Sim
        elif fetch[0:4] == '1011': 
            PC += 1
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:], 2)

            register[rx] = mem[ry]

        # BEZ (?) - Sim
        elif fetch[0:4] == '1100': 
            PC += 1
            imm = int(fetch[4:], 2)

            if register[0] == 0:
                PC += imm
                if (imm < 0):
                    finished = False

        # SLT (R) - Sim
        elif fetch[0:4] == '1101': 
            PC += 1
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:], 2)

            if register[rx] < register[ry]:
                register[0] = 1
            else:
                register[0] = 0

        # J (J) - Sim
        elif fetch[0:4] == '1110': 
            imm = int(fetch[4:], 2)

            PC += (imm + 1)
        
        else:
            # This is not implemented on purpose
            PC += 1
            print('Not implemented')

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')

    print('')

    print('Dynamic Instr Count: ', DIC)

    print('                      _______________________________________________________________________________________')
    print('Registers $0 - $7:    | {}[$0] | {}[$1] | {}[$2] | {}[$3] | {}[$4] | {}[$5] | {}[$6] | {}[$7] |'.format(register[0], register[1], register[2], register[3], register[4], register[5], register[6], register[7]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    print('                      _______________________________________________________________________________________')
    print('Registers $8 - $15:   | {}[$8] | {}[$9] | {}[$10] | {}[$11] | {}[$12] | {}[$13] | {}[$14] | {}[$15] |'.format(register[8], register[9], register[10], register[11], register[12], register[13], register[14], register[15]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    print('                      _______________________________________________________________________________________')
    print('Registers $16 - $23:  | {}[$16] | {}[$17] | {}[$18] | {}[$19] | {}[$20] | {}[$21] | {}[$22] | {}[$23] |'.format(register[16], register[17], register[18], register[19], register[20], register[21], register[22],register[23]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    print('                      ____________________________________________________')
    print('Registers lo, hi, PC: | {}[lo] | {}[$hi] | {}[$pc] |'.format(register[24], register[25], register[26]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('')

    print('Memory contents in Decimal:')
    print('                      _________________________________________________________________________________________________')
    print('Mem 0x2000 - 0x200F:  | [0x2000] {} {} {} {}  | [0x2004] {} {} {} {}  | [0x2008] {} {} {} {}  | [0x200C] {} {} {} {}  |'.format(mem[8192], mem[8193], mem[8194], mem[8195], mem[8196], mem[8197], mem[8198], mem[8199], mem[8200], mem[8201], mem[8202], mem[8203], mem[8204], mem[8205], mem[8206], mem[8207]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    print('                      _________________________________________________________________________________________________')
    print('Mem 0x2010 - 0x201F:  | [0x2010] {} {} {} {}  | [0x2014] {} {} {} {}  | [0x2018] {} {} {} {}  | [0x201C] {} {} {} {}  |'.format(mem[8208], mem[8209], mem[8210], mem[8211], mem[8212], mem[8213], mem[8214], mem[8215], mem[8216], mem[8217], mem[8218], mem[8219], mem[8220], mem[8221], mem[8222], mem[8223]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    print('                      _________________________________________________________________________________________________')
    print('Mem 0x2020 - 0x202F:  | [0x2020] {} {} {} {}  | [0x2024] {} {} {} {}  | [0x2028] {} {} {} {}  | [0x202C] {} {} {} {}  |'.format(mem[8224], mem[8225], mem[8226], mem[8227], mem[8228], mem[8229], mem[8230], mem[8231], mem[8232], mem[8233], mem[8234], mem[8235], mem[8236], mem[8237], mem[8238], mem[8239]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    print('                      _________________________________________________________________________________________________')
    print('Mem 0x2030 - 0x203F:  | [0x2030] {} {} {} {}  | [0x2034] {} {} {} {}  | [0x2038] {} {} {} {}  | [0x203C] {} {} {} {}  |'.format(mem[8240], mem[8241], mem[8242], mem[8243], mem[8244], mem[8245], mem[8246], mem[8247], mem[8248], mem[8249], mem[8250], mem[8251], mem[8252], mem[8253], mem[8254], mem[8255]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    print('                      _________________________________________________________________________________________________')
    print('Mem 0x2040 - 0x204F:  | [0x2040] {} {} {} {}  | [0x2044] {} {} {} {}  | [0x2048] {} {} {} {}  | [0x204C] {} {} {} {}  |'.format(mem[8256], mem[8257], mem[8258], mem[8259], mem[8260], mem[8261], mem[8262], mem[8263], mem[8264], mem[8265], mem[8266], mem[8267], mem[8268], mem[8269], mem[8270], mem[8271]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    print('                      ____________________')
    print('Mem 0x2050:           | [0x2050] {} |'.format(mem[8272]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    input()

# Remember where each of the jump label is, and the target location
def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    countWithoutLabels = 0

    for line in asm:
        line = line.replace(" ","")

        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(countWithoutLabels) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
            countWithoutLabels -= 1

        lineCount += 1
        countWithoutLabels += 1

    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')


def main():
    # HW 4 (ASM to MC Instructions)
    labelIndex = []
    labelName = []

    f = open("mc.txt", "w+")
    h = open("Hash-MIPS-plus.asm", "r")

    asm = h.readlines()
    currentline = 0

    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm, labelIndex, labelName)  # Save all jump's destinations

    for line in asm:

        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0

        # = = = = ADDIU = = = = = = = = (I)
        if (line[0:5] == "addiu"):
            line = line.replace("addiu", "")  # delete the addiu from the string.
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            
            f.write(str('001001') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = ADDI = = = = = = = = (I)
        elif (line[0:4] == "addi"):
            line = line.replace("addi", "")
            line = line.split(",")
            
            imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            
            f.write(str('001000') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = ADD = = = = = = (R)
        elif (line[0:3] == "add"):
            line = line.replace("add", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rt = format(int(line[2]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000') + '\n')
            currentline += 1

        # = = = = SUB = = = = = = = = (R)
        elif (line[0:3] == "sub"):
            line = line.replace("sub", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rt = format(int(line[2]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100010') + '\n')
            currentline += 1

        # = = = = MULTU = = = = = = = = (R)
        elif (line[0:5] == "multu"):
            line = line.replace("multu", "")
            line = line.split(",")
            
            rs = format(int(line[0]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            rt = format(int(line[1]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            
            f.write(str('000000') + str(rs) + str(rt) + str('00000') + str('00000') + str('011001') + '\n')
            currentline += 1

        # = = = = MULT = = = = = = = = (R)
        elif (line[0:4] == "mult"):
            line = line.replace("mult", "")
            line = line.split(",")
            
            rs = format(int(line[0]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            rt = format(int(line[1]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            
            f.write(str('000000') + str(rs) + str(rt) + str('00000') + str('00000') + str('011000') + '\n')
            currentline += 1

        # = = = = SRL = = = = = = = = (R)
        elif (line[0:3] == "srl"):
            line = line.replace("srl", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rt = format(int(line[1]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            sh = format(int(line[2]), '05b')  # make element 3 in the set, 'line' an int of 5 bits. (sh)
            
            f.write(str('000000') + str('00000') + str(rt) + str(rd) + str(sh) + str('000010') + '\n')
            currentline += 1

        # = = = = SLL = = = = = = = = (R)
        elif (line[0:3] == "sll"):
            line = line.replace("sll", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rt = format(int(line[1]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            sh = format(int(line[2]), '05b')  # make element 3 in the set, 'line' an int of 5 bits. (sh)
            
            f.write(str('000000') + str('00000') + str(rt) + str(rd) + str(sh) + str('000000') + '\n')
            currentline += 1
            # question about splitting in python for the paranthesees?

        # = = = = LBU = = = = = = = = (I)
        elif (line[0:3] == "lbu"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("lbu", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            
            f.write(str('100100') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = LHU = = = = = = = = = (I)
        elif (line[0:3] == "lhu"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("lhu", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            
            f.write(str('100101') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = LUI = = = = = = = = (I)
        elif (line[0:3] == "lui"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("lui", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')

            f.write(str('001111') + str('00000') + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = LB = = = = = = = = = (I)
        elif (line[0:2] == "lb"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("lb", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            
            f.write(str('100000') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = SB = = = = = = = = = (I)
        elif (line[0:2] == "sb"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("sb", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            
            f.write(str('101000') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = LW = = = = = = = = = (I)
        elif (line[0:2] == "lw"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("lw", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            
            f.write(str('100011') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = SW = = = = = = = = = (I)
        elif (line[0:2] == "sw"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("sw", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            
            f.write(str('101011') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = ORI = = = = = = = = = (I)
        elif (line[0:3] == "ori"):
            line = line.replace("ori", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[2]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            
            f.write(str('001101') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = ANDI = = = = = = = = = (I)
        elif (line[0:4] == "andi"):
            line = line.replace("andi", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[2]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            
            f.write(str('001100') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = AND = = = = = = = = = (R)
        elif (line[0:4] == "and"):
            line = line.replace("and", "")
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rt = format(int(line[2]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000') + str('100100') + '\n')
            currentline += 1

        # = = = = MFHI = = = = = = = = (R)
        elif (line[0:4] == "mfhi"):
            line = line.replace("mfhi", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            
            f.write(str('000000') + str('00000') + str('00000') + str(rd) + str('00000') + str('010000') + '\n')
            currentline += 1

        # = = = = MFLO = = = = = = = = (R)
        elif (line[0:4] == "mflo"):
            line = line.replace("mflo", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            
            f.write(str('000000') + str('00000') + str('00000') + str(rd) + str('00000') + str('010010') + '\n')
            currentline += 1

        # = = = = XOR = = = = = = = = (R)
        elif (line[0:3] == "xor"):
            line = line.replace("xor", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rt = format(int(line[2]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000') + str('100110') + '\n')
            currentline += 1

        # = = = = BEQ = = = = = = = = = (I)
        elif (line[0:3] == "beq"):
            line = line.replace("beq", "")
            line = line.split(",")

            rt = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            
            for i in range(len(labelName)):
                if (labelName[i] == line[2]):
                    if (labelIndex[i] < currentline + 1):
                        imm = labelIndex[i] - (currentline + 1) + 65536
                    else:
                        imm = labelIndex[i] - (currentline + 1)
            
            f.write(str('000100') + str(rs) + str(rt) + str(format(imm,'016b')) + '\n')
            currentline += 1

        # = = = = BNE = = = = = = = = = (I)
        elif (line[0:3] == "bne"):
            line = line.replace("bne", "")
            line = line.split(",")

            rt = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')

            for i in range(len(labelName)):
                if (labelName[i] == line[2]):
                    if (labelIndex[i] < currentline + 1):
                        imm = labelIndex[i] - (currentline + 1) + 65536
                    else:
                        imm = labelIndex[i] - (currentline + 1)
           
            f.write(str('000101') + str(rs) + str(rt) + str(format(imm,'016b')) + '\n')
            currentline += 1

        # = = = = SLTU = = = = = = = = = (R)
        elif (line[0:4] == "sltu"):
            line = line.replace("sltu", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            rt = format(int(line[2]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000') + str('101011') + '\n')
            currentline += 1

        # = = = = SLT = = = = = = = = = (R)
        elif (line[0:3] == "slt"):
            line = line.replace("slt", "")
            line = line.split(",")
            
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            rt = format(int(line[2]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000') + str('101010') + '\n')
            currentline += 1

        # = = = = COMP = = = = = = (I)
        elif (line[0:4] == "comp"):
            line = line.replace("comp", "")  # delete the addiu from the string.
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            imm = format(0, '016b')
            
            f.write(str('011011') + str(rs) + str(rt) + str(imm) + '\n')
            currentline += 1

        # = = = = JUMP = = = = = = (J)
        elif (line[0:1] == "j"):
            line = line.replace("j", "")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if (line[0].isdigit()):  # First,test to see if it's a label or a integer
                f.write(str('000010') + str(format(int(line[0]), '026b')) + '\n')
                currentline += 1

            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        f.write(str('000010') + str(format(int(labelIndex[i]), '026b')) + '\n')
                        currentline += 1

    f.close()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # file opener and reader (Machine Code)

    file = open('mc.txt')

    program = []

    for line in file:

        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)

        if line[0] == '\n':
            continue

        line = line.replace('\n', '')
        instr = line[:]

        program.append(instr)  # since PC increment by 4 every cycle,
        program.append(0)  # let's align the program code by every
        program.append(0)  # 4 lines
        program.append(0)

    # We SHALL start the simulation!
    sim(program)

if __name__ == '__main__':
    main()

#fin