def saveJumpLabel(asm,labelIndex, labelName, labelAddr):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index\
            labelAddr.append(lineCount*4)
            #asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def regNameInit(regName):
    i = 0
    while i<=23:
        regName.append(str(i))
        i = i + 1
    regName.append('lo')
    regName.append('hi')
    
def rshift(val, n):
    #x = 1
    return val>>n

def hash(A,B,pattern_Reg, MEM, regval):
    #first fold (down to 32 bits)
    C = B*A
    C_hi = C >> 32
    C_low = C & 0x00000000FFFFFFFF
    C = C_hi^C_low
    
    #Second fold (down to 16 bits)
    C = B*C
    C_hi = C >> 32
    C_low = C & 0x00000000FFFFFFFF
    C = C_hi^C_low

    #third fold
    C = B*C
    C_hi = C >> 32
    C_low = C & 0x00000000FFFFFFFF
    C = C_hi^C_low

    #fourth fold
    C = B*C
    C_hi = C >> 32
    C_low = C & 0x00000000FFFFFFFF
    C = C_hi^C_low

    #fifth fold
    C = B*C
    C_hi = C >> 32
    C_low = C & 0x00000000FFFFFFFF
    C = C_hi^C_low

    #Down to 16 bits
    C_hi = C >> 16
    C_low = C & 0x0000FFFF
    C = C_hi^C_low

    #Down to 8 bits
    C_hi = C >> 8
    C_low = C & 0x00FF
    C = C_hi^C_low

    MEM[0x2020 + (A - 1)] = C

    #pattern match
    if('11111' in str(bin(C))):
        regval[pattern_Reg] += 1
        #place in memory incremented by one

    if(A == 100):
        MEM[0x2008] = regval[pattern_Reg]

    



def main():
    
    MEM = [0]*12288 #intialize array to all 0s for 0x3000 indices
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    regNameInit(regName)
    regval = [0]*26 #0-23 and lo, hi
    LO = 24
    HI = 25
    good_in = False
    while(good_in == False):
        file_Name = input("Please type file name, enter for default, or q to quit:")
        if(file_Name == "q"):
           print("Bye!")
           return
        if(file_Name == "\n"):
            file_Name = "mips1.asm"
        try:
            f = open(file_Name)
            f.close()
            good_in = True
        except FileNotFoundError:
            print('File does not exist')
    
    f = open("mc.txt","w+")
    h = open(file_Name,"r")

    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName, labelAddr) # Save all jump's destinations

    #for lineCount in len(asm):
    lineCount = 0
    while(lineCount < len(asm)):

        line = asm[lineCount]
        f.write('------------------------------ \n')
        if(not(':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        
        if(line[0:4] == "addi"): # ADDI, $t = $s + imm; advance_pc (4); addi $t, $s, imm
            #f.write(line)
            line = line.replace("addi","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] + int(line[2])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            
        #hash and pattern
        elif(line[0:4]=="func"):
            line = line.replace("func","")
            line = line.split(",")
            A = regval[int(line[0])]
            pattern_Reg = int(line[1])
            B = int(line[2], 16)
            hash(A, B, pattern_Reg, MEM, regval)

        #bne
        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne","")
            line = line.split(",")
            if(regval[int(line[0])]!=regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = line[2]
                    lineCount = line[2]
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')
        
        lineCount = lineCount + 1
        
    #print final results
    #print(hex(MEM[0x2000]))
    #print(hex(MEM[0x2004]))
    #print(hex(MEM[0x2008]))
    ("REGISTERS:")
    print("-----------")
    for x in range(len(regval)):
        if(x == 24):
            print("lo: ", hex(regval[x]))
        elif(x == 25):
            print("hi: ", hex(regval[x]))
        else:
            print("$", x,": ", hex(regval[x]))
    print("PC: ", hex(PC))

    print("\n")
    print("Used Memory values:\n")
    print("            ", end="")
    for x in range(0,8,1):
        print("0x"+ format((x*4),"08x"), end=" ")
    print("\n")
    print("--------------------------------------------------------------------------------------------------",end="")
    count = 0
    print("\n")
    for x in range(0x2003,0x2100,4):
        if((x-0x3)%0x20==0):
            print("0x"+format(x-0x3,"08x") + '|', end=" ")
        print("0x", end="")
        for y in range(0,4,1):
            print(format(MEM[x-y], "02x"), end="")
        print(" ", end = "")
        count += 1
        if(count == 8):
            count = 0
            print("\n")

    f.close()

if __name__ == "__main__":
    main()
