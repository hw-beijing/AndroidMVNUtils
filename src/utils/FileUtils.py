import os
from utils.StringUtils import StringUtils


class FileUtils:

    # 读取文件
    @staticmethod
    def readFile(path):
        if path.strip() != "":
            fr = open(path, encoding='utf-8')
            arrayOLines = fr.readlines()
            return arrayOLines
        return []

    # 判断文件是否存在
    @staticmethod
    def judgeFileExist(path):
        return os.path.exists(path)

    # 读取setting文件
    @staticmethod
    def readSetting(rootPath):
        modules = []
        if rootPath.strip() != "":
            arrayOLines = FileUtils.readFile(rootPath + os.sep + 'settings.gradle')
            for line in arrayOLines:
                line = line.strip()  # strip()函数为删除一行中的空白符
                if line != "":
                    t = r"//"
                    if not line.startswith(t):
                        st = line.split("'")
                        if st.__sizeof__() >= 2 and not st[1].__eq__(":app"):
                            print("readSetting : " + st[1])
                            modules.append(st[1])
        return modules

    # 读取app gradle 文件
    @staticmethod
    def readMainGradle(rootPath, modules):
        modulesMap = {}
        if rootPath.strip() != "":
            arrayOLines = FileUtils.readFile(rootPath + os.sep + 'app' + os.sep + 'build.gradle')
            for line in arrayOLines:
                line = StringUtils.formatString(line)
                t = r"//"
                if line != "" and not line.startswith(t) and line.startswith("compile"):
                    for str in modules:
                        strName = str.split(":")
                        if strName.__sizeof__() >= 2 and strName[-1] in line:
                            st = line.split("\"")
                            print("readMainGradle : " + str + " " + st[1])
                            modulesMap[str] = st[1]
                            break
        return modulesMap

    # 获取模块路径
    @staticmethod
    def getModulePath(rootPath, moduleName=""):
        if rootPath.strip() != "" and StringUtils.formatString(moduleName) != "":
            moduleName = moduleName.replace(":", os.sep)
            modulePath = rootPath + os.sep + moduleName + os.sep
            return modulePath
        return ""

    # 判断模块是否存在
    @staticmethod
    def judgeModuleExist(modulePath):
        if StringUtils.formatString(modulePath) != "":
            str = modulePath + ".git" + os.sep + "HEAD"
            return FileUtils.judgeFileExist(str)
        return False

    @staticmethod
    def getModuleGitVersion(modulePath):
        if StringUtils.formatString(modulePath) != "":
            arrayOLines = FileUtils.readFile(modulePath + ".git" + os.sep + "HEAD")
            if arrayOLines.__sizeof__() > 1:
                str = arrayOLines[0]
                if os.sep in str:
                    versions = str.split(os.sep)
                    print("getModuleGitVersion : " + versions[-1])
                    return versions[-1]
                else:
                    return str
        return ""
