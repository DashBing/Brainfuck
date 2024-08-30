from sys import argv

class IndexMinusError(Exception):
    message = "Index can't be minus."
    def __str__(self) -> str:
        return self.message

class Interpreter:
    memory = [0]
    index_now = 0  # index of the memory now
    input_cache = []  # input cache list

    seek_now = 0  # pointer of the code
    jmplist = []  # jump pointer list for circular instructions

    def left(self):
        if self.index_now > 0:
            self.index_now -= 1
        else:
            raise IndexMinusError()

    def right(self):
        if self.index_now+2 > len(self.memory):
            self.memory.append(0)
        self.index_now += 1

    def output(self):
        print(chr(self.memory[self.index_now]), end="")

    def input(self):
        if(len(self.input_cache) == 0):
            self.input_cache = list(input())
        self.memory[self.index_now] = ord(self.input_cache[0])
        del self.input_cache[0]

    def __str__(self) -> str:
        return(self.memory.__str__())
    def __repr__(self) -> str:
        return(self.memory.__repr__())
