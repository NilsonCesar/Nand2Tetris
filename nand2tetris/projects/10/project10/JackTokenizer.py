class JackTokenizer:
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, input):
        self.lines = self.format_input(input)

    def format_input(self, program):
        lines = []
        for line in program:
            ans = line
            slash_idx = line.find("//")

            if slash_idx != -1:
                ans = line[:slash_idx]
            ans = ans.strip()

            if ans != "":
                lines.append(ans)
        return lines
    
    def make_token(self, token):
        return f'<{self.type_of(token)}> {self.format_token(token)} <{self.type_of(token)}>'

    def type_of(self, token):
        if token in JackTokenizer.keywords:
            return 'keyword'
        if token in JackTokenizer.symbol:
            return 'symbol'
        if token[0] == '"':
            return 'stringConstant'
        try:
            int(token)
            return 'integerConstant'
        except:
            return 'identifier'
    
    def format_token(self, token):
        type_token = self.type_of(token)
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

            if line[i] == '"':
                string = ''
                i += 1
                while line[i] != '"':
                    string += line[i]
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
            if self.isInReservedWords(line[i]):
                tokens.append(self.make_token(line[i]))
                i += 1
            else:
                identifier = ''
                i += 1
                while i < len(line) and not (self.isInReservedWords(line[i]) or line[i] == ' '):
                    identifier += line[i]
                    i += 1
                tokens.append(self.make_token(identifier))