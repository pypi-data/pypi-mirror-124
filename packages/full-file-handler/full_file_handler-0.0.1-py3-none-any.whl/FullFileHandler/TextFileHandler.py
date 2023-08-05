from Exceptions import *

class TextFileHandler:
    def __init__(self,path:str,mode:str="r"):
        self.path = path
        if mode == "w" or mode == "r" or mode == "a":
            self.mode = mode
        else:
            self.mode = "r"
            raise InvalidModeException(mode)

    def read(self):
        if self.mode == "r":
            f1 = open(self.path,self.mode)
            return f1.read()
        else:
            raise InvalidFunctionCallException(self.mode,"read")