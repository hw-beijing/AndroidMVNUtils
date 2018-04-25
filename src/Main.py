import os
import sys
from utils.CommandUtils import CommandUtils
from utils.FileUtils import FileUtils
from utils.StringUtils import StringUtils
from utils.SysUtils import SysUtils
from utils.ModuleUtils import ModuleUtils

print(sys.argv)
argvLen = len(sys.argv)
print(argvLen)
# git目录
gitPath = ""
# app git目录
appGitPath = ""
# app 的名字
appName = ""
# app的版本号
appVersion = ""
# app的路径
appPath = ""
# maven环境
environment = ""

if argvLen >= 2:
    appGitPath = sys.argv[1]
    appName = appGitPath.split("/")[1].replace(".git", "")
    gitPath = appGitPath.replace(appGitPath.split("/")[1], "")
if argvLen >= 3:
    appVersion = sys.argv[2]
if argvLen >= 4:
    appPath = sys.argv[3]
if argvLen >= 5:
    environment = sys.argv[4]

if StringUtils.formatString(appPath) == "":
    appPath = os.getcwd()
print("appName : " + appName)
print("gitPath : " + gitPath)
print("appGitPath : " + appGitPath)
print("appVersion : " + appVersion)
print("appPath : " + appPath)
print("environment : " + environment)

if gitPath != "" and appVersion != "" and appPath != "":
    print("参数检测通过")
    # 宿主app的操作
    ModuleUtils.appOperator(appPath, appGitPath, appVersion)

    modules = FileUtils.readSetting(appPath)
    modulesMap = FileUtils.readMainGradle(appPath, modules)
    for moduleName in modules:
        print("---------"+moduleName)
        if moduleName in modulesMap:
            moduleVersion = modulesMap[moduleName]
            ModuleUtils.submoduleOperator(appPath, gitPath, moduleName, moduleVersion, environment)
else:
    print("参数检测未通过")
