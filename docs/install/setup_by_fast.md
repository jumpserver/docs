# 安装文档

!!! info "说明"
    全新安装的 Centos7 (7.x)  
    需要连接 互联网  
    使用 root 用户执行  

- [安装视频](https://www.bilibili.com/video/bv19a4y1i7i9)

- 国内用户可以使用由华为云提供的容器镜像服务

| 区域          | 镜像仓库地址                      | 使用方式                                                     |
| :----------- | :------------------------------- | :----------------------------------------------------------- |
| 华北-北京一   | swr.cn-north-1.myhuaweicloud.com | export DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com  |
| 华北-北京四   | swr.cn-north-4.myhuaweicloud.com | export DOCKER_IMAGE_PREFIX=swr.cn-north-4.myhuaweicloud.com  |
| 华南-广州     | swr.cn-south-1.myhuaweicloud.com | export DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com  |
| 华东-上海一   | swr.cn-east-3.myhuaweicloud.com  | export DOCKER_IMAGE_PREFIX=swr.cn-east-3.myhuaweicloud.com   |

## 安装方式

!!! info "外置环境要求"
    - Redis >= 5.0.0
    - MySQL >= 5.7
    - MariaDB >= 10.2
    - 推荐使用外置 数据库 和 Redis, 方便日后扩展升级

=== "自动部署"
    !!! tip ""
        ```sh
        export DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com
        curl -sSL https://github.com/jumpserver/jumpserver/releases/download/v2.7.1/quick_start.sh | bash

        # 如果出现问题
        cd /opt/jumpserver-installer-v2.7.1
        ./jmsctl.sh --help
        ```

=== "手动部署"
    !!! tip ""
        ```sh
        export DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com
        cd /opt
        yum -y install wget
        wget https://github.com/jumpserver/installer/releases/download/v2.7.1/jumpserver-installer-v2.7.1.tar.gz
        tar -xf jumpserver-installer-v2.7.1.tar.gz
        cd jumpserver-installer-v2.7.1
        cat config-example.txt
        ```

    ???+ info "配置文件说明"
        ```vim
        # 以下设置默认情况下不需要修改

        # 说明
        #### 这是项目总的配置文件, 会作为环境变量加载到各个容器中
        #### 格式必须是 KEY=VALUE 不能有空格等

        # Compose项目设置
        COMPOSE_PROJECT_NAME=jms
        COMPOSE_HTTP_TIMEOUT=3600
        DOCKER_CLIENT_TIMEOUT=3600
        DOCKER_SUBNET=192.168.250.0/24

        ## IPV6
        DOCKER_SUBNET_IPV6=2001:db8:10::/64
        USE_IPV6=0

        ### 持久化目录, 安装启动后不能再修改, 除非移动原来的持久化到新的位置
        VOLUME_DIR=/opt/jumpserver

        ## 是否使用外部MYSQL和REDIS
        USE_EXTERNAL_MYSQL=0
        USE_EXTERNAL_REDIS=0

        ## Nginx 配置，这个Nginx是用来分发路径到不同的服务
        HTTP_PORT=80
        HTTPS_PORT=443
        SSH_PORT=2222

        ## LB 配置, 这个Nginx是HA时可以启动负载均衡到不同的主机
        USE_LB=0
        LB_HTTP_PORT=80
        LB_HTTPS_PORT=443
        LB_SSH_PORT=2223

        ## Task 配置
        USE_TASK=1

        ## XPack
        USE_XPACK=0

        # Koko配置
        CORE_HOST=http://core:8080
        ENABLE_PROXY_PROTOCOL=true

        # Core 配置
        ### 启动后不能再修改，否则密码等等信息无法解密
        SECRET_KEY=
        BOOTSTRAP_TOKEN=
        LOG_LEVEL=INFO
        # SESSION_COOKIE_AGE=86400
        # SESSION_EXPIRE_AT_BROWSER_CLOSE=false

        ## MySQL数据库配置
        DB_ENGINE=mysql
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        ## Redis配置
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        ### Keycloak 配置方式
        ### AUTH_OPENID=true
        ### BASE_SITE_URL=https://jumpserver.company.com/
        ### AUTH_OPENID_SERVER_URL=https://keycloak.company.com/auth
        ### AUTH_OPENID_REALM_NAME=cmp
        ### AUTH_OPENID_CLIENT_ID=jumpserver
        ### AUTH_OPENID_CLIENT_SECRET=
        ### AUTH_OPENID_SHARE_SESSION=true
        ### AUTH_OPENID_IGNORE_SSL_VERIFICATION=true

        # Guacamole 配置
        JUMPSERVER_SERVER=http://core:8080
        JUMPSERVER_KEY_DIR=/config/guacamole/data/key/
        JUMPSERVER_RECORD_PATH=/config/guacamole/data/record/
        JUMPSERVER_DRIVE_PATH=/config/guacamole/data/drive/
        JUMPSERVER_ENABLE_DRIVE=true
        JUMPSERVER_CLEAR_DRIVE_SESSION=true
        JUMPSERVER_CLEAR_DRIVE_SCHEDULE=24

        # Mysql 容器配置
        MYSQL_ROOT_PASSWORD=
        MYSQL_DATABASE=jumpserver
        ```

??? warning "如果 export 的镜像加速方法无效请查看此处的帮助文档"
    ```sh
    docker pull swr.cn-south-1.myhuaweicloud.com/jumpserver/core:v2.7.1
    docker tag swr.cn-south-1.myhuaweicloud.com/jumpserver/core:v2.7.1 jumpserver/core:v2.7.1
    docker rmi -f swr.cn-south-1.myhuaweicloud.com/jumpserver/core:v2.7.1
    # 其他镜像也可以使用这样的方式拉, 后续版本我们会在安装脚本里面优化
    ```

## 使用方式

- 安装目录 /opt/jumpserver-install-v2.7.1

!!! tip "Install"
    ```sh
    ./jmsctl.sh install
    ```

!!! tip "Help"
    ```sh
    ./jmsctl.sh -h
    ```

!!! tip "Upgrade"
    ```sh
    ./jmsctl.sh check_update
    ```

后续的使用请参考 [安全建议](install_security.md) [快速入门](../../admin-guide/quick_start/)  
