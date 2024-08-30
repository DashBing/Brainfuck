from sys import argv

annotator = ";"

class IndexMinusError(Exception):
    message = "Index can't be minus."
    def __str__(self) -> str:
        return self.message

class UnknownCommandError(IndexMinusError):
    message = 'Unknown command: "%s"'
    def __init__(self, command):
        self.message = self.message%command

class Classic:
    memory = [0]
    index_now = 0  # index of the memory now
    input_cache = []  # input cache list

    seek_now = 0  # pointer of the code
    jmplist = []  # jump pointer list for circular instructions

    flag_find_bracket = False

    @property
    def now(self) -> int:
        return self.memory[self.index_now]

    def left(self):
        if self.index_now > 0:
            self.index_now -= 1
        else:
            raise IndexMinusError()

    def right(self):
        if self.index_now+2 > len(self.memory):
            self.memory.append(0)
        self.index_now += 1

    def add(self):
        self.memory[self.index_now] += 1

    def sub(self):
        self.memory[self.index_now] -= 1

    def output(self):
        print(chr(self.now), end="")

    def input(self):
        if(len(self.input_cache) == 0):
            self.input_cache = list(input())
        self.memory[self.index_now] = ord(self.input_cache[0])
        del self.input_cache[0]

    def __str__(self) -> str:
        return self.memory.__str__()
    def __repr__(self) -> str:
        return self.memory.__repr__()

    def left_bracket(self):
        if self.now == 0:
            self.flag_find_bracket = True
            if self.seek_now in self.jmplist:
                if self.jmplist[-1] == self.seek_now:
                    del self.jmplist[-1]
        elif len(self.jmplist) > 0:
            if self.jmplist[-1] != self.seek_now:
                self.jmplist.append(self.seek_now)
        else:
            self.jmplist.append(self.seek_now)
        self.seek_now += 1

    def right_bracket(self):
        self.seek_now = self.jmplist[-1]

    def unknown_command(self, command):
        raise UnknownCommandError(command)

    @property
    def break_condition(self):
        return(self.flag_find_bracket)

    def break_do(self, text:str):
        if text[self.seek_now] == "]":
            self.flag_find_bracket = False
        self.seek_now += 1

    def run(self, text:str):
        while self.seek_now < len(text):
            if self.break_condition:
                self.break_do()
            else:
                match text[self.seek_now]:
                    case ">":
                        self.right()
                        self.seek_now += 1
                    case "<":
                        self.left()
                        self.seek_now += 1
                    case "+":
                        self.add()
                        self.seek_now += 1
                    case "-":
                        self.sub()
                        self.seek_now += 1
                    case ".":
                        self.output()
                        self.seek_now += 1
                    case ",":
                        self.input()
                        self.seek_now += 1
                    case "[":
                        self.left_bracket()
                    case "]":
                        self.right_bracket()
                    case x:
                        self.unknown_command(x)

class JumppointNotFoundError(Exception):
    pass

class NewStandard(Classic):

    jmppoint_list = []

    flag_jump = False

    @property
    def break_condition(self):
        return(super().break_condition or self.flag_jump)

    def break_do(self, text: str):
        if self.flag_jump:
            if text[self.seek_now] == ":":
                self.flag_jump = False
            self.seek_now += 1
        else:
            super().break_do(text)

    def unknown_command(self, command):
        match command:
            case "?":
                if self.now == 0:
                    self.flag_jump = True
                self.seek_now += 1
            case x:
                super().unknown_command(x)

def preprocessor(code:str) -> str:
    code = code.replace("\r", "\n")
    code = code.split("\n")
    for i in range(len(code)):
        code[i] = code[i].split(annotator)[0]
    code = "".join(code)
    code = code.replace(" ", "")
    code = code.replace("\t", "")
    return code

def file_processor(files:str):
    s = ""
    for i in files:
        with open(i, "r") as f:
            s = s + f.read()
        s = s + "\n"
    return preprocessor(s)

def interpreter(files:str, mode:object = Classic):
    mode().run(file_processor(files))

if __name__ == "__main__":
    match argv[1:]:
        case [*files]:
            interpreter(files)
        case ["-n", *files]:
            interpreter(files, NewStandard)
