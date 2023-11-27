import JackTokenizer, JackAnalyzer, SymbolTable

class CompilationEngine:
    def __init__(self, program):
        tokens = JackTokenizer.JackTokenizer(program)
        tokens = tokens.tokenize()
        analyzer = JackAnalyzer.JackAnalyzer(tokens)
        self.tokens = analyzer.compileTokens()
        self.symbol_table = SymbolTable.SymbolTable()
        self.act_token = 0
    
    def advance(self):
        self.act_token += 1
    
    def getCurrentToken(self):
        return self.tokens[self.act_token]

    def getCurrentTokenValue(self):
        token = self.getCurrentToken()
        second_lt = token[1:].find('<')
        first_gt = token.find('>')
        return token[first_gt + 2: second_lt]