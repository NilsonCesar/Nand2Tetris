import sys, os, CompilationEngine

class JackCompiler:
    void_os_functions = ['String.dispose', 'String.setCharAt', 'String.eraseLastChar', 'String.setInt', 'Array.dispose', 'Output.moveCursor', 'Output.printChar', 'Output.printString', 'Output.printInt', 'Output.println', 'Output.backSpace', 'Screen.clearScreen', 'Screen.setColor', 'Screen.drawPixel', 'Screen.drawLine', 'Screen.drawRectangle', 'Screen.drawCircle', 'Memory.poke', 'Memory.deAlloc', 'Sys.halt', 'Sys.error', 'Sys.wait']

    def __init__(self):
        self.methods = []
        self.void = []
        self.dests = []
        self.vm_codes = []

    def compile(self, file_path, last = True):
        program = open(file_path).readlines()
        compilationEngine = CompilationEngine.CompilationEngine(program)
        vm_instructions = CompilationEngine.compileTokens()
        self.methods += compilationEngine.method_functions
        self.void += compilationEngine.void_functions
        self.dests.append(file_path[:-4] + 'vm')
        self.vm_codes.append(vm_instructions)
        if last:
            self.checkCrossCall()
            for i in range(len(self.vm_codes)):
                self.writeProgram(self.vm_codes[i], self.dests[i])
    
    def writeProgram(vm_instructions, dest):
        with open(dest, 'w') as file:
            for instruction in vm_instructions:
                file.write(instruction)
                file.write('\n')


if __name__ == '__main__':
    jackCompiler = JackCompiler()
    path = sys.argv[1]

    if len(path) >= 4 and path[-4:] == 'jack':
        jackCompiler.compile(path)
    else:
        if path[-1] != '/':
            path += '/'
        files = os.scandir(path)
        jackFiles = []

        for file in files:
            if len(file) >= 4 and file[-4:] == 'jack':
                jackFiles.append(file.path)
        
        for i in range(len(jackFiles)):
            jackCompiler.compile(jackFiles, i == len(jackFiles) - 1)