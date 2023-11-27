class VMWriter:
    def __init__(self, file_name):
        self.vm_comands = []
        self.file_name = file_name

    def writePush(self, segment, index):
        self.vm_comands += [f'push {segment} {index}']
    
    def writePop(self, segment, index):
        self.vm_comands += [f'push {segment} {index}']
    
    def writeArithmetic(self, command):
        self.vm_comands += [command]
    
    def writeLabel(self, label):
        self.vm_comands += [f'({label})']
    
    def writeGoto(self, label):
        self.vm_comands += [f'goto {label}']