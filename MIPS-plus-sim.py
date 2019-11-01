# Author(s): 
# Supported instrs:
# LUI, ORI, ADDIU, MULTU, MFHI, MFLO, XOR, SRL, ADDU, ANDI, ST, LD, BEZ, SLT, JMP

# register[4] = PC

def hash(A, B, rx, mem, register):
    #first fold (down to 8 bits)
    C = B*A
    C_hi = C >> 8
    C_low = C & 0x00FF
    C = C_hi^C_low
    
    #Second fold
    C = B*C
    C_hi = C >> 8
    C_low = C & 0x00FF
    C = C_hi^C_low

    #third fold
    C = B*C
    C_hi = C >> 8
    C_low = C & 0x00FF
    C = C_hi^C_low

    #fourth fold
    C = B*C
    C_hi = C >> 8
    C_low = C & 0x00FF
    C = C_hi^C_low

    #fifth fold
    C = B*C
    C_hi = C >> 8
    C_low = C & 0x00FF
    C = C_hi^C_low

    #Down to 4 bits
    C_hi = C >> 4
    C_low = C & 0x0F
    C = C_hi^C_low

    #Down to 2 bits
    C_hi = C >> 2
    C_low = C & 0xF
    C = C_hi^C_low

    if(C == '00'):
        mem[0] = mem[0] + 1
    elif(C == '01'):
        mem[1] = mem[1] + 1
    elif(C == '10'):
        mem[2] = mem[2] + 1
    elif(C == '11'):
        mem[3] = mem[3] + 1

    mem[0x4 + (A - 1)] = C
    register[rx] = C

def sim(program):
    # Machine Code to Simulation

    finished = False        # Is the simulation finished?
    PC = 0                  # Program Counter
    register = [0] * 5     # Let's initialize 32 empty registers
    mem = [0] * 12288       # Let's initialize 0x3000 or 12288 spaces in memory.
    #f = open("mc.txt","w+")
    DIC = 0                 # Dynamic Instr Count
    while (not (finished)):

        if PC == len(program) - 1:
            finished = True
            register[4] = PC + 1       # which register will be PC ? 

        fetch = program[PC]
        DIC += 1

        # ADDI - Sim
        if fetch[0:2] == '11': 
            PC += 1
            rx = int(fetch[2:4], 2)
            imm = -(16 - int(fetch[4:], 2)) if fetch[4] == '1' else int(fetch[4:], 2)

            register[rx] = register[rx] + imm

        # FUNC - Sim
        elif fetch[0:2] == '00':
            PC += 1
            rx = int(fetch[2:4], 2)
            ry = int(fetch[4:6], 2)
            rz = int(fetch[6:], 2)
            
            hash(register[ry], register[rz], rx, mem, register)

        # ADD - Sim
        if fetch[0:4] == '0100': 
            PC += 1
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:], 2)

            register[rx] = register[rx] + register[ry]

        # BNEZR2 - Sim
        elif fetch[0:4] == '1011':
            PC += 1
            imm = -(16 - int(fetch[4:], 2)) if fetch[4] == '1' else int(fetch[4:], 2)
            
            # Compare the registers and decide if jumping or not
            if register[2] != 0:
                PC = PC + imm
                if (imm < 0):
                    finished = False

        # LUIR1 - Sim
        elif fetch[0:4] == '0110': 
            PC += 1
            imm = int(fetch[4:], 2)

            #f.write("LUIR1\n")

            register[1] = imm << 4

        # ORIR1 - Sim
        elif fetch[0:4] == '0111': 
            PC += 1
            imm = int(fetch[4:], 2)

            #f.write("ORIR1\n")

            register[1] = int(register[1]) | imm
        
        else:
            # This is not implemented on purpose
            PC += 1
            print('Not implemented')
            #f.write("N I")

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')

    print('')

    print('Dynamic Instr Count: ', DIC)

    print('                      ____________________________________________')
    print('Registers $0 - $3:    | {}[$0] | {}[$1] | {}[$2] | {}[$3] |'.format(register[0], register[1], register[2], register[3]))
    print('                      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    print('    ______________')
    print('PC: | {}[$pc] |'.format(register[4]))
    print('    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('')

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
    h = open("test.asm", "r")

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

        # = = = = ADDI = = = = = = = = 
        if (line[0:4] == "addi"):
            line = line.replace("addi", "")  # delete the addiu from the string.
            line = line.split(",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            
            rx = format(int(line[0]), '02b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '04b') if (int(line[1]) >= 0) else format(16 + int(line[1]), '04b')
            
            f.write(str('11') + str(rx) + str(imm) + '\n')
            currentline += 1

        # = = = = ADD = = = = = = 
        elif (line[0:3] == "add"):
            line = line.replace("add", "")
            line = line.split(",")
            
            rx = format(int(line[0]), '02b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            ry = format(int(line[1]), '02b')
            
            f.write(str('0100') + str(rx) + str(ry) + '\n')
            currentline += 1

        # = = = = FUNC = = = = = = 
        elif (line[0:4] == "func"):
            line = line.replace("func", "")
            line = line.split(",")
            
            rx = format(int(line[0]), '02b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            ry = format(int(line[1]), '02b')
            rz = format(int(line[2]), '02b')
            
            f.write(str('00') + str(rx) + str(ry) + str(rz) + '\n')
            currentline += 1

        # = = = = INIT = = = = = = 
        elif (line[0:4] == "init"):          
            line = line.replace("init", "")
            line = line.split(",")
            
            rx = format(int(line[0]), '02b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '04b')
            
            f.write(str('00') + str(rx) + str(imm) + '\n')
            currentline += 1

        # = = = = bnezR2 = = = = = = = = = 
        elif (line[0:6] == "bnezR2"):
            line = line.replace("bnezR2", "")
            line = line.split(",")

            imm = format(int(line[0]), '04b') if (int(line[0]) >= 0) else format(16 + int(line[0]), '04b')
           
            f.write(str('1011') + str(imm) + '\n')
            currentline += 1

        # = = = = LUIR1 = = = = = = 
        elif (line[0:5] == "luiR1"):          
            line = line.replace("luiR1", "")
            line = line.split(",")
            
            imm = format(int(line[0]), '04b')
            
            f.write(str('0110') + str(imm) + '\n')
            currentline += 1

        # = = = = ORIR1 = = = = = = 
        elif (line[0:5] == "oriR1"):          
            line = line.replace("oriR1", "")
            line = line.split(",")
            
            imm = format(int(line[0]), '04b')
            
            f.write(str('0111') + str(imm) + '\n')
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