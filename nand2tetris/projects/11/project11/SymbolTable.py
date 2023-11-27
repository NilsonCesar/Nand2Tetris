class SymbolTable:
    def __init__(self):
        self.sb_class_level = dict()
        self.static_vars = 0
        self.field_vars = 0
        self.arg_vars = 0
        self.local_vars = 0

    def startSubroutine(self):
        self.sb_subroutine_level = dict()
        self.arg_vars = 0
        self.local_vars = 0
    
    def define(self, name, type, kind):
        if kind == 'STATIC' or kind == 'FIELD':
            self.sb_class_level[name] = [type, kind, self.varCount(kind)]
        else:
            self.sb_subroutine_level[name] = [type, kind, self.varCount(kind)]
        self.updateVarCount(kind)
    
    def varCount(self, kind):
        if kind == 'STATIC':
            return self.static_vars
        if kind == 'FIELD':
            return self.field_vars
        if kind == 'ARG':
            return self.arg_vars
        if kind == 'VAR':
            return self.local_vars
        return 0

    def updateVarCount(self, kind):
        if kind == 'STATIC':
            self.static_vars += 1
        if kind == 'FIELD':
            self.field_vars += 1
        if kind == 'ARG':
            self.arg_vars += 1
        if kind == 'VAR':
            self.local_vars += 1
    
    def kindOf(self, name):
        if name in self.sb_class_level.keys():
            kind = self.sb_class_level[name][1]
            if kind == 'STATIC':
                return 'static'
            else:
                return 'field'
        elif name in self.sb_subroutine_level.keys():
            kind = self.sb_subroutine_level[name][1]
            if kind == 'ARG':
                return 'argument'
            else:
                return 'local'
        return 'NONE'

    def typeOf(self, name):
        if name in self.sb_class_level.keys():
            return self.sb_class_level[name][0]
        if name in self.sb_subroutine_level.keys():
            return self.sb_subroutine_level[name][0]
        return 'NONE'
    
    def indexOf(self, name):
        if name in self.sb_class_level.keys():
            return self.sb_class_level[name][2]
        if name in self.sb_subroutine_level.keys():
            return self.sb_subroutine_level[name][2]
        return -1