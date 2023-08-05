from TextFileHandler import *
from Modes import *

t = TextFileHandler("test.py",Modes.WRITE)
print(t.read())