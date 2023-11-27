import JackTokenizer, JackAnalyzer, SymbolTable

class CompilationEngine:
    def __init__(self, program):
        tokens = JackTokenizer.JackTokenizer(program)
        tokens = tokens.tokenize()
        analyzer = JackAnalyzer.JackAnalyzer(tokens)
        self.tokens = analyzer.compileTokens()
        self.symbol_table = SymbolTable.SymbolTable()
