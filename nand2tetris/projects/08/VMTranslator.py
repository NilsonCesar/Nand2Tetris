import sys, os

class Parser():
    def __init__(self, program):
        self.lines = self.format_lines(program)
    
    def format_lines(self, program):
        lines = []
        for line in program:
            ans = line
            slash_idx = line.find("//")

            if slash_idx != -1:
                ans = line[:slash_idx]
            ans = ans.strip()

            if ans != "":
                lines.append(ans)
        return lines

    def take_operations(self):
        operations = []
        for operation in self.lines:
            operation_parts = operation.split()
            operations.append(operation_parts)
        return operations

class CodeWriter():
    def __init__(self, vm_operations, name_file, asm_code, op):
        self.vm_operations = vm_operations
        self.name_file = name_file
        self.asm_code = asm_code
        self.op = op
    
    def translate_to_asm(self):
        count = len(self.asm_code) - self.op
        actual_function = ""
        current_i = 1
        for vm_operation in self.vm_operations:
            self.asm_code += ["// " + " ".join(vm_operation)]
            self.op += 1
            if vm_operation[0] == "add":
                self.asm_code += self.add_asm_code()
            if vm_operation[0] == "sub":
                self.asm_code += self.sub_asm_code()
            if vm_operation[0] == "neg":
                self.asm_code += self.neg_asm_code()
            if vm_operation[0] == "eq":
                self.asm_code += self.eq_asm_code(count + 1)
            if vm_operation[0] == "gt":
                self.asm_code += self.gt_asm_code(count + 1)
            if vm_operation[0] == "lt":
                self.asm_code += self.lt_asm_code(count + 1)
            if vm_operation[0] == "and":
                self.asm_code += self.and_asm_code()
            if vm_operation[0] == "or":
                self.asm_code += self.or_asm_code()
            if vm_operation[0] == "not":
                self.asm_code += self.not_asm_code()
            if vm_operation[0] == "push" and vm_operation[1] == "constant":
                self.asm_code += self.push_const_asm_code(int(vm_operation[2]))
            if vm_operation[0] == "push" and vm_operation[1] == "local":
                self.asm_code += self.push_latt_asm_code("LCL", int(vm_operation[2]), count + 1)
            if vm_operation[0] == "push" and vm_operation[1] == "argument":
                self.asm_code += self.push_latt_asm_code("ARG", int(vm_operation[2]), count + 1)
            if vm_operation[0] == "push" and vm_operation[1] == "this":
                self.asm_code += self.push_latt_asm_code("THIS", int(vm_operation[2]), count + 1)
            if vm_operation[0] == "push" and vm_operation[1] == "that":
                self.asm_code += self.push_latt_asm_code("THAT", int(vm_operation[2]), count + 1)
            if vm_operation[0] == "push" and vm_operation[1] == "static":
                self.asm_code += self.push_static_asm_code(int(vm_operation[2]))
            if vm_operation[0] == "push" and vm_operation[1] == "temp":
                self.asm_code += self.push_temp_asm_code(int(vm_operation[2]))
            if vm_operation[0] == "push" and vm_operation[1] == "pointer" and vm_operation[2] == "0":
                self.asm_code += self.push_pointer("THIS")
            if vm_operation[0] == "push" and vm_operation[1] == "pointer" and vm_operation[2] == "1":
                self.asm_code += self.push_pointer("THAT")
            if vm_operation[0] == "pop" and vm_operation[1] == "local":
                self.asm_code += self.pop_latt_asm_code("LCL", int(vm_operation[2]), count + 1)
            if vm_operation[0] == "pop" and vm_operation[1] == "argument":
                self.asm_code += self.pop_latt_asm_code("ARG", int(vm_operation[2]), count + 1)
            if vm_operation[0] == "pop" and vm_operation[1] == "this":
                self.asm_code += self.pop_latt_asm_code("THIS", int(vm_operation[2]), count + 1)
            if vm_operation[0] == "pop" and vm_operation[1] == "that":
                self.asm_code += self.pop_latt_asm_code("THAT", int(vm_operation[2]), count + 1)
            if vm_operation[0] == "pop" and vm_operation[1] == "static":
                self.asm_code += self.pop_static_asm_code(int(vm_operation[2]))
            if vm_operation[0] == "pop" and vm_operation[1] == "temp":
                self.asm_code += self.pop_temp_asm_code(int(vm_operation[2]))
            if vm_operation[0] == "pop" and vm_operation[1] == "pointer" and vm_operation[2] == "0":
                self.asm_code += self.pop_pointer_asm_code("THIS")
            if vm_operation[0] == "pop" and vm_operation[1] == "pointer" and vm_operation[2] == "1":
                self.asm_code += self.pop_pointer_asm_code("THAT")
            if vm_operation[0] == "label":
                if actual_function == "":
                    self.asm_code += self.label_asm_code(vm_operation[1])
                else:
                    self.asm_code += self.label_asm_code(actual_function + "$" + vm_operation[1])
                self.op += 1
            if vm_operation[0] == "goto":
                if actual_function == "":
                    self.asm_code += self.goto_asm_code(vm_operation[1])
                else:
                    self.asm_code += self.goto_asm_code(actual_function + "$" + vm_operation[1])
            if vm_operation[0] == "if-goto":
                if actual_function == "":
                    self.asm_code += self.if_goto_asm_code(vm_operation[1])
                else:
                    self.asm_code += self.if_goto_asm_code(actual_function + "$" + vm_operation[1])
            if vm_operation[0] == "call":
                self.asm_code += self.call_asm_code(vm_operation[1], int(vm_operation[2]), actual_function + "$ret." + str(current_i), count + 1)
                current_i += 1
                self.op += 1
            if vm_operation[0] == "function":
                self.asm_code += self.function_asm_code(vm_operation[1], int(vm_operation[2]), count)
                self.op += 1 
                actual_function = vm_operation[1]
                current_i = 1
            if vm_operation[0] == "return":
                self.asm_code += self.return_asm_code()
            count = len(self.asm_code) - self.op
        return [self.asm_code, self.op]

    def find_addr(self, pointer, i, act_line):
        return [f"@{pointer}", "D=M", "@addr", "M=D", f"@{i}", "D=A", "@i", "M=D", "D=M", f"@{19 + act_line}", "D;JEQ", "@addr", "M=M+1", "@i", "M=M-1", "D=M", f"@{19 + act_line}", "D;JEQ", f"@{10 + act_line}", "0;JMP"]

    def push_in_stack(self):
        return ["@addr", "A=M", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def pop_in_stack(self):
        return ["@SP", "AM=M-1", "D=M", "@addr", "A=M", "M=D"]

    def add_asm_code(self):
        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=M+D", "@SP", "M=M+1"]
    
    def sub_asm_code(self):
        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=M-D", "@SP", "M=M+1"]

    def neg_asm_code(self):
        return ["@SP", "AM=M-1", "M=-M", "@SP", "M=M+1"]

    def eq_asm_code(self, act_line):
        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "D=M-D", f"@{11 + act_line}", "D;JEQ", "D=0", f"@{12 + act_line}", "0;JMP", "D=-1", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def gt_asm_code(self, act_line):
        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "D=M-D" , f"@{10 + act_line}", "D;JGT", "D=0", f"@{11 + act_line}", "0;JMP", "D=-1", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    
    def lt_asm_code(self, act_line):
        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "D=M-D", f"@{10 + act_line}", "D;JLT", "D=0", f"@{11 + act_line}", "0;JMP", "D=-1", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def and_asm_code(self):
        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=M&D", "@SP", "M=M+1"]

    def or_asm_code(self):
        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=M|D", "@SP", "M=M+1"]

    def not_asm_code(self):
        return ["@SP", "AM=M-1", "M=!M", "@SP", "M=M+1"]

    def push_const_asm_code(self, i):
        return [f"@{i}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def push_latt_asm_code(self, pointer, i, act_line):
        return self.find_addr(pointer, i, act_line) + self.push_in_stack()
    
    def push_static_asm_code(self, i):
        return [f"@{self.name_file}.{i}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    
    def push_temp_asm_code(self, i):
        return [f"@{5 + i}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def push_pointer(self, pointer):
        return [f"@{pointer}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    
    def pop_latt_asm_code(self, pointer, i, act_line):
        return self.find_addr(pointer, i, act_line) + self.pop_in_stack()

    def pop_static_asm_code(self, i):
        return ["@SP", "AM=M-1", "D=M", f"@{self.name_file}.{i}", "M=D"]
    
    def pop_temp_asm_code(self, i):
        return ["@SP", "AM=M-1", "D=M", f"@{5 + i}", "M=D"]
    
    def pop_pointer_asm_code(self, pointer):
        return ["@SP", "AM=M-1", "D=M", f"@{pointer}", "M=D"]

    def label_asm_code(self, label):
        return [f"({label})"]
    
    def goto_asm_code(self, label):
        return [f"@{label}", "0;JMP"]
    
    def if_goto_asm_code(self, label):
        return ["@SP", "AM=M-1", "D=M", f"@{label}", "D;JNE"]

    def call_asm_code(self, function_name, n_args, retAddrLabel, act_line):
        return [f"@{48 + act_line}", "D=A", f"@{retAddrLabel}", "M=D", "@SP", "A=M", "M=D", "@SP",
                "M=M+1", "@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                "@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1", "@THIS", "D=M",
                "@SP", "A=M", "M=D", "@SP", "M=M+1", "@THAT", "D=M", "@SP", "A=M",
                "M=D", "@SP", "M=M+1", f"@{5 + n_args}", "D=A", "@SP", "D=M-D", "@ARG",
                "M=D", "@SP", "D=M", "@LCL", "M=D"] + self.goto_asm_code(function_name) + [f"({retAddrLabel})"]

    def function_asm_code(self, function_name, n_vars, act_line):
        return self.label_asm_code(function_name) + [f"@{n_vars}", "D=A", "@i", "M=D", f"@{17 + act_line}", "D;JEQ"] + self.push_const_asm_code(0) + ["@i", "MD=M-1", f"@{4 + act_line}", "0;JMP"]

    def return_asm_code(self):
        return ["@LCL", "D=M", "@5", "D=D-A", "A=D", "D=M", "@retAddr", "M=D", 
                "@SP", "AM=M-1", "D=M", "@ARG", "A=M", "M=D", "@ARG",
                "D=M+1", "@SP", "M=D", "@LCL", "AM=M-1", "D=M",
                "@THAT", "M=D", "@LCL", "AM=M-1", "D=M", "@THIS", "M=D", "@LCL", "AM=M-1", "D=M",
                "@ARG", "M=D", "@LCL", "AM=M-1", "D=M", "@LCL", "M=D", "@retAddr", "A=M", "0;JMP"]

def find_name_file(dir):
    init = 0
    final = len(dir)

    for i in range(len(dir)):
        if dir[i] == '/':
            init = i + 1
        if dir[i] == '.':
            final = i

    return dir[init:final]

def find_folder_name(dir):
    last_slash = -1
    third_to_last_slash = -1
    if dir[len(dir) - 1] == "/":
        last_slash = len(dir) - 1
    
    if last_slash == -1:
        for i in range(len(dir)):
            if dir[i] == "/":
                last_slash = i
        return dir[last_slash + 1:]
    else:
        for i in range(len(dir) - 1):
            if dir[i] == "/":
                third_to_last_slash = i
        return dir[third_to_last_slash + 1: last_slash]

def VM_file_to_asm(file_path, asm_code, op):
    name_file = find_name_file(file_path)
    program = open(file_path).readlines()
    parser = Parser(program)
    operations = parser.take_operations()
    code_writer = CodeWriter(operations, name_file, asm_code, op)
    ans = code_writer.translate_to_asm()
    return ans

if __name__ == "__main__":
    path = sys.argv[1]
    asm_code = []
    if len(path) >= 2 and path[-2:] == "vm":
        ans = VM_file_to_asm(path, [], 0)
        asm_code = ans[0]
        dest = path[:-2] + "asm"
    else:
        if path[len(path) - 1] != "/":
            path += "/"
        has_sys = False
        entries = os.scandir(path)
        op = 0
        folder_name = find_folder_name(path)
        dest = path + folder_name + ".asm"
        for entry in entries:
            file = entry.name
            if file == "Sys.vm":
                has_sys = True
        entries = os.scandir(path)
        if has_sys:
            asm_code = ["@Sys.init", "0;JMP"]
            for entry in entries:
                file = entry.name
                if file[-2:] == "vm":
                    ans = VM_file_to_asm(path + file, asm_code, op)
                    asm_code = ans[0]
                    op = ans[1]
        else:
            asm_code = []
            for entry in entries:
                file = entry.name
                if file[-2:] == "vm":
                    asm_code = VM_file_to_asm(path + file, asm_code, op)

    with open(dest, 'w') as file:
        for line in asm_code:
            file.write(line + '\n')