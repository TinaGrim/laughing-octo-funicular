
from PySide6.QtCore import QThread
class Threader(QThread):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.arg = args
        self.kwargs = kwargs
    def run(self):
        self.func(*self.arg, **self.kwargs)