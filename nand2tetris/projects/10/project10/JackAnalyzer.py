import sys, os, JackTokenizer, CompilationEngine

def find_name_file(dir):
    init = 0
    final = len(dir)

    for i in range(len(dir)):
        if dir[i] == '/':
            init = i + 1
        if dir[i] == '.':
            final = i

    return dir[init:final]

def parse_file(file_path):
    program = open(file_path).readlines()
    tokenizer = JackTokenizer.JackTokenizer(program)
    tokenizer.tokenize()
    compilation_engine = CompilationEngine.CompilationEngine(tokenizer.program_tokenized)
    compilation_engine.compileTokens()
    dest = file_path[:-5] + "A.xml"
    with open(dest, "w") as file:
        for line in compilation_engine.compiled_tokens:
            file.write(line)
            file.write('\n')

if __name__ == '__main__':
    file_path = sys.argv[1]
    if len(file_path) >= 5 and file_path[-4:] == 'jack':
        parse_file(file_path)
    else:
        if file_path[-1] != '/':
            file_path += '/'
        files = os.scandir(file_path)

        for file in files:
            if file.name[-4:] == 'jack':
                parse_file(file.path)