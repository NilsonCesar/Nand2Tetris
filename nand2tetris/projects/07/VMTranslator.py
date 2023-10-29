import sys

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
    def __init__(self, vm_operations):
        self.vm_operations = vm_operations
    
    def translate(self):
        self.asm_code = []
        for vm_operation in self.vm_operations:
            if vm_operation[0] == "add":
                self.asm_code += self.add_asm_code()
            if vm_operation[0] == "sub":
                self.asm_code += self.sub_asm_code()
            if vm_operation[0] == "neg":
                self.asm_code += self.neg_asm.code()
            if vm_operation[0] == "eq":
                self.asm_code += self.eq_asm_code(len(self.asm_code) + 1)
            if vm_operation[0] == "gt":
                self.asm_code += self.gt_asm_code(len(self.asm_code) + 1)
            if vm_operation[0] == "lt":
                self.asm_code += self.lt_asm_code(len(self.asm_code) + 1)
            if vm_operation[0] == "and":
                self.asm_code += self.and_asm_code()
            if vm_operation[0] == "or":
                self.asm_code += self.or_asm_code()
            if vm_operation[0] == "not":
                self.asm_code += self.not_asm_code()
            if vm_operation[0] == "push" and vm_operation[1] == "constant":
                self.asm_code += self.push_const_asm_code(int(vm_operation[2]))
            if vm_operation[0] == "push" and vm_operation[1] == "local":
                self.asm_code += self.push_latt_asm_code("LCL", int(vm_operation[2]), len(self.asm_code) + 1)
            if vm_operation[0] == "push" and vm_operation[1] == "argument":
                self.asm_code += self.push_latt_asm_code("ARG", int(vm_operation[2]), len(self.asm_code) + 1)
            if vm_operation[0] == "push" and vm_operation[1] == "this":
                self.asm_code += self.push_latt_asm_code("THIS", int(vm_operation[2]), len(self.asm_code) + 1)
            if vm_operation[0] == "push" and vm_operation[1] == "that":
                self.asm_code += self.push_latt_asm_code("THAT", int(vm_operation[2]), len(self.asm_code) + 1)
            if vm_operation[0] == "pop" and vm_operation[1] == "local":
                self.asm_code += self.pop_latt_asm_code("LCL", int(vm_operation[2]), len(self.asm_code) + 1)

    def find_addr(self, pointer, i, act_line):
        return [f"@{pointer}", "D=A", "@addr", "M=D", f"@{i}", "D=A", "@i", "M=D", "D=M", f"@{20 + act_line}", "D;JEQ", "@addr", "M=M+1", "@i", "M=M-1", "D=M", f"@{20 + act_line}", "D;JEQ", f"@{11 + act_line}", "0;JMP"]

    def push_in_stack(self):
        return ["@addr", "A=M", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def pop_in_stack(self):
        return ["@SP", "M=M-1", "A=M", "D=M", "@addr", "A=M", "M=D"]

    def add_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M+D", "@SP", "M=M+1"]
    
    def sub_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M-D", "@SP", "M=M+1"]

    def neg_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "M=-M", "@SP", "M=M+1"]

    def eq_asm_code(self, act_line):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M-D", f"@{13 + act_line}", "D;JEQ", "D=0", f"@{14 + act_line}", "0;JMP", "D=1", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def gt_asm_code(self, act_line):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M-D", f"@{13 + act_line}", "D;JGT", "D=0", f"@{14 + act_line}", "0;JMP", "D=1", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    
    def lt_asm_code(self, act_line):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M-D", f"@{13 + act_line}", "D;JLT", "D=0", f"@{14 + act_line}", "0;JMP", "D=1", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def and_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M&D", "@SP", "M=M+1"]

    def or_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M|D", "@SP", "M=M+1"]

    def neg_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "M=!M", "@SP", "M=M+1"]

    def push_const_asm_code(self, i):
        return [f"@{i}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def push_latt_asm_code(self, pointer, i, act_line):
        return self.find_addr(pointer, i, act_line) + self.push_in_stack()
    
    def pop_latt_asm_code(self, pointer, i, act_line):
        return self.find_addr(pointer, i, act_line) + self.pop_in_stack()

if __name__ == "__main__":
    file_path = sys.argv[1]
    program = open(file_path).readlines()
    parser = Parser(program)
    print([1, 2] + [3, 4])