class InvalidModeException(Exception):
    def __init__(self, mode):
        self.salary = mode
        self.message = f"mode: {mode} does not exist."
        super().__init__(self.message)

class InvalidFunctionCallException(Exception):
    def __init__(self, mode,medthodName):
        self.salary = mode
        self.message = f"mode: {mode} was specified but called {medthodName}"
        super().__init__(self.message)