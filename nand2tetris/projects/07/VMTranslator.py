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

    def add_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M+D", "@SP", "M=M+1"]
    
    def sub_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M-D", "@SP", "M=M+1"]

    def neg_asm_code(self):
        return ["@SP", "M=M-1", "A=M", "M=-M", "@SP", "M=M+1"]

    def eq_asm_code(self, act_line):
        return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M-D", f"@{13 + act_line}", "D;JEQ", "D=0", f"@{14 + act_line}", "0;JMP", "D=1", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

if __name__ == "__main__":
    file_path = sys.argv[1]
    program = open(file_path).readlines()
    parser = Parser(program)
    print([1, 2] + [3, 4])