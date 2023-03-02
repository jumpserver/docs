# 离线安装

!!! tip "[JumpServer 部署环境要求可点击后进行参考](../setup_linux_standalone/requirements.md)"

## 1 安装部署
??? info "国内可以使用由 [华为云](https://www.huaweicloud.com/) 提供的容器镜像服务"
    | 区域          | 镜像仓库地址                         | 配置文件 /opt/jumpserver/config/config.txt                | Kubernetes values.yaml                           | OS/ARCH        |
    | :----------- | :----------------------------------- | -------------------------------------------------------- | ------------------------------------------------ | -------------- |
    | 华北-北京一   | swr.cn-north-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com     | repository: swr.cn-north-1.myhuaweicloud.com     | linux/amd64    |
    | 华南-广州     | swr.cn-south-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com     | repository: swr.cn-south-1.myhuaweicloud.com     | linux/amd64    |
    | 华北-北京四   | swr.cn-north-4.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-4.myhuaweicloud.com     | repository: swr.cn-north-4.myhuaweicloud.com     | linux/arm64    |
    | 华东-上海一   | swr.cn-east-3.myhuaweicloud.com      | DOCKER_IMAGE_PREFIX=swr.cn-east-3.myhuaweicloud.com      | repository: swr.cn-east-3.myhuaweicloud.com      | linux/arm64    |
    | 西南-贵阳一   | swr.cn-southwest-2.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-1.myhuaweicloud.com | repository: swr.ap-southeast-1.myhuaweicloud.com | linux/loong64  |

!!! tip ""
    - 从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录。

!!! tip ""
    - 此处以 x86_64 系统为例，其它架构请下载对应安装包进行安装。
  
!!! tip ""
    ```sh
    cd /opt
    tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-amd64-{{ jumpserver.installer }}.tar.gz
    cd jumpserver-offline-installer-{{ jumpserver.tag }}-amd64-{{ jumpserver.installer }}
    ```
    ```sh
    # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
    cat config-example.txt
    ```
    ```vim
    # 以下设置如果为空系统会自动生成随机字符串填入
    ## 迁移请修改 SECRET_KEY 和 BOOTSTRAP_TOKEN 为原来的设置
    ## 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

    ## Docker 镜像配置
    # DOCKER_IMAGE_MIRROR=1

    ## 安装配置
    VOLUME_DIR=/opt/jumpserver
    SECRET_KEY=
    BOOTSTRAP_TOKEN=
    LOG_LEVEL=ERROR

    ##  MySQL 配置, 如果使用外置数据库, 请输入正确的 MySQL 信息
    DB_HOST=mysql
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=
    DB_NAME=jumpserver

    ##  Redis 配置, 如果使用外置数据库, 请输入正确的 Redis 信息
    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_PASSWORD=

    # JumpServer 容器使用的网段, 请勿与现有的网络冲突, 根据实际情况自行修改
    DOCKER_SUBNET=192.168.250.0/24

    ## IPV6 设置, 容器是否开启 ipv6 nat, USE_IPV6=1 表示开启, 为 0 的情况下 DOCKER_SUBNET_IPV6 定义不生效
    USE_IPV6=0
    DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

    ## 访问配置
    HTTP_PORT=80
    SSH_PORT=2222
    RDP_PORT=3389
    MAGNUS_PORTS=30000-30100

    ## HTTPS 配置, 参考 https://docs.jumpserver.org/zh/master/admin-guide/proxy/ 配置
    # HTTPS_PORT=443
    # SERVER_NAME=your_domain_name
    # SSL_CERTIFICATE=your_cert
    # SSL_CERTIFICATE_KEY=your_cert_key

    ## Nginx 文件上传大小
    CLIENT_MAX_BODY_SIZE=4096m

    ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
    USE_TASK=1

    # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=True 表示关闭浏览器即 session 过期
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True

    # Koko Lion XRDP 组件配置
    CORE_HOST=http://core:8080
    JUMPSERVER_ENABLE_FONT_SMOOTHING=True

    ## 终端使用宿主 HOSTNAME 标识
    SERVER_HOSTNAME=${HOSTNAME}

    # 额外的配置
    CURRENT_VERSION=
    ```
    ```sh
    # 安装
    ./jmsctl.sh install

    # 启动
    ./jmsctl.sh start
    ```
        
!!! info "安装完成后 JumpServer 配置文件路径为： /opt/jumpserver/config/config.txt。 此处以 x86_64 系统为例，其它架构请下载对应安装包。"

!!! tip ""
    ```sh
    cd /opt/jumpserver-installer-{{ jumpserver.tag }}-amd64-{{ jumpserver.installer }}

    # 启动
    ./jmsctl.sh start

    # 停止
    ./jmsctl.sh down

    # 卸载
    ./jmsctl.sh uninstall

    # 帮助
    ./jmsctl.sh -h
    ```

## 2 环境访问
!!! tip ""
    **安装成功后，通过浏览器访问如下信息登录 JumpServer：**

    ```sh
    地址: http://目标服务器IP地址:服务运行端口
    用户名: admin
    密码: admin #第一次登陆需要修改密码
    ```
![登陆页面](../../img/online_install_01.png)