import JackTokenizer, Parser, SymbolTable

class CompilationEngine:
    def __init__(self, program):
        tokens = JackTokenizer.JackTokenizer(program)
        tokens = tokens.tokenize()
        analyzer = Parser.Parser(tokens)
        self.tokens = analyzer.compileTokens()
        self.symbol_table = SymbolTable.SymbolTable()
        self.act_token = 0
    
    def populeSymbolTable(self, variable):
        self.symbol_table.define(variable[0], variable[1], variable[2])

    def advance(self):
        self.act_token += 1

    def multAdvance(self, n):
        self.act_token = self.act_token + n

    def getCurrentToken(self):
        return self.tokens[self.act_token]

    def getCurrentTokenType(self):
        token = self.getCurrentToken()
        first_lt = token.find('<')
        first_gt = token.find('>')
        return token[first_lt + 1 : first_gt]

    def getCurrentTokenValue(self):
        token = self.getCurrentToken()
        second_lt = token[1:].find('<')
        first_gt = token.find('>')
        return token[first_gt + 2: second_lt]
    
    def createClassVariable(self):
        kind = self.getCurrentTokenValue()
        self.advance()
        if kind == 'field':
            kind = 'FIELD'
        if kind == 'static':
            kind = 'STATIC'
        type = self.getCurrentTokenValue()
        self.advance()
        name = self.getCurrentTokenValue()
        self.advance()
        return [name, type, kind]

    def createParameterVariable(self):
        kind = 'ARG'
        type = self.getCurrentTokenValue()
        self.advance()
        name = self.getCurrentTokenValue()
        self.advance()
        return [name, type, kind]

    def createVarVariable(self, type):
        kind = "VAR"
        name = self.getCurrentTokenValue()
        self.advance()
        return [name, type, kind]

    def compileClassVarDec(self):
        self.advance()
        variable = self.createClassVariable()
        self.populeSymbolTable(variable)
        self.multAdvance(3)

    def compileParameterList(self):
        self.advance()
        while self.getCurrentTokenType() != '/parameterList':
            variable = self.createParameterVariable()
            self.populeSymbolTable(variable)
            if self.getCurrentTokenValue() == ',':
                self.advance()
        self.advance()

    def compileVarDec(self):
        self.multAdvance(2)
        type = self.getCurrentTokenValue()
        self.advance()
        variable = self.createVarVariable(type)
        self.populeSymbolTable(variable)
        while self.getCurrentTokenValue() != ';':
            self.advance()
            variable = self.createVarVariable(type)
            self.populeSymbolTable(variable)
        self.multAdvance(2)
