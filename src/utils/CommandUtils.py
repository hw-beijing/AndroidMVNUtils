import os
from utils.FileUtils import FileUtils
from utils.StringUtils import StringUtils


class CommandUtils:
    #克隆项目
    @staticmethod
    def gitClone(modulePath, gitPath):
        if not FileUtils.judgeFileExist(modulePath):
            os.makedirs(modulePath)
        os.chdir(modulePath)
        a = os.system('git clone ' + gitPath+" " +modulePath)
        if a == 0:
            print("克隆成功")
            return True
        else:
            print("克隆失败")
            return False

    #更新
    @staticmethod
    def gitPull(modulePath):
        a = -1
        if FileUtils.judgeFileExist(modulePath):
            os.chdir(modulePath)
            a = os.system('git pull')
            if a == 0:
                print("更新成功")
                return True
            else:
                print("更新失败")
                return False
        return False

    #切换分支
    @staticmethod
    def gitChackOut(modulePath, version):
        a = -1
        if FileUtils.judgeFileExist(modulePath):
            os.chdir(modulePath)
            a = os.system('git checkout ' + version)
            if a == 0:
                print("切换分支成功")
                return True
            else:
                print("切换分支失败")
                return False
        return False

    #上传maven
    @staticmethod
    def mavenUpload(modulePath, environment):
        a = -1
        if FileUtils.judgeFileExist(modulePath):
            os.chdir(modulePath)
            a = os.system("gradle uploadArchives -Pmaven_environment=" + environment)
            print(a)
            if a == 0:
                print("maven上传成功")
                return True
            else:
                print("maven上传失败")
                return False
        return False
