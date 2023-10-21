filename = "asm"

asm = open(f"./Nand2Tetris/Nand2Tetris1/nand2tetris/projects/06/{filename}.asm")
lines = asm.readlines()

sb = {}

def A_Instruction(line):
    bin_represent = "{0:b}".format(int(line))
    ans = "0" * (16 - len(bin_represent)) + bin_represent
    print(ans)

# with open(f"Nand2Tetris/Nand2Tetris1/nand2tetris/projects/06/{filename}.hack", "w") as file:
