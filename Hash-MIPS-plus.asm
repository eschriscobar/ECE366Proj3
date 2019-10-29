init255
addi $1, 1
loop:
func $1, $3, 0xFA
addi $1, 1
bne $1, $0, -3
