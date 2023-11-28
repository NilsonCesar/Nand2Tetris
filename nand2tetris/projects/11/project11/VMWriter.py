class VMWriter:
    def __init__(self):
        self.vm_comands = []

    def writePush(self, segment, index):
        self.vm_comands += [f'push {segment} {index}']
    
    def writePop(self, segment, index):
        self.vm_comands += [f'pop {segment} {index}']
    
    def writeArithmetic(self, command):
        self.vm_comands += [command]
    
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