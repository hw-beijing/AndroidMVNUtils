# AndroidMVNUtils
androdi studio 项目的maven管理,自动拉取git代码,自动提交相应maven
本程序针对妙健康主版本开发
项目条件:
1.宿主工程和子模块工程分不同git仓库
2.宿主工程和子模块工程git仓木在同一目录
3.所有打开的setting项目存在分支
4,所有git项目分支号为 "v版本号"


调用参数
1. app的git目录
2. app的版本号
3. app的本地路径
4. 环境 
   环境可以不传,此环境只针对妙健康的项目的 开发,测试,生产 环境
