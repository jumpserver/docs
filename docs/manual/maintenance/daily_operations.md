## 1 命令行工具 jmsctl

JumpServer 默认的安装脚本位于 `<安装包解压路径>/jmsctl.sh`。同时，JumpServer 支持命令行工具 `jmsctl`。

> 注意：安装后 JumpServer 安装包可删除，但解压后的目录不可删除。

`jmsctl` 命令可以在服务器的任一目录执行，`./jmsctl.sh` 需要切换至安装目录下执行。

### 1.1 命令使用格式

- `jmsctl [COMMAND]`
- `./jmsctl [COMMAND]` (需切换至安装包解压目录下执行)

### 1.2 命令参数详解
| 命令 | 说明 |
| :--- | :--- |
| `jmsctl help` | 获取帮助 |
| `jmsctl start` | 启动 JumpServer 服务的所有容器 |
| `jmsctl stop` | 停止 JumpServer 服务的所有容器 |
| `jmsctl down` | 关闭并移除 JumpServer 服务的所有容器 |
| `jmsctl restart` | 重启 JumpServer 服务的所有容器 |
| `jmsctl status` | 查看 JumpServer 服务的容器运行状态 |
| `jmsctl backup_db` | 备份 JumpServer 数据库文件 |
| `jmsctl uninstall` | 卸载 JumpServer 服务（操作此项会删除所有与 JumpServer 相关的数据，操作前需谨慎） |
| `jmsctl restore_db` | 恢复数据库数据，使用备份的 SQL 文件来恢复数据库信息 |

> 注意：`jmsctl restart/down` 命令会删除容器或重建容器。服务会中断，但持久化目录数据以及业务数据不受影响。

## 2 修改配置文件

### 2.1 配置文件详解

