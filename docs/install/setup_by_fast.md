# 安装文档

!!! info "说明"
    全新安装的 Linux  
    需要连接 互联网  
    使用 root 用户执行  

??? info "可以使用由 [华为云](https://www.huaweicloud.com/) 提供的容器镜像服务 :heart:{: .heart }"
    | 区域          | 镜像仓库地址                         | 配置文件 /opt/jumpserver/config/config.txt                |
    | :----------- | :----------------------------------- | -------------------------------------------------------- |
    | 华北-北京一   | swr.cn-north-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com     |
    | 华北-北京四   | swr.cn-north-4.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-4.myhuaweicloud.com     |
    | 华南-广州     | swr.cn-south-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com     |
    | 华东-上海一   | swr.cn-east-3.myhuaweicloud.com      | DOCKER_IMAGE_PREFIX=swr.cn-east-3.myhuaweicloud.com      |
    | 亚太-香港     | swr.ap-southeast-1.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-1.myhuaweicloud.com |
    | 亚太-新加坡   | swr.ap-southeast-3.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-3.myhuaweicloud.com |

## 安装方式

- [安装演示视频](https://www.bilibili.com/video/bv19a4y1i7i9)

!!! info "外置环境要求"
    - 推荐使用外置 数据库 和 Redis, 方便日后扩展升级

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 6.0  |
| MariaDB | >= 10.2 |    |       |         |

=== "自动部署"
    !!! tip ""
        ```sh
        # 默认会安装到 /opt/jumpserver-installer-{{ jumpserver.version }} 目录
        curl -sSL https://github.com/jumpserver/jumpserver/releases/download/{{ jumpserver.version }}/quick_start.sh | bash
        ```

=== "手动部署"
    !!! tip ""
        ```sh
        cd /opt
        wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.version }}
        ```
        ```sh
        # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
        cat config-example.txt
        ```

    ???+ info "配置文件说明"
        ```vim
        # 以下设置如果为空系统会自动生成随机字符串填入
        ## 迁移请修改 SECRET_KEY 和 BOOTSTRAP_TOKEN 为原来的设置
        ## 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ## 安装配置, amd64 默认使用华为云加速下载, arm64 请注释掉 DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        # DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        VOLUME_DIR=/opt/jumpserver
        DOCKER_DIR=/var/lib/docker
        SECRET_KEY=
        BOOTSTRAP_TOKEN=
        LOG_LEVEL=ERROR

        ##  MySQL 配置, USE_EXTERNAL_MYSQL=1 表示使用外置数据库, 请输入正确的 MySQL 信息
        USE_EXTERNAL_MYSQL=0
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        ##  Redis 配置, USE_EXTERNAL_REDIS=1 表示使用外置数据库, 请输入正确的 Redis 信息
        USE_EXTERNAL_REDIS=0
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        ## Compose 项目设置, 如果 192.168.250.0/24 网段与你现有网段冲突, 请修改然后重启 JumpServer
        COMPOSE_PROJECT_NAME=jms
        COMPOSE_HTTP_TIMEOUT=3600
        DOCKER_CLIENT_TIMEOUT=3600
        DOCKER_SUBNET=192.168.250.0/24

        ## IPV6 设置, 容器是否开启 ipv6 nat, USE_IPV6=1 表示开启, 为 0 的情况下 DOCKER_SUBNET_IPV6 定义不生效
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=2001:db8:10::/64

        ## Nginx 配置, USE_LB=1 表示开启, 为 0 的情况下, HTTPS_PORT 定义不生效
        HTTP_PORT=80
        SSH_PORT=2222
        RDP_PORT=3389

        USE_LB=0
        HTTPS_PORT=443

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=true

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080

        # 额外的配置
        CURRENT_VERSION=
        ```
        ```sh
        ./jmsctl.sh install
        ./jmsctl.sh start
        ```


## 使用方式

!!! tip ""
    ```sh
    # 安装完成后配置文件 /opt/jumpserver/config/config.txt
    ```
    ```sh
    cd /opt/jumpserver-installer-{{ jumpserver.version }}

    # 启动
    ./jmsctl.sh start

    # 停止
    ./jmsctl.sh down

    # 卸载
    ./jmsctl.sh uninstall

    # 帮助
    ./jmsctl.sh -h
    ```

!!! tip ""
    ```sh
    # 重新安装
    ./jmsctl.sh uninstall
    ./jmsctl.sh install
    ```

后续的使用请参考 [安全建议](install_security.md) [快速入门](../../admin-guide/quick_start/)  
