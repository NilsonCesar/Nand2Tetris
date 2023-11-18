class JackTokenizer:
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '>', '<', '=', '~']

    def __init__(self, input):
        self.lines = self.format_input(input)

    def format_input(self, program):
        lines = []
        in_coment = False
        for line in program:
            ans = line
            slash_idx = line.find("//")

            if slash_idx != -1:
                ans = line[:slash_idx]
            
            slash_idx = line.find("/**")
            if slash_idx != -1:
                in_coment = True

            slash_idx = line.find("*/")
            if slash_idx != -1:
                in_coment = False
                ans = ""

            if in_coment:
                ans = ""
            
            ans = ans.strip()

            if ans != "":
                lines.append(ans)
        return lines
    
    def make_token(self, token):
        return f'<{self.type_of(token)}> {self.format_token(token)} </{self.type_of(token)}>'

    def type_of(self, token):
        if token in JackTokenizer.keywords:
            return 'keyword'
        if token in JackTokenizer.symbols:
            return 'symbol'
        if token[0] == '"':
            return 'stringConstant'
        try:
            int(token)
            return 'integerConstant'
        except:
            return 'identifier'

    def isInReservedWords(self, word):
        return (word in JackTokenizer.keywords) or (word in JackTokenizer.symbols)

    def format_token(self, token):
        type_token = self.type_of(token)
        if token == '&':
            return '&amp;'
        if token == '<':
            return '&lt;'
        if token == '>':
            return '&gt;'

        if type_token in ['keyword', 'symbol', 'integerConstant', 'identifier']:
            return token
        return token[1:-1]

    def tokenize_line(self, line):
        tokens = []
        i = 0
        while i < len(line):
            if line[i] == ' ':
                i += 1
                continue
        
            if self.isInReservedWords(line[i]):
                tokens.append(self.make_token(line[i]))
                i += 1
                continue

            if line[i] == '"':
                i += 1
                string = ''
                while i < len(line) and line[i] != '"':
                    string += line[i]
                    i += 1
                i += 1
                tokens.append(self.make_token('"'+ string + '"'))
                continue
            else:
                try:
                    int(line[i])
                    num = line[i]
                    i += 1
                    while i < len(line):
                        try:
                            int(line[i])
                            num += line[i]
                            i += 1
                        except:
                            break
                    tokens.append(self.make_token(num))
                    continue
                except:
                    0
            word = line[i]
            i += 1
            while i < len(line) and not (self.isInReservedWords(line[i]) or line[i] == ' '):
                word += line[i]
                i += 1
                if self.isInReservedWords(word):
                    break

            tokens.append(self.make_token(word))
        return tokens
    
    def tokenize(self):
        self.program_tokenized = ['<tokens>']
        for line in self.lines:
            self.program_tokenized += self.tokenize_line(line)
        self.program_tokenized += ['</tokens>']
        return self.program_tokenized