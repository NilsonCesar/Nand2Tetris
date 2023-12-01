class VMWriter:
    def __init__(self):
        self.vm_comands = []

    def writePush(self, segment, index):
        self.vm_comands += [f'push {segment} {index}']
    
    def writePop(self, segment, index):
        self.vm_comands += [f'pop {segment} {index}']
    
    def writeArithmetic(self, command, unary = False):
        if command == '+':
            self.vm_comands += ['add']
        if command == '-':
            if unary:
                self.vm_comands += ['not']
            else:
                self.vm_comands += ['sub']
        if command == '*':
            self.writeCall('Math.multiply', 2)
        if command == '/':
            self.writeCall('Math.divide', 2)
        if command == '&amp;':
            self.vm_comands += ['and']
        if command == '|':
            self.vm_comands += ['or']
        if command == '&lt;':
            self.vm_comands += ['lt']
        if command == '&gt;':
            self.vm_comands += ['gt']
        if command == '=':
            self.vm_comands += ['eq']
        if command == '~':
            self.vm_comands += ['not']
    
    def writeLabel(self, label):
        self.vm_comands += [f'label {label}']
    
    def writeGoto(self, label):
        self.vm_comands += [f'goto {label}']

    def writeIf(self, label):
        self.vm_comands += [f'if-goto {label}']

    def writeCall(self, name, nVars):
        self.vm_comands += [f'call {name} {nVars}']
    
    def writeFunction(self, name, nVars):
        self.vm_comands += [f'function {name} {nVars}']
    
    def writeReturn(self):
        self.vm_comands += ['return']