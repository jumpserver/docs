##  升级步骤

> 注：
> 1. 如您的环境需要升级，建议首先查看官方网站的 release note，了解近期版本变化，选择适合当前环境的版本。
> 2. 升级操作建议联系售后技术支持，了解版本升级风险、升级变更时间等。
> 3. 如需自行操作，需注意：JumpServer 服务升级过程中服务会停止一段时间（根据环境情况，时间为 10~30 分钟），建议至少申请一个小时的变更窗口，留足验证以及回退时间。

JumpServer 升级服务采用一键快速升级方式，此过程会重启整个 JumpServer 平台的所有服务，并自动变更数据库表结构；升级操作步骤如下：

### （一）下载并上传安装包
在飞致云 support 门户中下载最新安装包，并上传至 JumpServer 后端服务器中。

### （二）备份原环境服务数据
**方法一**：【任意目录可执行】
!!! tip ""
    ```bash
    jmsctl backup_db
    ```

**方法二**：【安装包目录下执行】
!!! tip ""
    ```bash
    cd /opt/jumpserver-ee-v4.10.6-x86_64/
    ./jmsctl.sh backup_db
    ```

### （三）解压安装包并进入目录
!!! tip ""
    ```bash
    tar -xf jumpserver-ee-v4.10.7-x86_64.tar.gz
    cd jumpserver-ee-v4.10.7-x86_64/
    ```

### （四）拉取升级版本所需镜像
!!! tip ""
    ```bash
    ./jmsctl.sh load_image
    ```

### （五）执行升级脚本
!!! tip ""
    ```bash
    ./jmsctl.sh upgrade
    ```

### （六）启动 JumpServer 服务
!!! tip ""
    ```bash
    ./jmsctl.sh start
    ```

> 注意：如为特殊部署场景，升级步骤需根据实际部署情况调整，请联系售后技术工程师。