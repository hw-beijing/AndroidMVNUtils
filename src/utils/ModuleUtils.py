import os
import time
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
        print("moduelClone: " + path)
        if not FileUtils.judgeModuleExist(path):
            if not CommandUtils.gitClone(path, gitPath):
                return False
        return True

    @staticmethod
    def modulePull(path, version):
        # 获取本地模块版本号
        gitVersion = FileUtils.getModuleGitVersion(path)
        success = True
        versionS = version
        if not version.startswith("v"):
            versionS = "v" + version
        # 对比本地版本号和需要的版本号,不同则切换分支
        print("gitVersion |" + gitVersion + "|")
        print("version  |" + versionS + "|")
        print(gitVersion == versionS)

        if FileUtils.judgeFileExist(path):
            os.chdir(path)
            os.system('git -c diff.mnemonicprefix=false -c core.quotepath=false fetch --prune --tags origin')
            needChackOut = False
            if not gitVersion.endswith(versionS):
                needChackOut = True
                if not CommandUtils.gitChackOut(path,versionS):
                    success = False
            if success:
                # 拉取新代码
                pullB = CommandUtils.gitPull(path)
                if pullB == 1 :
                    return 1
                elif pullB == 2 and needChackOut:
                    return 1
                else:
                    return pullB
        return 0

    @staticmethod
    def moduleOperator(path, gitPath, version):
        # 克隆项目
        if ModuleUtils.moduleClone(path, gitPath):
            # 拉取新代码
            return ModuleUtils.modulePull(path, version)
        else:
            return 0

    # 宿主app的操作
    @staticmethod
    def appOperator(appPath, appGitPath, appVersion="0.0.0"):
        success = ModuleUtils.moduleOperator(appPath, appGitPath, appVersion)
        if success == 1:
            print("宿主app操作成功")
        elif success == 2:
            print("宿主app不需要更新")
        else:
            print("宿主app操作失败")
            raise RuntimeError('宿主app操作失败')
            SysUtils.exit(False)

    @staticmethod
    def submoduleOperator(appPath, gitPath, moduleName, moduleVersion, forceMaven, environment, androidMvnConfig):
        print("submoduleOperator sys.path :" + sys.path[0])
        moduleGitPath = gitPath + moduleName.split(":")[-1] + ".git"
        modulePath = FileUtils.getModulePath(appPath, moduleName)
        success = ModuleUtils.moduleOperator(modulePath, moduleGitPath, moduleVersion)
        strGitUploadTime = "git_" + moduleName + "_" + moduleVersion;
        strMavenUploadTime = "maven_" + moduleName + "_" + moduleVersion + "_" + environment;

        if success == 0:
            print(moduleName + " git 操作失败")
            FileUtils.saveConfigDict(sys.path[0], androidMvnConfig)
            raise RuntimeError(moduleName +'git 操作失败')
            SysUtils.exit(False)
        elif success == 2 and forceMaven != 1:
            print(moduleName + " git 没有更新 ")
            gitUploadTime = 0
            mavenUploadTime = 0
            if androidMvnConfig.__contains__(strGitUploadTime):
                gitUploadTime = androidMvnConfig[strGitUploadTime]
            if androidMvnConfig.__contains__(strMavenUploadTime):
                mavenUploadTime = androidMvnConfig[strMavenUploadTime]
            print("gitUploadTime: " + str(gitUploadTime))
            print("mavenUploadTime: " + str(mavenUploadTime))
            if gitUploadTime < mavenUploadTime:
                print(moduleName + "不需要提交maven ")
                return

        if success == 1:
            androidMvnConfig[strGitUploadTime] = int(time.time())
            print(moduleName + " git 操作成功")
        if not environment.__eq__("git"):
            if CommandUtils.mavenUpload(modulePath, environment):
                androidMvnConfig[strMavenUploadTime] = int(time.time())
                print(moduleName + " maven 操作成功")
            else:
                print(moduleName + " maven 操作失败")

                FileUtils.saveConfigDict(sys.path[0], androidMvnConfig)
                raise RuntimeError(moduleName +'maven 操作失败')
                SysUtils.exit(False)
