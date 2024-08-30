from sys import argv

class IndexMinusError(Exception):
    message = "Index can't be minus."
    def __str__(self) -> str:
        return self.message

class Interpreter:
    memory = [0]
    p_now = 0
    p_jmplist = []

    def left(self):
        if self.p_now > 0:
            self.p_now -= 1
        else:
            raise IndexMinusError()

    def right(self):
        if self.p_now+2 > len(self.memory):
            self.memory.append(0)
        self.p_now += 1

    def output(self):
        print(chr(self.memory[self.p_now]), end="")
