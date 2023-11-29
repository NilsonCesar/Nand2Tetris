import sys, os, CompilationEngine

class JackCompiler:
    def __init__(self, program_path):
        self.program_path = program_path
        self.compilationEngine = CompilationEngine.CompilationEngine(program_path)

    def compile(self):
        vm_output = self.compilationEngine.compileTokens()
        return vm_output

def compileProgram(file_path):
    compiler = JackCompiler(file_path)
    vm_instructions = compiler.compile()
    dest = file_path[:-4] + 'vm'
    
    with open(dest, 'w') as file:
        for instruction in vm_instructions:
            file.write(instruction)
            file.write('\n')

if __name__ == 'main':
    path = sys.argv[1]

    if len(path) >= 4 and path[-4:] == 'jack':
        compileProgram(path)
    else:
        if path[-1] != '/':
            path += '/'
        files = os.scandir(path)

        for file in files:
            if len(path) >= 4 and file[-4:] == 'jack':
                compileProgram(path)

