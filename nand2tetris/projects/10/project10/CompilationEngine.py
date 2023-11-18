class CompilationEngine():
    def __init__(self, tokens):
        self.tokens = tokens[1:-1]
        self.actToken = 0
    
    def get_current_token(self):
        return self.tokens[self.actToken]

    def get_current_token_value(self):
        return self.get_element_value(self.get_current_token())

    def make_space(self, sps):
        return ['  ' * sps]
    
    def eat(self, sps):
        exp = self.make_space(sps) + self.get_current_token()
        self.actToken += 1
        return exp
    
    def multEat(self, sps, n):
        result = []
        for i in range(n):
            result += self.eat(sps)
        return result

    def get_element_type(self, token):
        first_lt = token.find('<')
        first_gt = token.find('>')
        return token[first_lt + 1 : first_gt]

    def get_element_value(self, token):
        second_lt = token[1:].find('<')
        first_gt = token.find('>')
        return token[first_gt + 2: second_lt]
    
    def compileClass(self, sps):
        result = ['  ' * sps]+ ['<class>']
        result += self.multEat(sps + 1, 3)
        while self.get_current_token_value() in ['static', 'field']:
            result += self.compileClassVarDec(sps + 1)
        while self.get_current_token_value() in ['constructor', 'function', 'method']:
            result += self.compileSubroutine(sps + 1)
        result += self.eat(sps + 1)
        result += ['  ' * sps] + ['</class>']
        return result

    def compileClassVarDec(self, sps):
        result = ['  ' * sps] + ['<classVarDec>']
        result += self.multEat(sps + 1, 3)
        while self.get_current_token_value() == ',':
            result += self.multEat(sps + 1, 2)
        result += self.eat(sps + 1)
        result += ['  ' * sps] + ['</classVarDec>']
        return result
    
    def compileSubroutine(self, sps):
        result = ['  ' * sps] + ['<subroutineDec>']
        result += self.multEat(sps + 1, 4)
        while self.get_current_token_value() != ')':
            result += self.multEat(sps + 1, 2)
            if self.get_current_token_value() == ',':
                result += self.eat(sps + 1)
        result += self.eat(sps + 1)
        result += self.compileSubroutineBody(sps + 1)
        result += ['  ' * sps] + ['</subroutineDec>']
        return result
    
    def compileSubroutineBody(self, sps):
        result = ['  ' * sps] + ['<subroutineBody>']
        result += self.eat(sps + 1)
        while self.get_current_token_value() == 'var':
            result += self.compileVarDec(sps + 1)
        result += self.compileStatements(sps + 1)
        result += self.eat(sps + 1)
        result = ['  ' * sps] + ['</subroutineBody>']
        return result

    def compileVarDec(self, sps):
        result = ['  ' * sps] + ['<varDec>']
        result += self.multEat(sps + 1, 3)
        while self.get_current_token_value() == ',':
            result += self.multEat(sps + 1, 2)
        result += self.eat(sps + 1)
        result += ['  ' * sps] + ['</varDec>']
        return result
    

test = CompilationEngine([])
print(test.get_element_value("<keyword> class </keyword>"))