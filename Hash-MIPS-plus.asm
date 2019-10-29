init255
addi $1, 1
loop:
func $1, $3, 0xFA19E366
addi $1, 1
bne $1, $2, loop