以下为 JumpServer 默认参数解释：
!!! tip ""
    ```ini
    # JumpServer configuration file example.
    # 如果不了解用途可以跳过修改此配置文件, 系统会自动填入
    # 完整参数文档 https://docs.jumpserver.org/zh/v3/guide/env/

    ################################## 镜像配置 ###################################
    # 国内连接 docker.io 会超时或下载速度较慢, 开启此选项使用华为云镜像加速
    # 取代旧版本 DOCKER_IMAGE_PREFIX
    # DOCKER_IMAGE_MIRROR=1

    # 镜像拉取规则 Always, IfNotPresent
    # Always 表示每次都会拉取最新镜像, IfNotPresent 表示本地不存在镜像时才会拉取
    # IMAGE_PULL_POLICY=Always

    ################################## 安装配置 ###################################
    # JumpServer 数据库持久化目录, 默认情况下录像、任务日志都在此目录
    # 请根据实际情况修改, 升级时备份的数据库文件(.sql)和配置文件也会保存到该目录
    VOLUME_DIR=/data/jumpserver  # JumpServer的持久化文件保存目录

    # 加密密钥, 迁移请保证 SECRET_KEY 与旧环境一致, 请勿使用特殊字符串
    # (*) Warning: Keep this value secret.
    # (*) 勿向任何人泄露 SECRET_KEY
    SECRET_KEY=NzhhNzNiNDItNmE0OC0wNTc0LTZlYzYtMzk1Mzk2ZDNhNjQ5  # 系统用来加密解密的key

    # 组件向 core 注册使用的 token, 迁移请保持 BOOTSTRAP_TOKEN 与旧环境一致,
    # 请勿使用特殊字符串
    # (*) Warning: Keep this value secret.
    # (*) 勿向任何人泄露 BOOTSTRAP_TOKEN
    BOOTSTRAP_TOKEN=NzhhNzNiNDItNmE0OC0wNTc0    # 其他组件用来向JumpServer注册使用的token

    # 日志等级 INFO, WARN, ERROR
    LOG_LEVEL=ERROR  # 日志级别，可以调整为DEBUG模式，输入更详细的日志信息，需注意产生的日志大小

    # JumpServer 容器使用的网段, 请勿与现有的网络冲突, 根据实际情况自行修改
    DOCKER_SUBNET=192.168.250.0/24  # JumpServer相关的容器的IP地址

    # ipv6 nat, 正常情况下无需开启
    # 如果宿主不支持 ipv6 开启此选项将会导致无法获取真实的客户端 ip 地址
    USE_IPV6=0
    DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

    ################################# DB 配置 ##################################
    # 外置数据库需要输入正确的数据库信息, 内置数据库系统会自动处理
    #
    DB_ENGINE=postgresql  # 指定数据库类型，可选mysql/postgresql
    DB_HOST=postgresql  # 数据库的连接地址，当地址为postgresql时。默认拉起PostgreSQL容器。
    DB_PORT=5432   # 数据库的连接端口
    DB_USER=postgres    # 数据库的连接用户
    DB_PASSWORD=1a703974685f00c6622fa5ea87  # 数据库的连接用户密码
    DB_NAME=jumpserver     # 数据库的连接数据库，即写入JumpServer数据的数据库

    # 如果外置 MySQL 需要开启 TLS/SSL 连接, 参考 https://docs.jumpserver.org/zh/v3/installation/security_setup/mysql_ssl/
    # DB_USE_SSL=true

    ################################# Redis 配置 ##################################
    # 外置 Redis 需要请输入正确的 Redis 信息, 内置 Redis 系统会自动处理
    REDIS_HOST=redis  # Redis数据库的连接地址，当地址为Redis时，默认拉起Redis容器。
    REDIS_PORT=6379  # Redis数据库的连接端口
    REDIS_PASSWORD=NzhhNzNiNDItNmE0OC0wNTc0LT   # Redis数据库的连接密码

    # 如果使用外置 Redis Sentinel, 请手动填写下面内容
    # REDIS_SENTINEL_HOSTS=mymaster/192.168.100.1:26379,192.168.100.1:26380,192.168.100.1:26381
    # REDIS_SENTINEL_PASSWORD=your_sentinel_password
    # REDIS_PASSWORD=your_redis_password
    # REDIS_SENTINEL_SOCKET_TIMEOUT=5

    # 如果外置 Redis 需要开启 TLS/SSL 连接, 参考 https://docs.jumpserver.org/zh/v3/installation/security_setup/redis_ssl/
    # REDIS_USE_SSL=true

    ################################## 访问配置 ###################################
    # 对外提供服务端口, 如果与现有服务冲突请自行修改
    HTTP_PORT=80    # JumpServer的Web界面访问端口

    ################################# HTTPS 配置 #################################
    # 参考 https://docs.jumpserver.org/zh/v3/installation/proxy/ 配置
    # HTTPS_PORT=443
    # SERVER_NAME=your_domain_name
    # SSL_CERTIFICATE=your_cert
    # SSL_CERTIFICATE_KEY=your_cert_key
    #

    # Nginx 文件上传下载大小限制
    CLIENT_MAX_BODY_SIZE=4096m

    ################################## 组件配置 ###################################
    # 组件注册使用, 默认情况下向 core 容器注册, 集群环境需要修改为集群 vip 地址
    #
    CORE_HOST=http://core:8080   # JumpServer项目的URL，API请求注册使用
    PERIOD_TASK_ENABLED=true  

    # Core Session 定义,
    # SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期,
    # SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # 可信任 DOMAINS 定义,
    # 定义可信任的访问 IP, 请根据实际情况修改, 如果是公网 IP 请改成对应的公网 IP,
    # DOMAINS="demo.jumpserver.org:443"
    # DOMAINS="172.17.200.191:80"
    # DOMAINS="demo.jumpserver.org:443,172.17.200.191:80"
    DOMAINS="10.1.12.47:80"

    # 配置不需要启动的组件, 默认所有组件都会开启, 如果不需要某个组件可以通过设置 {组件名称}_ENABLED 为 0 关闭
    # CORE_ENABLED=0
    # CELERY_ENABLED=0
    # KOKO_ENABLED=0
    # LION_ENABLED=0
    # MAGNUS_ENABLED=0
    # CHEN_ENABLED=0
    # Lion 开启字体平滑, 优化体验
    JUMPSERVER_ENABLE_FONT_SMOOTHING=true

    ################################# XPack配置 #################################
    # XPack 包, 开源版本设置无效
    SSH_PORT=2222   # JumpServer的ssh方式访问的端口
    RDP_PORT=3389   # RDP协议连接资产使用的端口（Razor）
    XRDP_PORT=3390  # RDP协议连接资产使用的端口（XRDP）
    MAGNUS_MYSQL_PORT=33061  # JumpServer使用Magnus组件连接MySQL数据库时使用的端口
    MAGNUS_MARIADB_PORT=33062 # JumpServer使用Magnus组件连接Mariadb数据库时使用的端口
    MAGNUS_REDIS_PORT=63790  # JumpServer使用Magnus组件连接Redis数据库时使用的端口
    MAGNUS_POSTGRESQL_PORT=54320  # JumpServer使用Magnus组件连接PostgreSQL数据库时使用的端口
    MAGNUS_SQLSERVER_PORT=14330   # JumpServer使用Magnus组件连接SQL Server数据库时使用的端口
    MAGNUS_ORACLE_PORT=15210   # JumpServer使用Magnus组件连接Oracle数据库时使用的端口
    XRDP_ENABLED=0

    ################################## 其他配置 ##################################
    # 终端使用宿主 HOSTNAME 标识, 首次安装自动生成
    SERVER_HOSTNAME=jumpserver-v4

    # 使用内置 SLB, 如果 Web 页面获取到的客户端 IP 地址不正确, 请将 USE_LB 设置为 0
    # USE_LB 设置为 1 时, 使用配置 proxy_set_header X-Forwarded-For $remote_addr
    # USE_LB 设置为 0 时, 使用配置proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for
    USE_LB=1

    # 当前运行的 JumpServer 版本号, 安装和升级完成后自动生成
    CURRENT_VERSION=v4.10.6
    ```

