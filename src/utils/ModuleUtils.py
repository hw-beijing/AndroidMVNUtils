import os
import sys
from utils.CommandUtils import CommandUtils
from utils.FileUtils import FileUtils
from utils.StringUtils import StringUtils
from utils.SysUtils import SysUtils


class ModuleUtils:

    # 检测项目是否存在
    @staticmethod
    def moduleClone(path, gitPath):
        # 检查项目是否存在,不存在则克隆项目
        if not FileUtils.judgeModuleExist(path):
            if not CommandUtils.gitClone(path, gitPath):
                return False
        return True

    @staticmethod
    def modulePull(path, version):
        # 获取本地模块版本号
        gitVersion = FileUtils.getModuleGitVersion(path)
        success = True
        # 对比本地版本号和需要的版本号,不同则切换分支
        if not gitVersion.__eq__("v" + version):
            if not CommandUtils.gitChackOut(path, "v" + version):
                success = False
        if success:
            # 拉取新代码
            if not CommandUtils.gitPull(path):
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def moduleOperator(path, gitPath, version):
        # 克隆项目
        if ModuleUtils.moduleClone(path, gitPath):
            #拉取新代码
            if not ModuleUtils.modulePull(path, version):
                return False
            else:
                return True
        else:
            return False

    # 宿主app的操作
    @staticmethod
    def appOperator(appPath, appGitPath, appVersion="0.0.0"):
        success = ModuleUtils.moduleOperator(appPath, appGitPath, appVersion)
        if success:
            print("宿主app操作成功")
        else:
            print("宿主app操作失败")
            SysUtils.exit(False)

    @staticmethod
    def submoduleOperator(appPath, gitPath, moduleName, moduleVersion,environment):
        moduleGitPath = gitPath + moduleName.split(":")[-1] + ".git"
        modulePath = FileUtils.getModulePath(appPath, moduleName)
        success = ModuleUtils.moduleOperator(modulePath, moduleGitPath, moduleVersion)
        if success:
            print(moduleName + " git 操作成功")
            if CommandUtils.mavenUpload(modulePath,environment):
                print(moduleName + " maven 操作成功")
            else:
                print(moduleName + " maven 操作失败     err")
        else:
            print(moduleName + " git 操作失败")
            SysUtils.exit(False)
