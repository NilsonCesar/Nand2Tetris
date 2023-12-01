import sys, os, CompilationEngine

class JackCompiler:
    VOID_OS_FUNCTIONS = ['String.dispose', 'String.setCharAt', 'String.eraseLastChar', 'String.setInt', 'Array.dispose', 'Output.moveCursor', 'Output.printChar', 'Output.printString', 'Output.printInt', 'Output.println', 'Output.backSpace', 'Screen.clearScreen', 'Screen.setColor', 'Screen.drawPixel', 'Screen.drawLine', 'Screen.drawRectangle', 'Screen.drawCircle', 'Memory.poke', 'Memory.deAlloc', 'Sys.halt', 'Sys.error', 'Sys.wait']

    def __init__(self):
        self.methods = []
        self.void = []
        self.dests = []
        self.vm_codes = []

    def compile(self, file_path, last = True):
        program = open(file_path).readlines()
        compilationEngine = CompilationEngine.CompilationEngine(program)
        vm_instructions = compilationEngine.compileTokens()
        self.methods += compilationEngine.method_functions
        self.void += compilationEngine.void_functions
        self.dests.append(file_path[:-4] + 'vm')
        self.vm_codes.append(vm_instructions)
        if last:
            self.checkCrossCall()
            for i in range(len(self.vm_codes)):
                self.writeProgram(self.vm_codes[i], self.dests[i])
    
    def isCall(self, instruction):
        return len(instruction) > 4 and instruction[:4] == 'call'

    def isMethod(self, signature):
        return signature in self.methods

    def isVoid(self, signature):
        return signature in self.void or signature in JackCompiler.VOID_OS_FUNCTIONS
    
    def checkCrossCall(self):
        for vm_code in self.vm_codes:
            for i in range(len(vm_code)):
                if self.isCall(vm_code[i]):
                    call_pieces = vm_code[i].split()
                    if self.isMethod(call_pieces[1]):
                        n = int(call_pieces[3])
                        vm_code[i] = vm_code[i][-1] + f'{n + 1}'
                        vm_code = vm_code[:i - n] + ['push pointer 0'] + vm_code[i - n:]
                    if self.isVoid(call_pieces[1]):
                        vm_code = vm_code[:i + 1] + ['pop temp 0'] + vm_code[i + 1:]


    def writeProgram(self, vm_instructions, dest):
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
            if len(file.path) >= 4 and file.path[-4:] == 'jack':
                jackFiles.append(file.path)
        
        for i in range(len(jackFiles)):
            jackCompiler.compile(jackFiles[i], i == len(jackFiles) - 1)