> 其他参数（默认参数或其他可自行添加的参数）请参考：[系统参数说明](env.md)

### 2.2 修改 config.txt

JumpServer 的核心配置文件为 `config.txt`，默认位置：`/opt/jumpserver/config/config.txt`。

如需要在 JumpServer 运行过程中更改 `config.txt` 文件中的内容，需要通过 `jmsctl restart` 命令重启 JumpServer 服务。

### 2.3 修改其他配置文件

JumpServer 在运行过程中，修改其他配置文件中的所有参数，均需要重启 JumpServer 进行加载。例如：

- nginx 的配置文件（`/opt/jumpserver/config/nginx/lb_http_server.conf`）
- MySQL 的配置文件（`/opt/jumpserver/config/mariadb/mariadb.cnf`）
- PostgreSQL 的配置文件（`/data/jumpserver/postgresql/data/postgresql.conf`）

如需要在 JumpServer 运行过程中更改上述文件中的内容，需要通过 `jmsctl restart` 命令重启 JumpServer 服务。

> 注意:数据库更改操作建议提前备份数据。

## 3 数据库备份

JumpServer 运行中，为防止 JumpServer 系统故障导致数据丢失，需要定时对 JumpServer 数据库进行备份。

### 3.1 命令行工具备份

!!! tip ""
    ```bash
    jmsctl backup_db
    ```

### 3.2 手动备份命令

#### MySQL 手动备份

> 注：内置数据库需要进入容器执行

!!! tip ""
    ```bash
    mysqldump -u$登录用户 -p$登录用户密码 jumpserver > jumpserver-$(date +"%Y-%m-%d").sql
    ```

#### PostgreSQL 手动备份

> 注：内置数据库需要进入容器执行

!!! tip ""
    ```bash
    pg_dump -U $登录用户 -h localhost -d jumpserver -f jumpserver-$(date +"%Y-%m-%d").dump
    ```

## 4 数据库恢复

当数据库节点宕机、升级失败或其他场景需要回滚数据库时，可参考以下操作。

> 注意：数据库回滚的前提是之前有进行数据库备份工作。

### 4.1 单节点数据库命令行工具恢复

!!! tip ""
    ```bash
    jmsctl restore_db <backup_file_path>  
    # 文件路径参数无法使用相对路径。被封文件默认位置在 /data/jumpserver/db_backup 目录下。
    ```

### 4.2 手动恢复命令
#### MySQL 单节点数据库回滚

> 注：内置数据库需要进入容器执行

!!! tip ""
    ```bash
    # 1. 停止 JumpServer 服务
    jmsctl stop
    
    # 2. 恢复数据库
    mysql -u$登录用户 -p$登录用户密码 jumpserver < /path/to/backup/jumpserver-YYYY-MM-DD.sql
    
    # 3. 启动 JumpServer 服务
    jmsctl start
    ```

#### PostgreSQL 单节点数据库回滚

> 注：内置数据库需要进入容器执行

!!! tip ""
    ```bash
    # 1. 停止 JumpServer 服务
    jmsctl stop
    
    # 2. 恢复数据库
    psql -U $登录用户 -h localhost -d jumpserver -f /path/to/backup/jumpserver-YYYY-MM-DD.dump
    
    # 3. 启动 JumpServer 服务
    jmsctl start
    ```
### 4.3 多节点数据库恢复

!!! info "企业版客户如果数据库架构复杂，建议在企业客户支持群中联系客户成功团队获取恢复帮助。"

需要根据具体的数据库集群架构，参考对应数据库的集群恢复方案进行操作。


