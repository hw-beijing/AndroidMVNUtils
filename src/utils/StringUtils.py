import os
class StringUtils:
    @staticmethod
    def formatString(str):
        str =str.strip()
        str = str.replace(" ", "")
        str = str.replace("\n", "")
        return str

    @staticmethod
    def getPathLastName(path):
        return path.split(os.sep)[-1]
