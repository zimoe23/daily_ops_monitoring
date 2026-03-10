import builtins
from config.settings import LOG_FILE

class Logger:

    def __init__(self):
        self.original_print = builtins.print

    def log(self, message):
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(str(message) + "\n")
        except:
            pass
        self.original_print(message)