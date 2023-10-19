

class Logger:
    def __init__(self, logFilePath):
        self.logFilePath = logFilePath
        self.logFile = open(logFilePath, "a+")

    def log(self, logMessage):
        self.logFile.write(logMessage + "\n")
        self.logFile.flush()

    def close(self):
        self.logFile.close()

    def __del__(self):
        self.close()