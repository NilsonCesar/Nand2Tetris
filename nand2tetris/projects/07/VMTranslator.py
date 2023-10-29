import sys

class Parser():
    def __init__(self, program):
        self.lines = self.format_lines(program)
    
    def format_lines(self, program):
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

    def take_operations(self):
        operations = []
        for operation in self.lines:
            operation_parts = operation.split()
            operations.append(operation_parts)
        return operations


if __name__ == "__main__":
    file_path = sys.argv[1]
    program = open(file_path).readlines()
    parser = Parser(program)
    print(parser.take_operations())