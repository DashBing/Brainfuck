from sys import argv

class IndexMinusError(Exception):
    message = "Index can't be minus."
    def __str__(self) -> str:
        return self.message

class Classic:
    memory = [0]
    index_now = 0  # index of the memory now
    input_cache = []  # input cache list

    seek_now = 0  # pointer of the code
    jmplist = []  # jump pointer list for circular instructions

    flag_find_bracket = False

    @property
    def now(self) -> int:
        return(self.memory[self.index_now])

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
        return(self.memory.__str__())
    def __repr__(self) -> str:
        return(self.memory.__repr__())

    def left_bracket(self):
        if self.now == 0:
            self.flag_find_bracket = True
        elif len(self.jmplist) > 0:
            if self.jmplist[-1] != self.seek_now:
                self.jmplist.append(self.seek_now)
        else:
            self.jmplist.append(self.seek_now)
        self.seek_now += 1

    def right_bracket(self):
        pass

    def unknown_command(x):
        pass

    def run(self, text:str):
        while self.seek_now < len(text):
            if self.flag_find_bracket:
                pass
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
