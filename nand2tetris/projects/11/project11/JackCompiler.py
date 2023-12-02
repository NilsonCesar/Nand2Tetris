import sys, os, CompilationEngine

class JackCompiler:
    VOID_OS_FUNCTIONS = ['String.dispose', 'String.setCharAt', 'String.eraseLastChar', 'String.setInt', 'Array.dispose', 'Output.moveCursor', 'Output.printChar', 'Output.printString', 'Output.printInt', 'Output.println', 'Output.backSpace', 'Screen.clearScreen', 'Screen.setColor', 'Screen.drawPixel', 'Screen.drawLine', 'Screen.drawRectangle', 'Screen.drawCircle', 'Memory.poke','Memory.deAlloc', 'Sys.halt', 'Sys.error', 'Sys.wait']

    OS_FUNCTIONS = ['Math.abs', 'Math.multiply', 'Math.divide', 'Math.min', 'Math.max', 'Math.sqrt', 'String.new', 'String.dispose', 'String.length', 'String.charAt', 'String.setCharAt', 'String.appendChar','String.eraseLastChar', 'String.intValue', 'String.setInt', 'String.backSpace', 'String.doubleQuote', 'String.newLine', 'Array.new', 'Array.dispose', 'Output.moveCursor', 'Output.printChar', 'Output.printString', 'Output.printInt', 'Output.println', 'Output.backSpace', 'Screen.clearScreen', 'Screen.setColor', 'Screen.drawPixel', 'Screen.drawLine', 'Screen.drawRectangle', 'Screen.drawCircle', 'Keyboard.keyPressed', 'Keyboard.readChar', 'Keyboard.readLine', 'Keyboard.readInt', 'Memory.peek','Memory.poke', 'Memory.alloc', 'Memory.deAlloc', 'Sys.halt', 'Sys.error', 'Sys.wait']

    def __init__(self):
        self.functions = []
        self.void = []
        self.dests = []
        self.vm_codes = []
        self.class_names = []

    def compile(self, file_path, last = True):
        program = open(file_path).readlines()
        compilationEngine = CompilationEngine.CompilationEngine(program)
        vm_instructions = compilationEngine.compileTokens()
        self.functions += compilationEngine.class_functions
        self.void += compilationEngine.void_functions
        self.class_names.append(compilationEngine.label_name)
        self.dests.append(file_path[:-4] + 'vm')
        self.vm_codes.append(vm_instructions)
        if last:
            self.checkCrossCall()
            self.checkVoidCalls()
            self.updateArguments()
            for i in range(len(self.vm_codes)):
                self.writeProgram(self.vm_codes[i], self.dests[i])
    
    def updateArguments(self):
        for cur in range(len(self.vm_codes)):
            command = 0
            inMethod = False
            while command < len(self.vm_codes[cur]):
                commands = self.vm_codes[cur][command].split()
                
                if len(commands) < 3:
                    command += 1
                    continue

                if commands[0] == 'function':
                    command += 1
                    if self.vm_codes[cur][command] == 'push argument 0' and self.vm_codes[cur][command + 1] == 'pop pointer 0':
                            inMethod = True
                            command += 2
                    else:
                        inMethod = False

                commands = self.vm_codes[cur][command].split()

                if inMethod and commands[1] == 'argument':
                    commands[2] = str(int(commands[2]) + 1)
                    self.vm_codes[cur][command] = commands[0] + ' ' + commands[1] + ' ' + commands[2]
                
                command += 1


    def isCall(self, instruction):
        return len(instruction) > 4 and instruction[:4] == 'call'

    def isMethod(self, signature):
        return signature not in self.functions and signature not in JackCompiler.OS_FUNCTIONS

    def isVoid(self, signature):
        return signature in self.void or signature in JackCompiler.VOID_OS_FUNCTIONS
    
    def checkCrossCall(self):
        done = []
        v = 0
        for vm_code in self.vm_codes:
            num_inst = len(vm_code)
            i = 0
            while i < num_inst:
                if self.isCall(vm_code[i]):
                    call_pieces = vm_code[i].split()
                    if self.isMethod(call_pieces[1]) and call_pieces[1] not in done:
                        n = int(call_pieces[2])
                        if call_pieces[1][call_pieces[1].find('.') + 1:] != 'new' and call_pieces[1][:call_pieces[1].find('.')] not in self.class_names:
                            done.append(call_pieces[1])
                            vm_code[i] = vm_code[i][:-1] + f'{n + 1}'
                            vm_code = vm_code[:i - n] + ['push argument 0', 'pop pointer 0'] + vm_code[i - n:]
                            num_inst += 2
                i += 1
            self.vm_codes[v] = vm_code
            v += 1

    def checkVoidCalls(self):
        for v in range(len(self.vm_codes)):
            n = len(self.vm_codes[v])
            i = 0
            while i < n:
                if self.isCall(self.vm_codes[v][i]):
                    call_parts = self.vm_codes[v][i].split()
                    if self.isVoid(call_parts[1]):
                        self.vm_codes[v] = self.vm_codes[v][:i + 1] + ['pop temp 0'] + self.vm_codes[v][i + 1:]
                        n += 1
                i += 1



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