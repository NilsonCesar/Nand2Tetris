filename = "asm"

asm = open(f"./Nand2Tetris/Nand2Tetris1/nand2tetris/projects/06/{filename}.asm")
lines = asm.readlines()

st_var = {}
st_dest = {}
st_comp = {}
st_jump = {}

def init_sts():
    init_st_var()
    init_st_dest()
    init_st_comp()
    init_st_jump()

def init_st_dest():
    st_dest["null"] = "000"
    st_dest["M"] = "001"
    st_dest["D"] = "010"
    st_dest["DM"] = "011"
    st_dest["A"] = "100"
    st_dest["AM"] = "101"
    st_dest["AD"] = "110"
    st_dest["ADM"] = "110"

def init_st_comp():
    st_comp["0"] = "0101010"
    st_comp["1"] = "0111111"
    st_comp["-1"] = "0111010"
    st_comp["D"] = "0001100"
    st_comp["A"] = "0110000"
    st_comp["!D"] = "0001101"
    st_comp["!A"] = "0110001"
    st_comp["-D"] = "0001111"
    st_comp["-A"] = "0110011"
    st_comp["D+1"] = "0011111"
    st_comp["A+1"] = "0110111"
    st_comp["D-1"] = "0001110"
    st_comp["A-1"] = "0110010"
    st_comp["D+A"] = "0000010"
    st_comp["D-A"] = "0010011"
    st_comp["A-D"] = "0000111"
    st_comp["D&A"] = "0000000"
    st_comp["D|A"] = "0010101"

    st_comp["M"] = "1110000"
    st_comp["!M"] = "1110001"
    st_comp["-M"] = "1110011"
    st_comp["M+1"] = "1110111"
    st_comp["M-1"] = "1110010"
    st_comp["D+M"] = "1000010"
    st_comp["D-M"] = "1010011"
    st_comp["M-D"] = "1000111"
    st_comp["D&M"] = "1000000"
    st_comp["D|M"] = "1010101"


def init_st_jump():
    st_jump["null"] = "000"
    st_jump["JGT"] = "001"
    st_jump["JEQ"] = "010"
    st_jump["JGE"] = "011"
    st_jump["JLT"] = "100"
    st_jump["JNE"] = "101"
    st_jump["JLE"] = "110"
    st_jump["JMP"] = "111"

def A_Instruction(line):
    bin_represent = "{0:b}".format(int(line))
    ans = "0" * (16 - len(bin_represent)) + bin_represent
    print(ans)

# with open(f"Nand2Tetris/Nand2Tetris1/nand2tetris/projects/06/{filename}.hack", "w") as file:
