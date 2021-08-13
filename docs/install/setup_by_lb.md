# 负载均衡

!!! info "环境说明"
    - 除 JumpServer 自身组件外，其他组件的高可用请参考对应的官方文档进行部署
    - 按照此方式部署后，后续只需要根据需要扩容 JumpServer 节点然后添加节点到 HAProxy 即可
    - 如果已经有 HLB 或者 SLB 可以跳过 HAProxy 部署，第三方 LB 要注意 session 和 websocket 问题
    - 如果已经有 云存储 (* S3/Ceph/Swift/OSS/Azure) 可以跳过 MinIO 部署，MySQL Redis 也一样
    - 生产环境中，应该使用 Ceph 等替代 NFS，或者部署高可用的 NFS 防止单点故障
    - [Redis 高可用快速部署可以参考此项目](https://github.com/wojiushixiaobai/redis-sentinel)

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 6.0  |
| MariaDB | >= 10.2 |    |       |         |

| Server Name   |        IP        |  Port       |     Use          |   Minimize Hardware    |   Standard Hardware    |
| ------------- | ---------------- | ----------- | ---------------- | ---------------------- | ---------------------- |
| NFS           |  192.168.100.11  |             | Core             | 2Core/8GB RAM/90G  HDD | 4Core/16GB RAM/1T  SSD |
| MySQL         |  192.168.100.11  | 3306        | Core             | 2Core/8GB RAM/90G  HDD | 4Core/16GB RAM/1T  SSD |  
| Redis         |  192.168.100.11  | 6379        | Core, Koko, Lion | 2Core/8GB RAM/90G  HDD | 4Core/16GB RAM/1T  SSD |
| HAProxy       |  192.168.100.100 | 80,443,2222 | All              | 2Core/4GB RAM/60G  HDD | 4Core/8GB  RAM/60G SSD |
| JumpServer 01 |  192.168.100.21  | 80,2222     | HAProxy          | 2Core/8GB RAM/60G  HDD | 4Core/8GB  RAM/90G SSD |
| JumpServer 02 |  192.168.100.22  | 80,2222     | HAProxy          | 2Core/8GB RAM/60G  HDD | 4Core/8GB  RAM/90G SSD |
| JumpServer 03 |  192.168.100.23  | 80,2222     | HAProxy          | 2Core/8GB RAM/60G  HDD | 4Core/8GB  RAM/90G SSD |
| JumpServer 04 |  192.168.100.24  | 80,2222     | HAProxy          | 2Core/8GB RAM/60G  HDD | 4Core/8GB  RAM/90G SSD |
| MinIO         |  192.168.100.41  | 9000,9001   | Core, KoKo, Lion | 2Core/4GB RAM/90G  HDD | 4Core/8GB  RAM/1T  SSD |

| Server Name   | Check Health                   | Example                                   |
| ------------- | ------------------------------ | ----------------------------------------- |
| Core          | http://core:8080/api/health/   | https://demo.jumpserver.org/api/health/   |
| KoKo          | http://koko:5000/koko/health/  | https://demo.jumpserver.org/koko/health/  |
| Lion          | http://lion:8081/lion/health/  | https://demo.jumpserver.org/lion/health/  |


## 部署 NFS 服务

    服务器: 192.168.100.11

!!! tip "安装依赖"
    ```sh
    yum -y install epel-release
    ```

!!! tip "安装 NFS"
    ```sh
    yum -y install nfs-utils rpcbind
    ```

!!! tip "启动 NFS"
    ```sh
    systemctl enable rpcbind nfs-server nfs-lock nfs-idmap
    systemctl start rpcbind nfs-server nfs-lock nfs-idmap
    ```

!!! tip "配置防火墙"
    ```sh
    firewall-cmd --add-service=nfs --permanent --zone=public
    firewall-cmd --add-service=mountd --permanent --zone=public
    firewall-cmd --add-service=rpc-bind --permanent --zone=public
    firewall-cmd --reload
    ```

!!! tip "配置 NFS"
    ```sh
    mkdir /data
    chmod 777 -R /data

    vi /etc/exports
    ```
    ```vim
    # 设置 NFS 访问权限, /data 是刚才创建的将被共享的目录, 192.168.100.* 表示整个 192.168.100.* 的资产都有括号里面的权限
    # 也可以写具体的授权对象 /data 192.168.100.30(rw,sync,no_root_squash) 192.168.100.31(rw,sync,no_root_squash)
    /data 192.168.100.*(rw,sync,all_squash,anonuid=0,anongid=0)
    ```
    ```sh
    exportfs -a
    ```

## 部署 MySQL 服务

    服务器: 192.168.100.11

!!! tip "设置 Repo"
    ```sh
    yum -y localinstall http://mirrors.ustc.edu.cn/mysql-repo/mysql57-community-release-el7.rpm
    ```

!!! tip "安装 MySQL"
    ```sh
    yum install -y mysql-community-server
    ```

!!! tip "配置 MySQL"
    ```sh
    if [ ! "$(cat /usr/bin/mysqld_pre_systemd | grep -v ^\# | grep initialize-insecure )" ]; then
        sed -i "s@--initialize @--initialize-insecure @g" /usr/bin/mysqld_pre_systemd
    fi
    ```

!!! tip "启动 MySQL"
    ```sh
    systemctl enable mysqld
    systemctl start mysqld
    ```

!!! tip "数据库授权"
    ```sh
    mysql -uroot
    ```
    ```mysql hl_lines="13 16 19 22 25 28"
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 2
    Server version: 5.7.32 MySQL Community Server (GPL)

    Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> create database jumpserver default charset 'utf8';
    Query OK, 1 row affected (0.00 sec)

    mysql> set global validate_password_policy=LOW;
    Query OK, 0 rows affected (0.00 sec)

    mysql> create user 'jumpserver'@'%' identified by 'KXOeyNgDeTdpeu9q';
    Query OK, 0 rows affected (0.00 sec)

    mysql> grant all on jumpserver.* to 'jumpserver'@'%';
    Query OK, 0 rows affected, 1 warning (0.00 sec)

    mysql> flush privileges;
    Query OK, 0 rows affected (0.00 sec)

    mysql> exit
    Bye
    ```

!!! tip "配置防火墙"
    ```sh
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="3306" accept"
    firewall-cmd --reload
    ```

## 部署 Redis 服务

    服务器: 192.168.100.11

!!! tip "下载源码"
    ```sh
    yum -y install epel-release wget make gcc-c++
    cd /opt
    wget https://download.redis.io/releases/redis-6.2.5.tar.gz
    ```

!!! tip "安装 Redis"
    ```sh
    tar -xf redis-6.2.5.tar.gz
    cd redis-6.2.5
    make
    make install PREFIX=/usr/local/redis
    ```

!!! tip "配置 Redis"
    ```sh
    cp redis.conf /etc/redis.conf
    sed -i "s/bind 127.0.0.1/bind 0.0.0.0/g" /etc/redis.conf
    sed -i "s/daemonize no/daemonize yes/g" /etc/redis.conf
    sed -i "s@pidfile /var/run/redis_6379.pid@pidfile /var/run/redis.pid@g" /etc/redis.conf
    sed -i "561i maxmemory-policy allkeys-lru" /etc/redis.conf
    sed -i "481i requirepass KXOeyNgDeTdpeu9q" /etc/redis.conf
    vi /etc/systemd/system/redis.service
    ```
    ```vim
    [Unit]
    Description=Redis persistent key-value database
    After=network.target
    After=network-online.target
    Wants=network-online.target

    [Service]
    Type=forking
    PIDFile=/var/run/redis.pid
    ExecStart=/usr/local/redis/bin/redis-server /etc/redis.conf
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s QUIT $MAINPID

    [Install]
    WantedBy=multi-user.target
    ```

!!! tip "启动 Redis"
    ```sh
    systemctl enable redis
    systemctl start redis
    ```

!!! tip "配置防火墙"
    ```sh
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="6379" accept"
    firewall-cmd --reload
    ```

## 部署 JumpServer 01

    服务器: 192.168.100.21

!!! tip "配置 NFS"
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.11
    ```
    ```sh
    # 将 Core 持久化目录挂载到 NFS, 默认 /opt/jumpserver/core/data, 请根据实际情况修改
    # JumpServer 持久化目录定义相关参数为 VOLUME_DIR, 在安装 JumpServer 过程中会提示
    mkdir /opt/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /opt/jumpserver/core/data
    ```

!!! warning ""
    ```sh
    # 可以写入到 /etc/fstab, 重启自动挂载. 注意: 设置后如果 nfs 损坏或者无法连接该服务器将无法启动
    echo "192.168.100.11:/data /opt/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```

!!! tip "修改配置文件"
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="6 11-15 18-23 26-29 32"
    # 修改下面选项, 其他保持默认, 请勿直接复制此处内容
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    # 安装配置
    ### 注意持久化目录 VOLUME_DIR, 如果上面 NFS 挂载其他目录, 此处也要修改. 如: NFS 挂载到/data/jumpserver/core/data, 则 DOCKER_DIR=/data/jumpserver
    VOLUME_DIR=/opt/jumpserver
    DOCKER_DIR=/var/lib/docker

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密, 请勿直接复制下面的字符串
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW    # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                                 # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR                                                  # 日志等级
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true                             # 关闭浏览器 session 过期

    # MySQL 配置
    USE_EXTERNAL_MYSQL=1                                             # 使用外置 MySQL
    DB_HOST=192.168.100.11
    DB_PORT=3306
    DB_USER=jumpserve
    DB_PASSWORD=KXOeyNgDeTdpeu9q
    DB_NAME=jumpserver

    # Redis 配置
    USE_EXTERNAL_REDIS=1                                             # 使用外置 Redis
    REDIS_HOST=192.168.100.11
    REDIS_PORT=6379
    REDIS_PASSWORD=KXOeyNgDeTdpeu9q

    # KoKo Lion 配置
    SHARE_ROOM_TYPE=redis                                            # KoKo Lion 使用 redis 共享
    ```
    ```sh
    ./jmsctl.sh install
    ```
    ```nginx hl_lines="31 48 57 61-66 70-73 77"

           ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
           ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
      ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
      ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
       ╚════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

    								                                     Version:  {{ jumpserver.version }}


    1. 检查配置文件
    配置文件位置: /opt/jumpserver/config
    /opt/jumpserver/config/config.txt  [ √ ]
    /opt/jumpserver/config/nginx/lb_rdp_server.conf  [ √ ]
    /opt/jumpserver/config/nginx/lb_ssh_server.conf  [ √ ]
    /opt/jumpserver/config/nginx/cert/server.crt  [ √ ]
    /opt/jumpserver/config/nginx/cert/server.key  [ √ ]
    完成

    2. 备份配置文件
    备份至 /opt/jumpserver/config/backup/config.txt.2021-07-15_22-26-13
    完成

    >>> 安装配置 Docker
    1. 安装 Docker
    开始下载 Docker 程序 ...
    开始下载 Docker Compose 程序 ...
    完成

    2. 配置 Docker
    是否需要自定义 docker 存储目录, 默认将使用目录 /var/lib/docker? (y/n)  (默认为 n): n
    完成

    3. 启动 Docker
    Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /etc/systemd/system/docker.service.
    完成

    >>> 加载 Docker 镜像
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/web:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/lion:{{ jumpserver.version }} 	    [ OK ]

    >>> 安装配置 JumpServer
    1. 配置网络
    是否需要支持 IPv6? (y/n)  (默认为 n): n
    完成

    2. 配置加密密钥
    SECRETE_KEY:     YTE2YTVkMTMtMGE3MS00YzI5LWFlOWEtMTc2OWJlMmIyMDE2
    BOOTSTRAP_TOKEN: YTE2YTVkMTMtMGE3
    完成

    3. 配置持久化目录
    是否需要自定义持久化存储, 默认将使用目录 /opt/jumpserver? (y/n)  (默认为 n): n
    完成

    4. 配置 MySQL
    是否使用外部 MySQL? (y/n)  (默认为 n): y
    请输入 MySQL 的主机地址 (无默认值): 192.168.100.11
    请输入 MySQL 的端口 (默认为3306): 3306
    请输入 MySQL 的数据库(事先做好授权) (默认为jumpserver): jumpserver
    请输入 MySQL 的用户名 (无默认值): jumpserver
    请输入 MySQL 的密码 (无默认值): KXOeyNgDeTdpeu9q
    完成

    5. 配置 Redis
    是否使用外部 Redis? (y/n)  (默认为 n): y
    请输入 Redis 的主机地址 (无默认值): 192.168.100.11
    请输入 Redis 的端口 (默认为6379): 6379
    请输入 Redis 的密码 (无默认值): KXOeyNgDeTdpeu9q
    完成

    6. 配置对外端口
    是否需要配置 JumpServer 对外访问端口? (y/n)  (默认为 n): n
    完成

    7. 初始化数据库
    Creating network "jms_net" with driver "bridge"
    Creating jms_redis ... done
    2021-07-15 22:39:52 Collect static files
    2021-07-15 22:39:52 Collect static files done
    2021-07-15 22:39:52 Check database structure change ...
    2021-07-15 22:39:52 Migrate model change to database ...

    475 static files copied to '/opt/jumpserver/data/static'.
    Operations to perform:
      Apply all migrations: acls, admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, notifications, ops, orgs, perms, sessions, settings, terminal, tickets, users
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0001_initial... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      ...
      Applying sessions.0001_initial... OK
      Applying terminal.0032_auto_20210302_1853... OK
      Applying terminal.0033_auto_20210324_1008... OK
      Applying terminal.0034_auto_20210406_1434... OK
      Applying terminal.0035_auto_20210517_1448... OK
      Applying terminal.0036_auto_20210604_1124... OK
      Applying terminal.0037_auto_20210623_1748... OK
      Applying tickets.0008_auto_20210311_1113... OK
      Applying tickets.0009_auto_20210426_1720... OK

    >>> 安装完成了
    1. 可以使用如下命令启动, 然后访问
    cd /root/jumpserver-installer-{{ jumpserver.version }}
    ./jmsctl.sh start

    2. 其它一些管理命令
    ./jmsctl.sh stop
    ./jmsctl.sh restart
    ./jmsctl.sh backup
    ./jmsctl.sh upgrade
    更多还有一些命令, 你可以 ./jmsctl.sh --help 来了解

    3. Web 访问
    http://192.168.100.212:80
    默认用户: admin  默认密码: admin

    4. SSH/SFTP 访问
    ssh -p2222 admin@192.168.100.212
    sftp -P2222 admin@192.168.100.212

    5. 更多信息
    我们的官网: https://www.jumpserver.org/
    我们的文档: https://docs.jumpserver.org/
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_lion      ... done
    Creating jms_koko      ... done
    Creating jms_web       ... done
    ```


## 部署 JumpServer 02

    服务器: 192.168.100.22

!!! tip "配置 NFS"
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.11
    ```
    ```sh
    # 将 Core 持久化目录挂载到 NFS, 默认 /opt/jumpserver/core/data, 请根据实际情况修改
    # JumpServer 持久化目录定义相关参数为 VOLUME_DIR, 在安装 JumpServer 过程中会提示
    mkdir /opt/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /opt/jumpserver/core/data
    ```

!!! warning ""
    ```sh
    # 可以写入到 /etc/fstab, 重启自动挂载. 注意: 设置后如果 nfs 损坏或者无法连接该服务器将无法启动
    echo "192.168.100.11:/data /opt/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```

!!! tip "修改配置文件"
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="6 11-15 18-23 26-29 32"
    # 修改下面选项, 其他保持默认, 请勿直接复制此处内容
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    # 安装配置
    ### 注意持久化目录 VOLUME_DIR, 如果上面 NFS 挂载其他目录, 此处也要修改. 如: NFS 挂载到/data/jumpserver/core/data, 则 DOCKER_DIR=/data/jumpserver
    VOLUME_DIR=/opt/jumpserver
    DOCKER_DIR=/var/lib/docker

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密, 请勿直接复制下面的字符串
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # MySQL 配置
    USE_EXTERNAL_MYSQL=1
    DB_HOST=192.168.100.11
    DB_PORT=3306
    DB_USER=jumpserver
    DB_PASSWORD=KXOeyNgDeTdpeu9q
    DB_NAME=jumpserver

    # Redis 配置
    USE_EXTERNAL_REDIS=1
    REDIS_HOST=192.168.100.11
    REDIS_PORT=6379
    REDIS_PASSWORD=KXOeyNgDeTdpeu9q

    # KoKo Lion 配置
    SHARE_ROOM_TYPE=redis
    ```
    ```sh
    ./jmsctl.sh install
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_lion      ... done
    Creating jms_koko      ... done
    Creating jms_web       ... done
    ```


## 部署 JumpServer 03

    服务器: 192.168.100.23

!!! tip "配置 NFS"
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.11
    ```
    ```sh
    # 将 Core 持久化目录挂载到 NFS, 默认 /opt/jumpserver/core/data, 请根据实际情况修改
    # JumpServer 持久化目录定义相关参数为 VOLUME_DIR, 在安装 JumpServer 过程中会提示
    mkdir /opt/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /opt/jumpserver/core/data
    ```

!!! warning ""
    ```sh
    # 可以写入到 /etc/fstab, 重启自动挂载. 注意: 设置后如果 nfs 损坏或者无法连接该服务器将无法启动
    echo "192.168.100.11:/data /opt/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```

!!! tip "修改配置文件"
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="6 11-15 18-23 26-29 32"
    # 修改下面选项, 其他保持默认, 请勿直接复制此处内容
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    # 安装配置
    ### 注意持久化目录 VOLUME_DIR, 如果上面 NFS 挂载其他目录, 此处也要修改. 如: NFS 挂载到/data/jumpserver/core/data, 则 DOCKER_DIR=/data/jumpserver
    VOLUME_DIR=/opt/jumpserver
    DOCKER_DIR=/var/lib/docker

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密, 请勿直接复制下面的字符串
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # MySQL 配置
    USE_EXTERNAL_MYSQL=1
    DB_HOST=192.168.100.11
    DB_PORT=3306
    DB_USER=jumpserver
    DB_PASSWORD=KXOeyNgDeTdpeu9q
    DB_NAME=jumpserver

    # Redis 配置
    USE_EXTERNAL_REDIS=1
    REDIS_HOST=192.168.100.11
    REDIS_PORT=6379
    REDIS_PASSWORD=KXOeyNgDeTdpeu9q

    # KoKo Lion 配置
    SHARE_ROOM_TYPE=redis
    ```
    ```sh
    ./jmsctl.sh install
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_core      ... done
    Creating jms_lion      ... done
    Creating jms_koko      ... done
    Creating jms_celery    ... done
    Creating jms_web       ... done
    ```


## 部署 JumpServer 04

    服务器: 192.168.100.24

!!! tip "配置 NFS"
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.11
    ```
    ```sh
    # 将 Core 持久化目录挂载到 NFS, 默认 /opt/jumpserver/core/data, 请根据实际情况修改
    # JumpServer 持久化目录定义相关参数为 VOLUME_DIR, 在安装 JumpServer 过程中会提示
    mkdir /opt/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /opt/jumpserver/core/data
    ```

!!! warning ""
    ```sh
    # 可以写入到 /etc/fstab, 重启自动挂载. 注意: 设置后如果 nfs 损坏或者无法连接该服务器将无法启动
    echo "192.168.100.11:/data /opt/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```

!!! tip "修改配置文件"
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="6 11-15 18-23 26-29 32"
    # 修改下面选项, 其他保持默认, 请勿直接复制此处内容
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    # 安装配置
    ### 注意持久化目录 VOLUME_DIR, 如果上面 NFS 挂载其他目录, 此处也要修改. 如: NFS 挂载到/data/jumpserver/core/data, 则 DOCKER_DIR=/data/jumpserver
    VOLUME_DIR=/opt/jumpserver
    DOCKER_DIR=/var/lib/docker

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密, 请勿直接复制下面的字符串
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # MySQL 配置
    USE_EXTERNAL_MYSQL=1
    DB_HOST=192.168.100.11
    DB_PORT=3306
    DB_USER=jumpserver
    DB_PASSWORD=KXOeyNgDeTdpeu9q
    DB_NAME=jumpserver

    # Redis 配置
    USE_EXTERNAL_REDIS=1
    REDIS_HOST=192.168.100.11
    REDIS_PORT=6379
    REDIS_PASSWORD=KXOeyNgDeTdpeu9q

    # KoKo Lion 配置
    SHARE_ROOM_TYPE=redis
    ```
    ```sh
    ./jmsctl.sh install
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_lion      ... done
    Creating jms_koko      ... done
    Creating jms_web       ... done
    ```


## 部署 HAProxy 服务

    服务器: 192.168.100.100

!!! tip "安装依赖"
    ```sh
    yum -y install epel-release
    ```

!!! tip "安装 HAProxy"
    ```sh
    yum install -y haproxy
    ```

!!! tip "配置 HAProxy"
    ```sh
    vi /etc/haproxy/haproxy.cfg
    ```
    ```nginx
    global
        # to have these messages end up in /var/log/haproxy.log you will
        # need to:
        #
        # 1) configure syslog to accept network log events.  This is done
        #    by adding the '-r' option to the SYSLOGD_OPTIONS in
        #    /etc/sysconfig/syslog
        #
        # 2) configure local2 events to go to the /var/log/haproxy.log
        #   file. A line like the following can be added to
        #   /etc/sysconfig/syslog
        #
        #    local2.*                       /var/log/haproxy.log
        #
        log         127.0.0.1 local2

        chroot      /var/lib/haproxy
        pidfile     /var/run/haproxy.pid
        maxconn     4000
        user        haproxy
        group       haproxy
        daemon

        # turn on stats unix socket
        stats socket /var/lib/haproxy/stats

    #---------------------------------------------------------------------
    # common defaults that all the 'listen' and 'backend' sections will
    # use if not designated in their block
    #---------------------------------------------------------------------
    defaults
        log                     global
        option                  dontlognull
        option                  redispatch
        retries                 3
        timeout http-request    10s
        timeout queue           1m
        timeout connect         10s
        timeout client          1m
        timeout server          1m
        timeout http-keep-alive 10s
        timeout check           10s
        maxconn                 3000

    listen stats
        bind *:8080
        mode http
        stats enable
        stats uri /haproxy                      # 监控页面, 请自行修改. 访问地址为 http://192.168.100.100:8080/haproxy
        stats refresh 5s
        stats realm haproxy-status
        stats auth admin:KXOeyNgDeTdpeu9q       # 账户密码, 请自行修改. 访问 http://192.168.100.100:8080/haproxy 会要求输入

    #---------------------------------------------------------------------
    # check  检活参数说明
    # inter  间隔时间, 单位: 毫秒
    # rise   连续成功的次数, 单位: 次
    # fall   连续失败的次数, 单位: 次
    # 例: inter 2s rise 2 fall 3
    # 表示 2 秒检查一次状态, 连续成功 2 次服务正常, 连续失败 3 次服务异常
    #
    # server 服务参数说明
    # server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01
    # 第一个 192.168.100.21 做为页面展示的标识, 可以修改为其他任意字符串
    # 第二个 192.168.100.21:80 是实际的后端服务端口
    # weight 为权重, 多节点时安装权重进行负载均衡
    # cookie 用户侧的 cookie 会包含此标识, 便于区分当前访问的后端节点
    # 例: server db01 192.168.100.21:3306 weight 1 cookie db_01
    #---------------------------------------------------------------------

    listen jms-web
        bind *:80                               # 监听 80 端口
        mode http

        # redirect scheme https if !{ ssl_fc }  # 重定向到 https
        # bind *:443 ssl crt /opt/ssl.pem       # https 设置

        option httpclose
        option forwardfor
        option httpchk GET /api/health/         # Core 检活接口

        cookie SERVERID insert indirect
        hash-type consistent
        fullconn 500
        balance leastconn
        server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01 check inter 2s rise 2 fall 3  # JumpServer 服务器
        server 192.168.100.22 192.168.100.22:80 weight 1 cookie web02 check inter 2s rise 2 fall 3
        server 192.168.100.23 192.168.100.23:80 weight 1 cookie web03 check inter 2s rise 2 fall 3
        server 192.168.100.23 192.168.100.24:80 weight 1 cookie web03 check inter 2s rise 2 fall 3

    listen jms-ssh
        bind *:2222
        mode tcp

        option tcp-check

        fullconn 500
        balance leastconn
        server 192.168.100.21 192.168.100.21:2222 weight 1 check inter 2s rise 2 fall 3 send-proxy
        server 192.168.100.22 192.168.100.22:2222 weight 1 check inter 2s rise 2 fall 3 send-proxy
        server 192.168.100.23 192.168.100.23:2222 weight 1 check inter 2s rise 2 fall 3 send-proxy
        server 192.168.100.24 192.168.100.23:2222 weight 1 check inter 2s rise 2 fall 3 send-proxy

    listen jms-koko
        mode http

        option httpclose
        option forwardfor
        option httpchk GET /koko/health/ HTTP/1.1\r\nHost:\ 192.168.100.100  # KoKo 检活接口, host 填写 HAProxy 的 ip 地址

        cookie SERVERID insert indirect
        hash-type consistent
        fullconn 500
        balance leastconn
        server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01 check inter 2s rise 2 fall 3
        server 192.168.100.22 192.168.100.22:80 weight 1 cookie web02 check inter 2s rise 2 fall 3
        server 192.168.100.23 192.168.100.23:80 weight 1 cookie web03 check inter 2s rise 2 fall 3
        server 192.168.100.24 192.168.100.23:80 weight 1 cookie web03 check inter 2s rise 2 fall 3

    listen jms-lion
        mode http

        option httpclose
        option forwardfor
        option httpchk GET /lion/health/ HTTP/1.1\r\nHost:\ 192.168.100.100  # Lion 检活接口, host 填写 HAProxy 的 ip 地址

        cookie SERVERID insert indirect
        hash-type consistent
        fullconn 500
        balance leastconn
        server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01 check inter 2s rise 2 fall 3
        server 192.168.100.22 192.168.100.22:80 weight 1 cookie web02 check inter 2s rise 2 fall 3
        server 192.168.100.23 192.168.100.23:80 weight 1 cookie web03 check inter 2s rise 2 fall 3
        server 192.168.100.24 192.168.100.23:80 weight 1 cookie web03 check inter 2s rise 2 fall 3
    ```

!!! tip "配置 Selinux"
    ```sh
    setsebool -P haproxy_connect_any 1
    ```

!!! tip "启动 HAProxy"
    ```sh
    systemctl enable haproxy
    systemctl start haproxy
    ```

!!! tip "配置防火墙"
    ```sh
    firewall-cmd --permanent --zone=public --add-port=80/tcp
    firewall-cmd --permanent --zone=public --add-port=443/tcp
    firewall-cmd --permanent --zone=public --add-port=2222/tcp
    firewall-cmd --reload
    ```

## 部署 MinIO 服务

    服务器: 192.168.100.41

!!! tip "安装 Docker"
    ```sh
    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
    yum makecache fast
    yum -y install docker-ce
    ```

!!! tip "配置 Docker"
    ```sh
    mkdir /etc/docker/
    vi /etc/docker/daemon.json
    ```
    ```json
    {
      "live-restore": true,
      "registry-mirrors": ["https://hub-mirror.c.163.com", "https://bmtrgdvx.mirror.aliyuncs.com", "http://f1361db2.m.daocloud.io"],
      "log-driver": "json-file",
      "log-opts": {"max-file": "3", "max-size": "10m"}
    }
    ```

!!! tip "启动 Docker"
    ```sh
    systemctl enable docker
    systemctl start docker
    ```

!!! tip "下载 MinIO 镜像"
    ```sh
    docker pull minio/minio:latest
    ```
    ```vim
    latest: Pulling from minio/minio
    a591faa84ab0: Pull complete
    76b9354adec6: Pull complete
    f9d8746550a4: Pull complete
    890b1dd95baa: Pull complete
    3a8518c890dc: Pull complete
    8053f0501aed: Pull complete
    506c41cb8532: Pull complete
    Digest: sha256:e7a725edb521dd2af07879dad88ee1dfebd359e57ad8d98104359ccfbdb92024
    Status: Downloaded newer image for minio/minio:latest
    docker.io/minio/minio:latest
    ```

!!! tip "持久化数据目录"
    ```sh
    mkdir -p /opt/jumpserver/minio/data /opt/jumpserver/minio/config
    ```

!!! tip "启动 MinIO"
    ```vim
    ## 请自行修改账号密码并牢记，丢失后可以删掉容器后重新用新密码创建，数据不会丢失
    # 9000                                  # api     访问端口
    # 9001                                  # console 访问端口
    # MINIO_ROOT_USER=minio                 # minio 账号
    # MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q  # minio 密码
    ```
    ```sh
    docker run --name jms_minio -d -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q -v /opt/jumpserver/minio/data:/data -v /opt/jumpserver/minio/config:/root/.minio --restart=always minio/minio:latest server /data --console-address ":9001"
    ```

!!! tip "设置 MinIO"
    - 访问 http://192.168.100.41:9000，输入刚才设置的 MinIO 账号密码登录
    - 点击左侧菜单的 Buckets，选择 Create Bucket 创建桶，Bucket Name 输入 jumpserver，然后点击 Save 保存

!!! tip "设置 JumpServer"
    - 访问 JumpServer Web 页面并使用管理员账号进行登录
    - 点击左侧菜单栏的 [终端管理]，在页面的上方选择 [存储配置]，在 [录像存储] 下方选择 [创建] 选择 [Ceph]
    - 根据下方的说明进行填写，保存后在 [终端管理] 页面对所有组件进行 [更新]，录像存储选择 [jms-mino]，提交

| 选项            | 参考值                      | 说明                |
| :-------------  | :------------------------- | :------------------ |
| 名称 (Name)     | jms-minio                  | 标识, 不可重复       |
| 类型 (Type)     | Ceph                       | 固定, 不可更改       |
| 桶名称 (Bucket) | jumpserver                 | Bucket Name         |
| Access key      | minio                      | MINIO_ROOT_USER     |
| Secret key      | KXOeyNgDeTdpeu9q           | MINIO_ROOT_PASSWORD |
| 端点 (Endpoint) | http://192.168.100.41:9000 | minio 服务访问地址   |
| 默认存储        |                            | 新组件将自动使用该存储 |

## 升级 注意事项

!!! warning "更新前请一定要做好备份工作"
    - 升级前请关闭所有 JumpServer 节点
    - 在任意一个 JumpServer 节点按照升级文档完成升级操作
    - 仔细检查该节点升级过程确保无异常
    - 然后按照升级文档对其他 JumpServer 节点升级即可

    ```sh
    cd /opt
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```
    ```sh
    # 额外节点可以设置 SKIP_BACKUP_DB=1 跳过数据库备份, 第一个升级节点不要跳过备份
    export SKIP_BACKUP_DB=1
    ./jmsctl.sh upgrade
    ```
