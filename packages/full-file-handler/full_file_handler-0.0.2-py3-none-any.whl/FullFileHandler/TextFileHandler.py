from Exceptions import *
from Modes import Modes

class TextFileHandler:
    def __init__(self,path:str,mode:str="r"):
        self.path = path
        if mode == Modes.WRITE or mode == Modes.READ or mode == Modes.APPEND:
            self.mode = mode
            self.f1 = open(self.path,self.mode)
        else:
            self.mode = Modes.READ
            raise InvalidModeException(mode)

    def read(self):
        if self.mode == Modes.READ:
            return self.f1.read()
        else:
            raise InvalidFunctionCallException(self.mode,"read")

    def write(self,content:str):
        if self.mode == Modes.WRITE:
            self.f1.write(content)
        else:
            raise InvalidFunctionCallException(self.mode,"write")
    
    def append(self,content:str):
        if self.mode == Modes.APPEND:
            self.f1.write(content)
        else:
            raise InvalidFunctionCallException(self.mode,"write")