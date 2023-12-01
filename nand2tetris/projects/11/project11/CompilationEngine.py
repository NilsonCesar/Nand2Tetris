import JackTokenizer, Parser, SymbolTable, VMWriter, os

class CompilationEngine:
    def __init__(self, program):
        tokens = JackTokenizer.JackTokenizer(program)
        tokens = tokens.tokenize()
        analyzer = Parser.Parser(tokens)
        self.tokens = analyzer.compileTokens()
        with open('/home/nilson/Documentos/Workspace/Nand2Tetris/nand2tetris/projects/11/Seven/Main.tokens', 'w') as file:
            for token in self.tokens:
                file.write(token)
                file.write('\n')
        self.symbol_table = SymbolTable.SymbolTable()
        self.vmwriter = VMWriter.VMWriter()
        self.act_token = 0
        self.label_name = ''
        self.label_num = 1
        self.name_file = ''
        self.num_fields = 0
        self.void_functions = []
        self.method_functions = []
        self.class_functions = []


    def has_more_tokens(self):
        return self.act_token < len(self.tokens)

    def populeSymbolTable(self, variable):
        self.symbol_table.define(variable[0], variable[1], variable[2])

    def advance(self):
        if self.has_more_tokens():
            self.act_token += 1
        return len(self.tokens)

    def multAdvance(self, n):
        if self.act_token + n < len(self.tokens):
            self.act_token = self.act_token + n
        return len(self.tokens)

    def getCurrentToken(self):
        if self.act_token < len(self.tokens):
            return self.tokens[self.act_token]
        return self.tokens[-1]

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
    
    def getNumberOfVarDec(self):
        num = 0
        inVarDec = False
        cur = self.act_token
        while self.tokens[cur] != '<statements>':
            if self.tokens[cur] == '<varDec>':
                num += 1
                inVarDec = True
            if self.tokens[cur] == '<symbol> , </symbol>' and inVarDec:
                num += 1
            if self.tokens[cur] == '</varDec>':
                inVarDec = False
            cur += 1
        return num

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
        kind = self.getCurrentTokenValue()
        self.advance()
        if kind == 'field':
            self.num_fields += 1
            kind = 'FIELD'
        if kind == 'static':
            kind = 'STATIC'
        type = self.getCurrentTokenValue()
        self.advance()
        name = self.getCurrentTokenValue()
        self.advance()
        self.populeSymbolTable([name, type, kind])
        
        while self.getCurrentTokenValue() != ';':
            self.advance()
            name = self.getCurrentTokenValue()
            self.advance()
            self.populeSymbolTable([name, type, kind])
        self.multAdvance(2)

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
                n = 0
                self.advance()
                n += self.compileExpressionList()
                self.advance()
                self.vmwriter.writeCall(self.name_file + '.' + name, n)
            elif self.getCurrentTokenValue() == '.':
                n = 0
                self.advance()
                subroutineName = self.getCurrentTokenValue()
                self.multAdvance(2)
                n += self.compileExpressionList()
                self.advance()
                self.vmwriter.writeCall(f'{name}.{subroutineName}', n)
            elif self.getCurrentTokenValue() != '[':
                self.vmwriter.writePush(self.symbol_table.kindOf(name), self.symbol_table.indexOf(name))
            elif self.getCurrentTokenValue() == '[':
                self.vmwriter.writePush(self.symbol_table.kindOf(name), self.symbol_table.indexOf(name))
                self.advance()
                self.compileExpression()
                self.advance()
                self.vmwriter.writeArithmetic('+')
                self.vmwriter.writePop('pointer', 1)
                self.vmwriter.writePush('that', 0)
        elif tokenType == 'symbol':
            if self.getCurrentTokenValue() == '(':
                self.advance()
                self.compileExpression()
                self.advance()
            else:
                op = self.getCurrentTokenValue()
                self.advance()
                self.compileTerm()
                self.vmwriter.writeArithmetic(op, True)
        elif tokenType == 'keyword':
            value = self.getCurrentTokenValue()
            if value == 'true':
                self.vmwriter.writePush('constant', 0)
                self.vmwriter.writeArithmetic('~', True)
                self.advance()
            elif value in ['false', 'null']:
                self.vmwriter.writePush('constant', 0)
                self.advance()
            elif value == 'this':
                self.vmwriter.writePush('pointer', 0)
                self.advance()
        else:
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
        else:
            self.vmwriter.writePush(self.symbol_table.kindOf(name), self.symbol_table.indexOf(name))
            self.advance()
            self.compileExpression()
            self.multAdvance(2)
            self.vmwriter.writeArithmetic('+')
            self.compileExpression()
            self.vmwriter.writePop('temp', 0)
            self.vmwriter.writePop('pointer', 1)
            self.vmwriter.writePush('temp', 0)
            self.vmwriter.writePop('that', 0)
        self.multAdvance(2)

    def compileReturn(self):
        self.multAdvance(2)
        if self.getCurrentTokenValue() == ';':
            self.vmwriter.writePush('constant', 0)
        else:
            self.compileExpression()
        self.vmwriter.writeReturn()
        self.multAdvance(2)

    def compileDo(self):
        self.multAdvance(2)
        self.compileTerm(True)
        self.multAdvance(2)

    def compileIf(self):
        l1 = self.label_num
        l2 = self.label_num + 1
        self.label_num += 2
        self.multAdvance(3)
        self.compileExpression()
        self.vmwriter.writeArithmetic('-', True)
        self.vmwriter.writeIf(f'${self.label_name}{l1}')
        self.multAdvance(2)
        self.compileStatements()
        self.vmwriter.writeGoto(f'${self.label_name}{l2}')
        self.advance()
        self.vmwriter.writeLabel(f'${self.label_name}{l1}')
        if self.getCurrentTokenValue() == 'else':
            self.multAdvance(2)
            self.compileStatements()
            self.multAdvance(2)
        else:
            self.advance()
        self.vmwriter.writeLabel(f'${self.label_name}{l2}')

    def compileWhile(self):
        l1 = self.label_num
        l2 = self.label_num + 1
        self.label_num += 2
        self.vmwriter.writeLabel(f'${self.label_name}{l1}')
        self.multAdvance(3)
        self.compileExpression()
        self.vmwriter.writeArithmetic('-', True)
        self.vmwriter.writeIf(f'${self.label_name}{l2}')
        self.multAdvance(2)
        self.compileStatements()
        self.multAdvance(2)
        self.vmwriter.writeGoto(f'${self.label_name}{l1}')
        self.vmwriter.writeLabel(f'${self.label_name}{l2}')
    
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
    
    def compileExpressionList(self):
        n = 0
        self.advance()
        while self.getCurrentTokenType() != '/expressionList':
            n += 1
            self.compileExpression()
            if self.getCurrentTokenValue() == ',':
                self.advance()
        self.advance()
        return n
    
    def compileSubroutineBody(self, routineType, routineName = ''):
        self.multAdvance(2)
        while self.getCurrentTokenType() == 'varDec':
            self.compileVarDec()

        if routineType == 'constructor':
            self.vmwriter.writePush('constant', self.num_fields)
            self.vmwriter.writeCall('Memory.alloc', 1)
            self.vmwriter.writePop('pointer', 0)
        if routineType == 'method':
            self.vmwriter.writePush('argument', 0)
            self.vmwriter.writePop('pointer', 0)
        if routineType == 'function':
            self.class_functions.append(self.label_name + '.' + routineName)
        self.compileStatements()
        self.multAdvance(2)

    def compileSubroutine(self):
        self.symbol_table.startSubroutine()
        self.advance()
        routineType = self.getCurrentTokenValue()
        self.advance()
        routineKind = self.getCurrentTokenValue()
        self.advance()
        routineName = self.getCurrentTokenValue()
        self.advance()
        if routineType == 'method':
            self.method_functions.append(self.label_name + '.' + routineName)
        if routineKind == 'void':
            self.void_functions.append(self.label_name + '.' + routineName)
        n = self.getNumberOfVarDec()
        self.vmwriter.writeFunction(self.name_file + '.' + routineName, n)
        self.advance()
        self.compileParameterList()
        self.advance()
        self.compileSubroutineBody(routineType, routineName)
        self.advance()

    def compileClass(self):
        self.multAdvance(2)
        name = self.getCurrentTokenValue()
        self.name_file = name
        self.label_name = name
        self.multAdvance(2)

        while self.getCurrentTokenType() == 'classVarDec':
            self.compileClassVarDec()
        while self.getCurrentTokenType() == 'subroutineDec':
            self.compileSubroutine()
        self.multAdvance(2)

    def compileActToken(self):
        token_value = self.getCurrentToken()
        if token_value == '<class>':
            return self.compileClass()
        elif token_value in ['<letStatement>', '<ifStatement>', '<whileStatement>', '<doStatement>', '<returnStatement>']:
            return self.compileStatements()
        else:
            return self.compileExpression()
    
    def compileTokens(self):
        self.compileClass()
        return self.vmwriter.vm_comands