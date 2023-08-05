from Exceptions import *
from Modes import Modes

class TextFileHandler:
    def __init__(self,path:str,mode:str=Modes.READ):
        self.path = path
        if mode == Modes.WRITE or mode == Modes.READ or mode == Modes.APPEND:
            self.mode = mode
            self.file = open(self.path,self.mode)
        else:
            self.mode = Modes.READ
            raise InvalidModeException(mode)

    def read(self):
        if self.mode == Modes.READ:
            return self.file.read()
        else:
            raise InvalidFunctionCallException(self.mode,"read")

    def write(self,content:str):
        if self.mode == Modes.WRITE:
            self.file.write(content)
        else:
            raise InvalidFunctionCallException(self.mode,"write")
    
    def append(self,content:str):
        if self.mode == Modes.APPEND:
            self.file.write(content)
        else:
            raise InvalidFunctionCallException(self.mode,"append")
    
    def close(self):
        self.file.close()