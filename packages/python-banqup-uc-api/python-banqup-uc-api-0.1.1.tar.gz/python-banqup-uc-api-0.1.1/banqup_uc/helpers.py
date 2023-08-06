import os

def getFilename(filePath):
    return filePath.split(os.sep)[-1]