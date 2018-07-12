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
#是否将至maven 0不强制更新  1是强制更新
forceMaven = "0"

#是否操作宿主 0 不操作 1操作（默认）
operationApp = "1"




if argvLen >= 2:
    appGitPath = sys.argv[1]
    appName = appGitPath.split("/")[1].replace(".git", "")
    gitPath = appGitPath.replace(appGitPath.split("/")[1], "")
if argvLen >= 3:
    appVersion = sys.argv[2]
if argvLen >= 4:
    appPath = sys.argv[3]+os.sep
if argvLen >= 5:
    forceMaven = sys.argv[4]
if argvLen >= 6:
    operationApp = sys.argv[5]
if argvLen >= 7:
    environment = sys.argv[6]

if StringUtils.formatString(appPath) == "":
    appPath = os.getcwd()

if not appPath.endswith(os.sep):
    appPath = appPath + os.sep

print("appName : " + appName)
print("gitPath : " + gitPath)
print("appGitPath : " + appGitPath)
print("appVersion : " + appVersion)
print("appPath : " + appPath)
print("forceMaven : " + forceMaven)
print("operationApp : " + operationApp)
print("environment : " + environment)

if gitPath != "" and appVersion != "" and appPath != "":
    print("参数检测通过")
    # 宿主app的操作
    if operationApp.__eq__("1"):
        ModuleUtils.appOperator(appPath, appGitPath, appVersion)

    modules = FileUtils.readSetting(appPath)
    modulesMap = FileUtils.readMainGradle(appPath, modules)
    print(" ")
    print(" ")
    androidMvnConfig = FileUtils.readConfigDict(sys.path[0])
    print(str(androidMvnConfig))
    for moduleName in modules:
        if moduleName in modulesMap:
            print("")
            print("")
            print(moduleName+ " start--------------------------------------------------------------------")
            moduleVersion = modulesMap[moduleName]
            print("---------" + moduleName + " " + moduleVersion)
            if not environment.__eq__("version"):
                ModuleUtils.submoduleOperator(appPath, gitPath, moduleName, moduleVersion,forceMaven, environment, androidMvnConfig)
            print(moduleName+" end----------------------------------------------------------------------")
            print("")
            print("")
    FileUtils.saveConfigDict(sys.path[0], androidMvnConfig)
    print(str(androidMvnConfig))
else:
    print("参数检测未通过")
