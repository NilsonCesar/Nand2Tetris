filename = "Pong"
folder = "pong"

asm = open(f"./Nand2Tetris/Nand2Tetris1/nand2tetris/projects/06/{folder}/{filename}.asm")
lines = asm.readlines()
second_program = []
to_assembly = []
machine_code = []

st_var = {}
st_dest = {}
st_comp = {}
st_jump = {}

# A function, considering an addr in decimal base
def A_Instruction(addr):
    bin_represent = "{0:b}".format(int(addr))
    ans = "0" * (16 - len(bin_represent)) + bin_represent
    return ans

# C function
def C_Instruction(line):
    dest = line.find('=')
    jump = line.find(';')

    if dest == -1:
        l = 0
    else:
        l = dest + 1
    if jump == -1:
        r = len(line)
    else:
        r = jump

    comp = line[l:r]

    if dest == -1:
        dest = st_dest["null"]
    else:
        dest = st_dest[line[:dest]]
    if jump == -1:
        jump = st_jump["null"]
    else:
        jump = st_jump[line[jump + 1:]]

    return "111" + st_comp[comp] + dest + jump

# Functions that initiate the symbol tables
def init_sts():
    init_st_var()
    init_st_dest()
    init_st_comp()
    init_st_jump()

def init_st_var():
    st_var["R0"] = "0"
    st_var["R1"] = "1"
    st_var["R2"] = "2"
    st_var["R3"] = "3"
    st_var["R4"] = "4"
    st_var["R5"] = "5"
    st_var["R6"] = "6"
    st_var["R7"] = "7"
    st_var["R8"] = "8"
    st_var["R9"] = "9"
    st_var["R10"] = "10"
    st_var["R11"] = "11"
    st_var["R12"] = "12"
    st_var["R13"] = "13"
    st_var["R14"] = "14"
    st_var["R15"] = "15"
    st_var["SCREEN"] = "16384"
    st_var["KBD"] = "24576"
    st_var["SP"] = "0"
    st_var["LCL"] = "1"
    st_var["ARG"] = "2"
    st_var["THIS"] = "3"
    st_var["THAT"] = "4"

def init_st_dest():
    st_dest["null"] = "000"
    st_dest["M"] = "001"
    st_dest["D"] = "010"
    st_dest["DM"] = "011"
    st_dest["MD"] = "011"
    st_dest["A"] = "100"
    st_dest["AM"] = "101"
    st_dest["MA"] = "101"
    st_dest["AD"] = "110"
    st_dest["DA"] = "110"
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

# Check if some variable are in st_var
def var_exists(var):
    return not (st_var.get(var) == None)

# Format line to strip white space and ignore comments
def format_line(line):
    ans = line
    slash_idx = line.find("//")

    if slash_idx != -1:
        ans = line[:slash_idx]
    ans = ans.strip()

    return ans

# Return the address memorie taken as input v, where v is the number/symbol in @v
# If he should, the env will be added with a new variable v
def manipulate_memory(value, pointer, mem=-1):
    try:
        addr = int(value)
        return [addr, 0]
    except:
        if var_exists(value):
            return [st_var[value], 0]
        else:
            if mem == -1:
                st_var[value] = pointer
                pointer += 1
            else:
                st_var[value] = mem
        return [pointer, 1]

init_sts()

def first_pass(lines):
    counter = 0
    for line in lines:
        fline = format_line(line)

        if fline != "" and fline[0] == "(":
            second_parethesis = fline.find(")")
            manipulate_memory(fline[1:second_parethesis], 0, counter)
        elif fline != "":
            second_program.append(fline)
            counter += 1

def second_pass(program):
    pointer = 16
    for line in program:
        new_line = ""
        if line[0] == "@":
            v = manipulate_memory(line[1:], pointer)
            if v[1] == 1:
                pointer = v[0]
                new_line = "@" + str(pointer - 1)
            else:
                new_line = "@" + str(v[0])
        else:
            new_line = line
        to_assembly.append(new_line)

def assembly(assembly_code):
    for line in assembly_code:
        new_line = ""
        if line[0] == "@":
            new_line = A_Instruction(line[1:])
        else:
            new_line = C_Instruction(line)
        machine_code.append(new_line)

first_pass(lines)
second_pass(second_program)
assembly(to_assembly)

with open(f"Nand2Tetris/Nand2Tetris1/nand2tetris/projects/06/{folder}/{filename}.hack", "w") as file:
    for line in machine_code:
        file.write(line)
        file.write("\n")
