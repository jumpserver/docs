# 离线安装

!!! info "离线包解压需要 tar 命令, 参考 [环境要求](./requirements.md) 手动安装"

| OS/Arch       | Architecture | Linux Kernel | Offline Name                                                                                 |
| :------------ | :----------- | :----------- | :------------------------------------------------------------------------------------------- |
| linux/amd64   | x86_64       | >= 4.0       | jumpserver-offline-installer-{{ jumpserver.tag }}-amd64.tar.gz   |
| linux/arm64   | aarch64      | >= 4.0       | jumpserver-offline-installer-{{ jumpserver.tag }}-arm64.tar.gz   |
| linux/loong64 | loongarch64  | == 4.19      | jumpserver-offline-installer-{{ jumpserver.tag }}-loong64.tar.gz |

## 1. 安装部署

=== "linux/amd64"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-amd64.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-amd64
        ```
        ```sh
        # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
        cat config-example.txt
        ```
        ```vim
        # JumpServer configuration file example.
        #
        # 如果不了解用途可以跳过修改此配置文件, 系统会自动填入
        # 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ################################## 镜像配置 ###################################
        #
        # 国内连接 docker.io 会超时或下载速度较慢, 开启此选项使用华为云镜像加速
        # 取代旧版本 DOCKER_IMAGE_PREFIX
        #
        # DOCKER_IMAGE_MIRROR=1

        ################################## 安装配置 ###################################
        #
        # JumpServer 数据库持久化目录, 默认情况下录像、任务日志都在此目录
        # 请根据实际情况修改, 升级时备份的数据库文件(.sql)和配置文件也会保存到该目录
        #
        VOLUME_DIR=/data/jumpserver

        # 加密密钥, 迁移请保证 SECRET_KEY 与旧环境一致, 请勿使用特殊字符串
        # (*) Warning: Keep this value secret.
        # (*) 勿向任何人泄露 SECRET_KEY
        #
        SECRET_KEY=

        # 组件向 core 注册使用的 token, 迁移请保持 BOOTSTRAP_TOKEN 与旧环境一致,
        # 请勿使用特殊字符串
        # (*) Warning: Keep this value secret.
        # (*) 勿向任何人泄露 BOOTSTRAP_TOKEN
        #
        BOOTSTRAP_TOKEN=

        # 日志等级 INFO, WARN, ERROR
        #
        LOG_LEVEL=ERROR

        # JumpServer 容器使用的网段, 请勿与现有的网络冲突, 根据实际情况自行修改
        #
        DOCKER_SUBNET=192.168.250.0/24

        # ipv6 nat, 正常情况下无需开启
        # 如果宿主不支持 ipv6 开启此选项将会导致无法获取真实的客户端 ip 地址
        #
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

        ################################# MySQL 配置 ##################################
        # 外置 MySQL 需要输入正确的 MySQL 信息, 内置 MySQL 系统会自动处理
        #
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        # 如果外置 MySQL 需要开启 TLS/SSL 连接, 参考 https://docs.jumpserver.org/zh/master/install/install_security/#ssl
        #
        # DB_USE_SSL=True

        ################################# Redis 配置 ##################################
        # 外置 Redis 需要请输入正确的 Redis 信息, 内置 Redis 系统会自动处理
        #
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        # 如果使用外置 Redis Sentinel, 请手动填写下面内容
        #
        # REDIS_SENTINEL_HOSTS=mymaster/192.168.100.1:26379,192.168.100.1:26380,192.168.100.1:26381
        # REDIS_SENTINEL_PASSWORD=your_sentinel_password
        # REDIS_PASSWORD=your_redis_password
        # REDIS_SENTINEL_SOCKET_TIMEOUT=5

        # 如果外置 Redis 需要开启 TLS/SSL 连接, 参考 https://docs.jumpserver.org/zh/master/install/install_security/#redis-ssl
        #
        # REDIS_USE_SSL=True

        ################################## 访问配置 ###################################
        # 对外提供服务端口, 如果与现有服务冲突请自行修改
        #
        HTTP_PORT=80
        SSH_PORT=2222
        MAGNUS_MYSQL_PORT=33061
        MAGNUS_MARIADB_PORT=33062
        MAGNUS_REDIS_PORT=63790

        ################################# HTTPS 配置 #################################
        # 参考 https://docs.jumpserver.org/zh/master/admin-guide/proxy/ 配置
        #
        # HTTPS_PORT=443
        # SERVER_NAME=your_domain_name
        # SSL_CERTIFICATE=your_cert
        # SSL_CERTIFICATE_KEY=your_cert_key
        #

        # Nginx 文件上传下载大小限制
        #
        CLIENT_MAX_BODY_SIZE=4096m

        ################################## 组件配置 ###################################
        # 组件注册使用, 默认情况下向 core 容器注册, 集群环境需要修改为集群 vip 地址
        #
        CORE_HOST=http://core:8080
        PERIOD_TASK_ENABLED=True

        # Core Session 定义,
        # SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期,
        # SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
        #
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=True

        # 可信任 DOMAINS 定义,
        # 定义可信任的访问 IP, 请根据实际情况修改, 如果是公网 IP 请改成对应的公网 IP,
        # DOMAINS="demo.jumpserver.org"
        # DOMAINS="172.17.200.191"
        # DOMAINS="demo.jumpserver.org,172.17.200.191"
        DOMAINS=

        # Lion 开启字体平滑, 优化体验
        #
        JUMPSERVER_ENABLE_FONT_SMOOTHING=True

        ################################# XPack 配置 #################################
        # XPack 包, 开源版本设置无效
        #
        RDP_PORT=3389
        MAGNUS_POSTGRESQL_PORT=54320
        MAGNUS_ORACLE_PORTS=30000-30030

        ################################## 其他配置 ##################################
        # 终端使用宿主 HOSTNAME 标识, 首次安装自动生成
        #
        SERVER_HOSTNAME=${HOSTNAME}

        # 当前运行的 JumpServer 版本号, 安装和升级完成后自动生成
        #
        CURRENT_VERSION=
        ```
        ```sh
        # 安装
        ./jmsctl.sh install

        # 启动
        ./jmsctl.sh start
        ```

    !!! info "安装完成后 JumpServer 配置文件路径为： /opt/jumpserver/config/config.txt"

    !!! tip ""
        ```sh
        cd jumpserver-offline-release-{{ jumpserver.tag }}-amd64

        # 启动
        ./jmsctl.sh start

        # 停止
        ./jmsctl.sh down

        # 卸载
        ./jmsctl.sh uninstall

        # 帮助
        ./jmsctl.sh -h
        ```

=== "linux/arm64"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/arm64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-arm64.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-arm64
        ```
        ```sh
        # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
        cat config-example.txt
        ```
        ```vim
        # JumpServer configuration file example.
        #
        # 如果不了解用途可以跳过修改此配置文件, 系统会自动填入
        # 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ################################## 镜像配置 ###################################
        #
        # 国内连接 docker.io 会超时或下载速度较慢, 开启此选项使用华为云镜像加速
        # 取代旧版本 DOCKER_IMAGE_PREFIX
        #
        # DOCKER_IMAGE_MIRROR=1

        ################################## 安装配置 ###################################
        #
        # JumpServer 数据库持久化目录, 默认情况下录像、任务日志都在此目录
        # 请根据实际情况修改, 升级时备份的数据库文件(.sql)和配置文件也会保存到该目录
        #
        VOLUME_DIR=/data/jumpserver

        # 加密密钥, 迁移请保证 SECRET_KEY 与旧环境一致, 请勿使用特殊字符串
        # (*) Warning: Keep this value secret.
        # (*) 勿向任何人泄露 SECRET_KEY
        #
        SECRET_KEY=

        # 组件向 core 注册使用的 token, 迁移请保持 BOOTSTRAP_TOKEN 与旧环境一致,
        # 请勿使用特殊字符串
        # (*) Warning: Keep this value secret.
        # (*) 勿向任何人泄露 BOOTSTRAP_TOKEN
        #
        BOOTSTRAP_TOKEN=

        # 日志等级 INFO, WARN, ERROR
        #
        LOG_LEVEL=ERROR

        # JumpServer 容器使用的网段, 请勿与现有的网络冲突, 根据实际情况自行修改
        #
        DOCKER_SUBNET=192.168.250.0/24

        # ipv6 nat, 正常情况下无需开启
        # 如果宿主不支持 ipv6 开启此选项将会导致无法获取真实的客户端 ip 地址
        #
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

        ################################# MySQL 配置 ##################################
        # 外置 MySQL 需要输入正确的 MySQL 信息, 内置 MySQL 系统会自动处理
        #
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        # 如果外置 MySQL 需要开启 TLS/SSL 连接, 参考 https://docs.jumpserver.org/zh/master/install/install_security/#ssl
        #
        # DB_USE_SSL=True

        ################################# Redis 配置 ##################################
        # 外置 Redis 需要请输入正确的 Redis 信息, 内置 Redis 系统会自动处理
        #
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        # 如果使用外置 Redis Sentinel, 请手动填写下面内容
        #
        # REDIS_SENTINEL_HOSTS=mymaster/192.168.100.1:26379,192.168.100.1:26380,192.168.100.1:26381
        # REDIS_SENTINEL_PASSWORD=your_sentinel_password
        # REDIS_PASSWORD=your_redis_password
        # REDIS_SENTINEL_SOCKET_TIMEOUT=5

        # 如果外置 Redis 需要开启 TLS/SSL 连接, 参考 https://docs.jumpserver.org/zh/master/install/install_security/#redis-ssl
        #
        # REDIS_USE_SSL=True

        ################################## 访问配置 ###################################
        # 对外提供服务端口, 如果与现有服务冲突请自行修改
        #
        HTTP_PORT=80
        SSH_PORT=2222
        MAGNUS_MYSQL_PORT=33061
        MAGNUS_MARIADB_PORT=33062
        MAGNUS_REDIS_PORT=63790

        ################################# HTTPS 配置 #################################
        # 参考 https://docs.jumpserver.org/zh/master/admin-guide/proxy/ 配置
        #
        # HTTPS_PORT=443
        # SERVER_NAME=your_domain_name
        # SSL_CERTIFICATE=your_cert
        # SSL_CERTIFICATE_KEY=your_cert_key
        #

        # Nginx 文件上传下载大小限制
        #
        CLIENT_MAX_BODY_SIZE=4096m

        ################################## 组件配置 ###################################
        # 组件注册使用, 默认情况下向 core 容器注册, 集群环境需要修改为集群 vip 地址
        #
        CORE_HOST=http://core:8080
        PERIOD_TASK_ENABLED=True

        # Core Session 定义,
        # SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期,
        # SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
        #
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=True

        # 可信任 DOMAINS 定义,
        # 定义可信任的访问 IP, 请根据实际情况修改, 如果是公网 IP 请改成对应的公网 IP,
        # DOMAINS="demo.jumpserver.org"
        # DOMAINS="172.17.200.191"
        # DOMAINS="demo.jumpserver.org,172.17.200.191"
        DOMAINS=

        # Lion 开启字体平滑, 优化体验
        #
        JUMPSERVER_ENABLE_FONT_SMOOTHING=True

        ################################# XPack 配置 #################################
        # XPack 包, 开源版本设置无效
        #
        RDP_PORT=3389
        MAGNUS_POSTGRESQL_PORT=54320
        MAGNUS_ORACLE_PORTS=30000-30030

        ################################## 其他配置 ##################################
        # 终端使用宿主 HOSTNAME 标识, 首次安装自动生成
        #
        SERVER_HOSTNAME=${HOSTNAME}

        # 当前运行的 JumpServer 版本号, 安装和升级完成后自动生成
        #
        CURRENT_VERSION=
        ```
        ```sh
        # 安装
        ./jmsctl.sh install

        # 启动
        ./jmsctl.sh start
        ```

    !!! info "安装完成后 JumpServer 配置文件路径为： /opt/jumpserver/config/config.txt"

    !!! tip ""
        ```sh
        cd jumpserver-offline-release-{{ jumpserver.tag }}-arm64

        # 启动
        ./jmsctl.sh start

        # 停止
        ./jmsctl.sh down

        # 卸载
        ./jmsctl.sh uninstall

        # 帮助
        ./jmsctl.sh -h
        ```

