
!!! info "企业版客户如果架构复杂，建议在企业客户支持群中联系客户成功团队获取升级帮助。"

> 注意：</br>
> 1. 如您的环境需要升级，建议首先查看官方网站的 release note，了解近期版本变化，选择适合当前环境的版本。</br>
> 2. JumpServer 服务升级过程中服务会停止一段时间（根据环境情况，时间为 10~30 分钟），建议至少申请一个小时的变更窗口，留足验证以及回退时间。


JumpServer 升级服务采用一键快速升级方式，此过程会重启整个 JumpServer 平台的所有服务，并自动变更数据库表结构；升级操作步骤如下：

## 1 下载并上传安装包

- 社区版安装包需要从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}
- 企业版安装包在飞致云 support 门户中下载最新安装包或在企业支持群中联系相关客户成功团队获取。

下载完成后，需要上传安装包至服务器后台。

## 2 备份原环境服务数据

```bash
jmsctl backup_db
```

## 3 解压安装包并进入新版本安装包目录

```bash
tar -xf jumpserver-ee-{{ jumpserver.tag }}-x86_64.tar.gz
cd jumpserver-ee-{{ jumpserver.tag }}-x86_64/
```

## 4 执行升级脚本
!!! warning "此步骤需要进入新版本安装包内执行，请注意路径。"

```bash
./jmsctl.sh upgrade
```

## 5 启动 JumpServer 服务

```bash
./jmsctl.sh start
```
