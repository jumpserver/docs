# 极速安装

!!! info "说明"
    全新安装的 Centos7 (7.x)  
    需要连接 互联网  
    使用 root 用户执行  

!!! warning ""
    资产数量不多，或者测试体验的用户请使用本脚本快速部署  
    如果资产规模较大，请参考 [分布式部署](setup_by_prod.md) 文档  

    注意: 对系统进行任何修改均可能导致安装失败，推荐在安装完成后再进行调优

- [安装视频](https://www.bilibili.com/video/bv19a4y1i7i9)

!!! tip "一键安装 JumpServer"
    ```sh
    curl -sSL https://github.com/jumpserver/jumpserver/releases/download/v2.2.1/quick_start.sh | sh
    ```

## 下载

!!! tip "下载文件"
    ```sh
    cd /opt
    yum -y install wget git
    git clone --depth=1 https://github.com/jumpserver/setuptools.git
    cd setuptools
    cp config_example.conf config.conf
    vi config.conf
    ```

??? info "配置文件说明, 注意不能使用纯数字字符串, 如果不知道用途请勿修改"
    ```vim
    # 以下设置默认情况下不需要修改

    # 需要安装的版本
    Version=2.0.0

    # Jms 加密配置
    SECRET_KEY=
    BOOTSTRAP_TOKEN=

    # 数据库 配置, 如果 数据库 安装在其他的服务器, 请修改下面设置
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_USER=jumpserver
    DB_PASSWORD=
    DB_NAME=jumpserver

    # Redis 配置, 如果 Redis 安装在其他的服务器, 请修改下面设置
    REDIS_HOST=127.0.0.1
    REDIS_PORT=6379
    REDIS_PASSWORD=

    # 服务端口设置, 如果云服务器未备案请修改 http_port 端口为其他端口
    http_port=80
    ssh_port=2222

    # 服务安装目录
    install_dir=/opt

    Server_IP=`ip addr | grep 'state UP' -A2 | grep inet | egrep -v '(127.0.0.1|inet6|docker)' | awk '{print $2}' | tr -d "addr:" | head -n 1 | cut -d / -f1`
    Docker_IP=`ip addr | grep docker.* | grep inet | awk '{print $2}' | head -n 1`
    ```

## 安装

!!! tip "Install"
    ```sh
    ./jmsctl.sh install
    ```

## 帮助

!!! tip "Help"
    ```sh
    ./jmsctl.sh -h
    ```

## 升级

!!! tip "Upgrade"
    ```sh
    cd /opt/setuptools
    git pull
    ./jmsctl.sh upgrade
    ```

后续的使用请参考 [安全建议](install_security.md) [快速入门](../../admin-guide/quick_start/)  
