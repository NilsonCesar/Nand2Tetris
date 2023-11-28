import JackTokenizer, Parser, SymbolTable, VMWriter

class CompilationEngine:
    def __init__(self, program, label_name = 'default'):
        tokens = JackTokenizer.JackTokenizer(program)
        tokens = tokens.tokenize()
        analyzer = Parser.Parser(tokens)
        self.tokens = analyzer.compileTokens()
        self.symbol_table = SymbolTable.SymbolTable()
        self.vmwriter = VMWriter.VMWriter()
        self.act_token = 0
        self.label_name = label_name
        self.label_num = 1
    
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

    def compileExpression(self):
        self.advance()
        self.compileTerm()
        while self.getCurrentTokenType() != '/expression':
            op = self.getCurrentTokenValue()
            self.advance()
            self.compileTerm()
            self.vmwriter.writeArithmetic(op)
        self.advance()

    def compileTerm(self, inDo = False):
        if(not inDo):
            self.advance()
        tokenType = self.getCurrentTokenType()
        if tokenType == 'integerConstant':
            self.vmwriter.writePush('constant', self.getCurrentTokenValue())
            self.advance()
        elif tokenType == 'stringConstant':
            string = self.getCurrentTokenValue()
            self.vmwriter.writePush('constant', len(string))
            self.vmwriter.writeCall('String.new', 1)

            for c in string:
                self.vmwriter.writePush('constant', ord(c))
                self.vmwriter.writeCall('String.appendChar', 2)
            self.advance()
        elif tokenType == 'identifier':
            name = self.getCurrentTokenValue()
            self.advance()
            if self.getCurrentTokenValue() == '(':
                self.advance()
                n = self.compileExpressionList()
                self.advance()
                self.vmwriter.writeCall(name, n)
            elif self.getCurrentTokenValue() != '[':
                self.vmwriter.writePush(self.symbol_table.kindOf(name), self.symbol_table.indexOf(name))
                self.advance()
        elif tokenType == 'symbol':
            if self.getCurrentTokenValue == '(':
                self.advance()
                self.compileExpression()
                self.advance()
            else:
                op = self.getCurrentTokenValue()
                self.advance()
                self.compileTerm()
                self.vmwriter.writeArithmetic(op)
        elif tokenType == 'keyword':
            value = self.getCurrentTokenValue()
            if value == 'true':
                self.vmwriter.writePush('constant', 1)
                self.vmwriter.writeArithmetic('-', True)
                self.advance()
            elif value in ['false', 'null']:
                self.vmwriter.writePush('constant', 0)
                self.advance()
            elif value == 'this':
                self.vmwriter.writePush('pointer', 0)
                self.advance()

        if(not inDo):
            self.advance()
    def compileLet(self):
        self.multAdvance(2)
        name = self.getCurrentTokenValue()
        self.advance()
        if self.getCurrentTokenValue() != '[':
            self.advance()
            self.compileExpression()
            self.vmwriter.writePop(self.symbol_table.kindOf(name), self.symbol_table.indexOf(name))
            self.advance()
        self.advance()

    def compileReturn(self):
        self.multAdvance(2)
        if self.getCurrentTokenValue == ';':
            self.vmwriter.writePush('constant', 0)
        else:
            self.compileExpression()
        self.vmwriter.writeReturn()
        self.multAdvance(2)

    def compileDo(self):
        self.multAdvance(2)
        self.compileTerm(True)
        while self.getCurrentTokenValue != '/doStatement':
            self.advance()
        self.advance()

    def compileIf(self):
        l1 = self.label_num
        l2 = self.label_num + 1
        self.label_num += 2
        self.multAdvance(3)
        self.compileExpression()
        self.vmwriter.writeArithmetic('-', True)
        self.vmwriter.writeIf(f'${self.label_name + l1}')
        self.multAdvance(2)
        self.compileStatements()
        self.vmwriter.writeGoto(f'${self.label_name + l2}')
        self.advance()
        self.vmwriter.writeLabel(f'${self.label_name + l1}')
        if self.getCurrentTokenValue == 'else':
            self.multAdvance(2)
            self.compileStatements()
            self.advance()
        self.vmwriter.writeLabel(f'${self.label_name + l2}')

    def compileWhile(self):
        l1 = self.label_num
        l2 = self.label_num + 1
        self.label_num += 2
        self.vmwriter.writeLabel(f'${self.label_name + l1}')
        self.multAdvance(3)
        self.compileExpression()
        self.vmwriter.writeArithmetic('-', True)
        self.vmwriter.writeIf(f'${self.label_name + l2}')
        self.multAdvance(2)
        self.compileStatements()
        self.multAdvance(2)
        self.vmwriter.writeGoto(f'${self.label_name + l1}')
        self.vmwriter.writeLabel(f'${self.label_name + l2}')
    
    def compileStatements(self):
        self.advance()
        while self.getCurrentTokenType() != '/statements':
            tokenType = self.getCurrentTokenType()
            if tokenType == 'letStatement':
                self.compileLet()
            if tokenType == 'ifStatement':
                self.compileIf()
            if tokenType == 'whileStatement':
                self.compileWhile()
            if tokenType == 'doStatement':
                self.compileDo()
            if tokenType == 'returnStatement':
                self.compileReturn()
        self.advance()