=== "linux/loong64"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/loong64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-loong64.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-loong64
        ```
        ```sh
        # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
        cat config-example.txt
        ```
        ```vim
        # JumpServer configuration file example.
        #
        # 如果不了解用途可以跳过修改此配置文件, 系统会自动填入
        # 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ################################## 镜像配置 ###################################
        #
        # 国内连接 docker.io 会超时或下载速度较慢, 开启此选项使用华为云镜像加速
        # 取代旧版本 DOCKER_IMAGE_PREFIX
        #
        # DOCKER_IMAGE_MIRROR=1

        ################################## 安装配置 ###################################
        #
        # JumpServer 数据库持久化目录, 默认情况下录像、任务日志都在此目录
        # 请根据实际情况修改, 升级时备份的数据库文件(.sql)和配置文件也会保存到该目录
        #
        VOLUME_DIR=/data/jumpserver

        # 加密密钥, 迁移请保证 SECRET_KEY 与旧环境一致, 请勿使用特殊字符串
        # (*) Warning: Keep this value secret.
        # (*) 勿向任何人泄露 SECRET_KEY
        #
        SECRET_KEY=

        # 组件向 core 注册使用的 token, 迁移请保持 BOOTSTRAP_TOKEN 与旧环境一致,
        # 请勿使用特殊字符串
        # (*) Warning: Keep this value secret.
        # (*) 勿向任何人泄露 BOOTSTRAP_TOKEN
        #
        BOOTSTRAP_TOKEN=

        # 日志等级 INFO, WARN, ERROR
        #
        LOG_LEVEL=ERROR

        # JumpServer 容器使用的网段, 请勿与现有的网络冲突, 根据实际情况自行修改
        #
        DOCKER_SUBNET=192.168.250.0/24

        # ipv6 nat, 正常情况下无需开启
        # 如果宿主不支持 ipv6 开启此选项将会导致无法获取真实的客户端 ip 地址
        #
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

        ################################# MySQL 配置 ##################################
        # 外置 MySQL 需要输入正确的 MySQL 信息, 内置 MySQL 系统会自动处理
        #
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        # 如果外置 MySQL 需要开启 TLS/SSL 连接, 参考 https://docs.jumpserver.org/zh/master/install/install_security/#ssl
        #
        # DB_USE_SSL=True

        ################################# Redis 配置 ##################################
        # 外置 Redis 需要请输入正确的 Redis 信息, 内置 Redis 系统会自动处理
        #
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        # 如果使用外置 Redis Sentinel, 请手动填写下面内容
        #
        # REDIS_SENTINEL_HOSTS=mymaster/192.168.100.1:26379,192.168.100.1:26380,192.168.100.1:26381
        # REDIS_SENTINEL_PASSWORD=your_sentinel_password
        # REDIS_PASSWORD=your_redis_password
        # REDIS_SENTINEL_SOCKET_TIMEOUT=5

        # 如果外置 Redis 需要开启 TLS/SSL 连接, 参考 https://docs.jumpserver.org/zh/master/install/install_security/#redis-ssl
        #
        # REDIS_USE_SSL=True

        ################################## 访问配置 ###################################
        # 对外提供服务端口, 如果与现有服务冲突请自行修改
        #
        HTTP_PORT=80
        SSH_PORT=2222
        MAGNUS_MYSQL_PORT=33061
        MAGNUS_MARIADB_PORT=33062
        MAGNUS_REDIS_PORT=63790

        ################################# HTTPS 配置 #################################
        # 参考 https://docs.jumpserver.org/zh/master/admin-guide/proxy/ 配置
        #
        # HTTPS_PORT=443
        # SERVER_NAME=your_domain_name
        # SSL_CERTIFICATE=your_cert
        # SSL_CERTIFICATE_KEY=your_cert_key
        #

        # Nginx 文件上传下载大小限制
        #
        CLIENT_MAX_BODY_SIZE=4096m

        ################################## 组件配置 ###################################
        # 组件注册使用, 默认情况下向 core 容器注册, 集群环境需要修改为集群 vip 地址
        #
        CORE_HOST=http://core:8080
        PERIOD_TASK_ENABLED=True

        # Core Session 定义,
        # SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期,
        # SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
        #
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=True

        # 可信任 DOMAINS 定义,
        # 定义可信任的访问 IP, 请根据实际情况修改, 如果是公网 IP 请改成对应的公网 IP,
        # DOMAINS="demo.jumpserver.org"
        # DOMAINS="172.17.200.191"
        # DOMAINS="demo.jumpserver.org,172.17.200.191"
        DOMAINS=

        # Lion 开启字体平滑, 优化体验
        #
        JUMPSERVER_ENABLE_FONT_SMOOTHING=True

        ################################# XPack 配置 #################################
        # XPack 包, 开源版本设置无效
        #
        RDP_PORT=3389
        MAGNUS_POSTGRESQL_PORT=54320
        MAGNUS_ORACLE_PORTS=30000-30030

        ################################## 其他配置 ##################################
        # 终端使用宿主 HOSTNAME 标识, 首次安装自动生成
        #
        SERVER_HOSTNAME=${HOSTNAME}

        # 当前运行的 JumpServer 版本号, 安装和升级完成后自动生成
        #
        CURRENT_VERSION=
        ```
        ```sh
        # 安装
        ./jmsctl.sh install

        # 启动
        ./jmsctl.sh start
        ```

    !!! info "安装完成后 JumpServer 配置文件路径为： /opt/jumpserver/config/config.txt"

    !!! tip ""
        ```sh
        cd jumpserver-offline-release-{{ jumpserver.tag }}-loong64

        # 启动
        ./jmsctl.sh start

        # 停止
        ./jmsctl.sh down

        # 卸载
        ./jmsctl.sh uninstall

        # 帮助
        ./jmsctl.sh -h
        ```

## 2. 环境访问
!!! info "安装成功后，通过浏览器访问登录 JumpServer"
    ```sh
    地址: http://<JumpServer服务器IP地址>:<服务运行端口>
    用户名: admin
    密码: admin
    ```

![登录页面](../../img/online_install_01.png)
