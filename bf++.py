from .bf import *

class NewStandard(Classic):

    jmppoint_list = []
    mem_back_list = []

    flag_jump = False
    flag_jump_right = True

    @property
    def break_condition(self):
        return(super().break_condition or self.flag_jump)

    def break_do(self, text: str):
        if self.flag_jump:
            if text[self.seek_now] == ":":
                self.flag_jump = False
            if self.flag_jump_right:
                self.seek_now += 1
            else:
                self.seek_now -= 1
        else:
            super().break_do(text)

    def output_str(self):
        while(self.now != 0):
            self.output()
            self.index_now += 1

    def unknown_command(self, command):
        match command:
            case "/":
                if self.now == 0:
                    self.flag_jump = True
                    self.flag_jump_right = True
                self.seek_now += 1
            case "\\":
                if self.now == 0:
                    self.flag_jump = True
                    self.flag_jump_right = False
                self.seek_now -= 1
            case "*":
                self.memory[self.index_now] = 0
                self.seek_now += 1
            case "#":
                self.memory = [0]
                self.index_now = 0
                self.seek_now += 1
            case "{":
                tmp = self.now()
                self.left()
                self.memory[self.index_now] = tmp
                self.seek_now += 1
            case "}":
                tmp = self.now()
                self.right()
                self.memory[self.index_now] = tmp
                self.seek_now += 1
            case ";":
                self.output_str()
                self.seek_now += 1
            case "!":
                self.mem_back_list.append(self.index_now)
                self.seek_now += 1
            case "@":
                self.index_now = self.mem_back_list[-1]
                del self.mem_back_list[-1]
                self.seek_now += 1
            case x:
                self.memory[self.index_now] = ord(x)
                self.right()
                self.seek_now += 1

if __name__ == "__main__":
    interpreter(argv[1:], NewStandard)
