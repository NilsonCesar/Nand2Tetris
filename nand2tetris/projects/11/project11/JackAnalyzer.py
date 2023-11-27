class JackAnalyzer():
    def __init__(self, tokens):
        self.tokens = tokens[1:-1]
        self.actToken = 0
    
    def has_more_tokens(self):
        return self.actToken < len(self.tokens)

    def get_current_token(self):
        return self.tokens[self.actToken]

    def get_current_token_value(self):
        if self.has_more_tokens():
            return self.get_element_value(self.get_current_token())
        return ''
    
    def get_current_element_type(self):
        return self.get_element_type(self.get_current_token())

    def make_space(self, sps, exp):
        return [str(exp)]
    
    def eat(self, sps):
        exp = self.make_space(sps, self.get_current_token())
        self.actToken += 1
        return exp
    
    def multEat(self, sps, n):
        result = []
        while n > 0:
            result += self.eat(sps)
            n -= 1
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
        result = self.make_space(sps, '<class>')
        result += self.multEat(sps + 1, 3)
        while self.get_current_token_value() in ['static', 'field']:
            result += self.compileClassVarDec(sps + 1)
        while self.get_current_token_value() in ['constructor', 'function', 'method']:
            result += self.compileSubroutine(sps + 1)
        result += self.eat(sps + 1)
        result += self.make_space(sps, '</class>')
        return result

    def compileClassVarDec(self, sps):
        result = self.make_space(sps, '<classVarDec>')
        result += self.multEat(sps + 1, 3)
        while self.get_current_token_value() == ',':
            result += self.multEat(sps + 1, 2)
        result += self.eat(sps + 1)
        result += self.make_space(sps, '</classVarDec>')
        return result
    
    def compileSubroutine(self, sps):
        result = self.make_space(sps, '<subroutineDec>')
        result += self.multEat(sps + 1, 4)
        result += self.compileParameterList(sps + 1)
        result += self.eat(sps + 1)
        result += self.compileSubroutineBody(sps + 1)
        result += self.make_space(sps, '</subroutineDec>')
        return result
    
    def compileParameterList(self, sps):
        result = self.make_space(sps, '<parameterList>')
        while self.get_current_token_value() in ['int', 'char', 'boolean'] or self.get_current_element_type() == 'identifier':
            result += self.multEat(sps + 1, 2)
            if self.get_current_token_value() == ',':
                result += self.eat(sps + 1)
        result += self.make_space(sps, '</parameterList>')
        return result

    def compileSubroutineBody(self, sps):
        result = self.make_space(sps, '<subroutineBody>')
        result += self.eat(sps + 1)
        while self.get_current_token_value() == 'var':
            result += self.compileVarDec(sps + 1)
        result += self.compileStatements(sps + 1)
        result += self.eat(sps + 1)
        result += self.make_space(sps, '</subroutineBody>')
        return result

    def compileVarDec(self, sps):
        result = self.make_space(sps, '<varDec>')
        result += self.multEat(sps + 1, 3)
        while self.get_current_token_value() == ',':
            result += self.multEat(sps + 1, 2)
        result += self.eat(sps + 1)
        result += self.make_space(sps, '</varDec>')
        return result

    def compileStatements(self, sps):
        result = self.make_space(sps, '<statements>')
        while self.get_current_token_value() in ['let', 'if', 'while', 'do', 'return']:
            statement = self.get_current_token_value()
            if statement == 'let':
                result += self.compileLet(sps + 1)
            if statement == 'if':
                result += self.compileIf(sps + 1)
            if statement == 'while':
                result += self.compileWhile(sps + 1)
            if statement == 'do':
                result += self.compileDo(sps + 1)
            if statement == 'return':
                result += self.compileReturn(sps + 1)
        result += self.make_space(sps, '</statements>')
        return result
    
    def compileLet(self, sps):
        result = self.make_space(sps, '<letStatement>')
        result += self.multEat(sps + 1, 2)
        if self.get_current_token_value() == '[':
            result += self.eat(sps + 1)
            result += self.compileExpression(sps + 1)
            result += self.eat(sps + 1)
        result += self.eat(sps + 1)
        result += self.compileExpression(sps + 1)
        result += self.eat(sps + 1)
        result += self.make_space(sps, '</letStatement>')
        return result
    
    def compileIf(self, sps):
        result = self.make_space(sps, '<ifStatement>')
        result += self.multEat(sps + 1, 2)
        result += self.compileExpression(sps + 1)
        result += self.multEat(sps + 1, 2)
        result += self.compileStatements(sps + 1)
        result += self.eat(sps + 1)
        if self.get_current_token_value() == 'else':
            result += self.multEat(sps + 1, 2)
            result += self.compileStatements(sps + 1)
            result += self.eat(sps + 1)
        result += self.make_space(sps, '</ifStatement>')
        return result

    def compileWhile(self, sps):
        result = self.make_space(sps, '<whileStatement>')
        result += self.multEat(sps + 1, 2)
        result += self.compileExpression(sps + 1)
        result += self.multEat(sps + 1, 2)
        result += self.compileStatements(sps + 1)
        result += self.eat(sps + 1)
        result += self.make_space(sps, '</whileStatement>')
        return result
    
    def compileDo(self, sps):
        result = self.make_space(sps, '<doStatement>')
        result += self.eat(sps + 1)
        result += self.compileTerm(sps)[1:-1]
        result += self.eat(sps + 1)
        result += self.make_space(sps, '</doStatement>')
        return result

    def compileReturn(self, sps):
        result = self.make_space(sps, '<returnStatement>')
        result += self.eat(sps + 1)
        if self.get_current_token_value() != ';':
            result += self.compileExpression(sps + 1)
        result += self.eat(sps + 1)
        result += self.make_space(sps, '</returnStatement>')
        return result
    
    def compileExpression(self, sps):
        result = self.make_space(sps, '<expression>')
        result += self.compileTerm(sps + 1)
        while self.get_current_token_value() in ['+', '-', '*', '/', '&', '|', '<', '>', '=', '&lt;', '&gt;', '&amp;', '&quot;']:
            result += self.eat(sps + 1)
            result += self.compileTerm(sps + 1)
        result += self.make_space(sps, '</expression>')
        return result
    
    def compileTerm(self, sps):
        result = self.make_space(sps, '<term>')
        if self.get_current_token_value() == '(':
            result += self.eat(sps + 1)
            result += self.compileExpression(sps + 1)
            result += self.eat(sps + 1)
        elif self.get_current_token_value() in ['-', '~']:
            result += self.eat(sps + 1)
            result += self.compileTerm(sps + 1)
        elif self.get_current_element_type() == 'integerConstant':
            result += self.eat(sps + 1)
        elif self.get_current_element_type() == 'stringConstant':
            result += self.eat(sps + 1)
        elif self.get_current_token_value() in ['true', 'false', 'null', 'this']:
            result += self.eat(sps + 1)
        elif self.get_current_element_type() == 'identifier':
            result += self.eat(sps + 1)
            if self.get_current_token_value() == '(':
                result += self.eat(sps + 1)
                result += self.compileExpressionList(sps + 1)
                result += self.eat(sps + 1)
            elif self.get_current_token_value() == '[':
                result += self.eat(sps + 1)
                result += self.compileExpression(sps + 1)
                result += self.eat(sps + 1)
            elif self.get_current_token_value() == '.':
                result += self.multEat(sps + 1, 3)
                result += self.compileExpressionList(sps + 1)
                result += self.eat(sps + 1)
        result += self.make_space(sps, '</term>')
        return result
    
    def compileExpressionList(self, sps):
        result = self.make_space(sps, '<expressionList>')
        if self.get_current_token_value() != ')':
            result += self.compileExpression(sps + 1)
            while self.get_current_token_value() != ')':
                result += self.eat(sps + 1)
                result += self.compileExpression(sps + 1)
        result += self.make_space(sps, '</expressionList>')
        return result
    
    def compileActToken(self):
        token_value = self.get_current_token_value()
        if token_value == 'class':
            return self.compileClass(0)
        elif token_value in ['let', 'if', 'while', 'do', 'return']:
            return self.compileStatements(0)
        else:
            return self.compileExpression(0)
    
    def compileTokens(self):
        self.compiled_tokens = []
        while self.has_more_tokens():
            self.compiled_tokens += self.compileActToken()
            count += 1
        return self.compiled_tokens