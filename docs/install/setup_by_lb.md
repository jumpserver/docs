# 负载均衡

!!! info "环境说明"
    - 除 JumpServer 自身组件外, 其他组件的高可用请参考对应的官方文档进行部署
    - 按照此方式部署后, 后续只需要根据需要扩容 core web 节点然后添加节点到 nginx 即可
    - 如果已经有 HLB 或者 SLB 可以跳过 nginx 部署, 第三方 LB 要注意 session 和 websocket 问题
    - 如果已经有 云存储(* S3/Ceph/Swift/OSS/Azure) 可以跳过 MinIO 部署, MySQL Redis 也一样

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 5.0  |
| MariaDB | >= 10.2 |    |       |         |

| Server Name   |        IP        |  Port  |     Use          |   Minimize Hardware   |   Standard Hardware    |
| ------------- | ---------------- | ------ | ---------------- | --------------------- | ---------------------- |
| MySQL         |  192.168.100.11  |  3306  |  Core            | 2Core/4GB RAM/1T  HDD | 4Core/16GB RAM/1T  SSD |  
| Redis         |  192.168.100.11  |  6379  |  Core, Koko      | 2Core/4GB RAM/60G HDD | 2Core/8GB  RAM/60G SSD |
| Nginx         |  192.168.100.100 | 80,443 |  All             | 2Core/4GB RAM/60G HDD | 4Core/8GB  RAM/60G SSD |
| Core Web 01   |  192.168.100.21  |  8080  |  Nginx           | 2Core/8GB RAM/60G HDD | 4Core/8GB  RAM/90G SSD |
| Core Web 02   |  192.168.100.22  |  8080  |  Nginx           | 2Core/8GB RAM/60G HDD | 4Core/8GB  RAM/90G SSD |
| Core Task     |  192.168.100.31  |  8080  |  Nginx           | 4Core/8GB RAM/60G HDD | 4Core/16GB RAM/90G SSD |
| MinIO         |  192.168.100.41  |  9000  |  KoKo, Guacamole | 2Core/4GB RAM/1T  HDD | 4Core/8GB  RAM/1T  SSD |

!!! warning "Core Task 目前仅支持单节点运行, 后续会优化"

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
    ```mysql hl_lines="13 16 19 22"
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 2
    Server version: 5.7.32 MySQL Community Server (GPL)

    Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> create database jumpserver default charset 'utf8' collate 'utf8_bin';
    Query OK, 1 row affected (0.00 sec)

    mysql> set global validate_password_policy=LOW;
    Query OK, 0 rows affected (0.00 sec)

    mysql> grant all on jumpserver.* to 'jumpserver'@'192.168.100.%' identified by 'weakPassword';
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

!!! tip "设置 Repo"
    ```sh
    yum -y install epel-release https://repo.ius.io/ius-release-el7.rpm
    ```

!!! tip "安装 Redis"
    ```sh
    yum install -y redis5
    ```

!!! tip "配置 Redis"
    ```sh
    sed -i "s/bind 127.0.0.1/bind 0.0.0.0/g" /etc/redis.conf
    sed -i "561i maxmemory-policy allkeys-lru" /etc/redis.conf
    sed -i "481i requirepass weakPassword" /etc/redis.conf
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

## 部署 Core Web 01

    服务器: 192.168.100.21

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
    ```vim hl_lines="5 9-10 16"
    # 修改下面选项, 其他保持默认
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    ## Task 配置
    USE_TASK=0                                                     # 不启动 jms_celery

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW  # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                               # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # KoKo 配置
    SHARE_ROOM_TYPE=redis                                          # KoKo 使用 redis 共享
    ```
    ```sh
    ./jmsctl.sh install
    ```
    ```nginx hl_lines="26 40 44-49 53-56 69 73"

           ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
           ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
      ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
      ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
       ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

    								                             Version:  {{ jumpserver.version }}


    >>> 一、配置JumpServer
    1. 检查配置文件
    各组件使用环境变量式配置文件，而不是 yaml 格式, 配置名称与之前保持一致
    配置文件位置: /opt/jumpserver/config/config.txt
    完成

    2. 配置 Nginx 证书
    证书位置在: /opt/jumpserver/config/nginx/cert
    完成

    3. 备份配置文件
    备份至 /opt/jumpserver/config/backup/config.txt.2020-12-18_10-18-00
    完成

    4. 配置网络
    需要支持 IPv6 吗? (y/n)  (默认为n): n
    完成

    5. 自动生成加密密钥
    完成

    6. 配置持久化目录
    修改日志录像等持久化的目录，可以找个最大的磁盘，并创建目录，如 /opt/jumpserver
    注意: 安装完后不能再更改, 否则数据库可能丢失

    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.0G   49G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    设置持久化卷存储目录 (默认为/opt/jumpserver): /opt/jumpserver
    完成

    7. 配置MySQL
    是否使用外部mysql (y/n)  (默认为n): y
    请输入mysql的主机地址 (无默认值): 192.168.100.11
    请输入mysql的端口 (默认为3306): 3306
    请输入mysql的数据库(事先做好授权) (默认为jumpserver): jumpserver
    请输入mysql的用户名 (无默认值): jumpserver
    请输入mysql的密码 (无默认值): weakPassword
    完成

    8. 配置Redis
    是否使用外部redis  (y/n)  (默认为n): y
    请输入redis的主机地址 (无默认值): 192.168.100.11
    请输入redis的端口 (默认为6379): 6379
    请输入redis的密码 (无默认值): weakPassword
    完成

    >>> 二、安装配置Docker
    1. 安装Docker
    完成

    2. 配置Docker
    修改Docker镜像容器的默认存储目录，可以找个最大的磁盘, 并创建目录，如 /opt/docker
    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.2G   48G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    Docker存储目录 (默认为/opt/docker): /var/lib/docker
    完成

    3. 启动Docker
    Docker 版本发生改变 或 docker配置文件发生变化，是否要重启 (y/n)  (默认为y): y
    完成

    >>> 三、加载镜像
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

    >>> 四、安装完成了
    1. 可以使用如下命令启动, 然后访问
    ./jmsctl.sh start

    2. 其它一些管理命令
    ./jmsctl.sh stop
    ./jmsctl.sh restart
    ./jmsctl.sh backup
    ./jmsctl.sh upgrade
    更多还有一些命令，你可以 ./jmsctl.sh --help来了解

    3. 访问 Web 后台页面
    http://192.168.100.236:8080
    https://192.168.100.236:8443

    4. ssh/sftp 访问
    ssh admin@192.168.100.236 -p2222
    sftp -P2222 admin@192.168.100.236

    5. 更多信息
    我们的文档: https://docs.jumpserver.org/
    我们的官网: https://www.jumpserver.org/
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_mysql     ... done
    Creating jms_redis     ... done
    Creating jms_core      ... done
    Creating jms_luna      ... done
    Creating jms_lina      ... done
    Creating jms_guacamole ... done
    Creating jms_koko      ... done
    Creating jms_nginx     ... done
    ```    

## 部署 Core Web 02

    服务器: 192.168.100.22

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
    ```vim hl_lines="5 9-10 16"
    # 修改下面选项, 其他保持默认
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    ## Task 配置
    USE_TASK=0                                                     # 不启动 jms_celery

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW  # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                               # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # KoKo 配置
    SHARE_ROOM_TYPE=redis                                          # KoKo 使用 redis 共享
    ```
    ```sh
    ./jmsctl.sh install
    ```
    ```nginx hl_lines="26 40 44-49 53-56 69 73"

           ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
           ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
      ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
      ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
       ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

    								                             Version:  {{ jumpserver.version }}


    >>> 一、配置JumpServer
    1. 检查配置文件
    各组件使用环境变量式配置文件，而不是 yaml 格式, 配置名称与之前保持一致
    配置文件位置: /opt/jumpserver/config/config.txt
    完成

    2. 配置 Nginx 证书
    证书位置在: /opt/jumpserver/config/nginx/cert
    完成

    3. 备份配置文件
    备份至 /opt/jumpserver/config/backup/config.txt.2020-12-18_10-18-00
    完成

    4. 配置网络
    需要支持 IPv6 吗? (y/n)  (默认为n): n
    完成

    5. 自动生成加密密钥
    完成

    6. 配置持久化目录
    修改日志录像等持久化的目录，可以找个最大的磁盘，并创建目录，如 /opt/jumpserver
    注意: 安装完后不能再更改, 否则数据库可能丢失

    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.0G   49G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    设置持久化卷存储目录 (默认为/opt/jumpserver): /opt/jumpserver
    完成

    7. 配置MySQL
    是否使用外部mysql (y/n)  (默认为n): y
    请输入mysql的主机地址 (无默认值): 192.168.100.11
    请输入mysql的端口 (默认为3306): 3306
    请输入mysql的数据库(事先做好授权) (默认为jumpserver): jumpserver
    请输入mysql的用户名 (无默认值): jumpserver
    请输入mysql的密码 (无默认值): weakPassword
    完成

    8. 配置Redis
    是否使用外部redis  (y/n)  (默认为n): y
    请输入redis的主机地址 (无默认值): 192.168.100.11
    请输入redis的端口 (默认为6379): 6379
    请输入redis的密码 (无默认值): weakPassword
    完成

    >>> 二、安装配置Docker
    1. 安装Docker
    完成

    2. 配置Docker
    修改Docker镜像容器的默认存储目录，可以找个最大的磁盘, 并创建目录，如 /opt/docker
    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.2G   48G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    Docker存储目录 (默认为/opt/docker): /var/lib/docker
    完成

    3. 启动Docker
    Docker 版本发生改变 或 docker配置文件发生变化，是否要重启 (y/n)  (默认为y): y
    完成

    >>> 三、加载镜像
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

    >>> 四、安装完成了
    1. 可以使用如下命令启动, 然后访问
    ./jmsctl.sh start

    2. 其它一些管理命令
    ./jmsctl.sh stop
    ./jmsctl.sh restart
    ./jmsctl.sh backup
    ./jmsctl.sh upgrade
    更多还有一些命令，你可以 ./jmsctl.sh --help来了解

    3. 访问 Web 后台页面
    http://192.168.100.236:8080
    https://192.168.100.236:8443

    4. ssh/sftp 访问
    ssh admin@192.168.100.236 -p2222
    sftp -P2222 admin@192.168.100.236

    5. 更多信息
    我们的文档: https://docs.jumpserver.org/
    我们的官网: https://www.jumpserver.org/
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_mysql     ... done
    Creating jms_redis     ... done
    Creating jms_core      ... done
    Creating jms_luna      ... done
    Creating jms_lina      ... done
    Creating jms_guacamole ... done
    Creating jms_koko      ... done
    Creating jms_nginx     ... done
    ```    

## 部署 Core Task

    服务器: 192.168.100.31

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
    ```vim hl_lines="5 9-10 16"
    # 修改下面选项, 其他保持默认
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    ## Task 配置
    USE_TASK=1                                                     # 启动 jms_celery

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW  # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                               # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # KoKo 配置
    SHARE_ROOM_TYPE=redis                                          # KoKo 使用 redis 共享
    ```
    ```sh
    ./jmsctl.sh install
    ```
    ```nginx hl_lines="26 40 44-49 53-56 69 73"

           ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
           ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
      ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
      ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
       ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

    								                             Version:  {{ jumpserver.version }}


    >>> 一、配置JumpServer
    1. 检查配置文件
    各组件使用环境变量式配置文件，而不是 yaml 格式, 配置名称与之前保持一致
    配置文件位置: /opt/jumpserver/config/config.txt
    完成

    2. 配置 Nginx 证书
    证书位置在: /opt/jumpserver/config/nginx/cert
    完成

    3. 备份配置文件
    备份至 /opt/jumpserver/config/backup/config.txt.2020-12-18_10-18-00
    完成

    4. 配置网络
    需要支持 IPv6 吗? (y/n)  (默认为n): n
    完成

    5. 自动生成加密密钥
    完成

    6. 配置持久化目录
    修改日志录像等持久化的目录，可以找个最大的磁盘，并创建目录，如 /opt/jumpserver
    注意: 安装完后不能再更改, 否则数据库可能丢失

    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.0G   49G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    设置持久化卷存储目录 (默认为/opt/jumpserver): /opt/jumpserver
    完成

    7. 配置MySQL
    是否使用外部mysql (y/n)  (默认为n): y
    请输入mysql的主机地址 (无默认值): 192.168.100.11
    请输入mysql的端口 (默认为3306): 3306
    请输入mysql的数据库(事先做好授权) (默认为jumpserver): jumpserver
    请输入mysql的用户名 (无默认值): jumpserver
    请输入mysql的密码 (无默认值): weakPassword
    完成

    8. 配置Redis
    是否使用外部redis  (y/n)  (默认为n): y
    请输入redis的主机地址 (无默认值): 192.168.100.11
    请输入redis的端口 (默认为6379): 6379
    请输入redis的密码 (无默认值): weakPassword
    完成

    >>> 二、安装配置Docker
    1. 安装Docker
    完成

    2. 配置Docker
    修改Docker镜像容器的默认存储目录，可以找个最大的磁盘, 并创建目录，如 /opt/docker
    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.2G   48G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    Docker存储目录 (默认为/opt/docker): /var/lib/docker
    完成

    3. 启动Docker
    Docker 版本发生改变 或 docker配置文件发生变化，是否要重启 (y/n)  (默认为y): y
    完成

    >>> 三、加载镜像
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

    >>> 四、安装完成了
    1. 可以使用如下命令启动, 然后访问
    ./jmsctl.sh start

    2. 其它一些管理命令
    ./jmsctl.sh stop
    ./jmsctl.sh restart
    ./jmsctl.sh backup
    ./jmsctl.sh upgrade
    更多还有一些命令，你可以 ./jmsctl.sh --help来了解

    3. 访问 Web 后台页面
    http://192.168.100.236:8080
    https://192.168.100.236:8443

    4. ssh/sftp 访问
    ssh admin@192.168.100.236 -p2222
    sftp -P2222 admin@192.168.100.236

    5. 更多信息
    我们的文档: https://docs.jumpserver.org/
    我们的官网: https://www.jumpserver.org/
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_mysql     ... done
    Creating jms_redis     ... done
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_luna      ... done
    Creating jms_lina      ... done
    Creating jms_guacamole ... done
    Creating jms_koko      ... done
    Creating jms_nginx     ... done
    ```        

## 部署 Nginx 服务

    服务器: 192.168.100.100

!!! tip "配置 Repo"
    ```sh
    vi /etc/yum.repos.d/nginx.repo
    ```
    ```vim
    [nginx-stable]
    name=nginx stable repo
    baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
    gpgcheck=1
    enabled=1
    gpgkey=https://nginx.org/keys/nginx_signing.key
    module_hotfixes=true
    ```

!!! tip "安装 Nginx"
    ```sh
    yum install -y nginx
    ```

!!! tip "配置 Nginx"
    ```sh
    vi /etc/nginx/nginx.conf
    ```
    ```nginx
    user  nginx;
    worker_processes  auto;

    error_log  /var/log/nginx/error.log warn;
    pid        /var/run/nginx.pid;


    events {
        worker_connections  1024;
    }

    stream {
        log_format  proxy  '$remote_addr [$time_local] '
                           '$protocol $status $bytes_sent $bytes_received '
                           '$session_time "$upstream_addr" '
                           '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';

        access_log /var/log/nginx/tcp-access.log  proxy;
        open_log_file_cache off;

        upstream kokossh {
            # core web 节点
            server 192.168.100.21:2222;
            server 192.168.100.22:2222;
            least_conn;
        }

        server {
            listen 2222;
            proxy_pass kokossh;
            proxy_protocol on;
            proxy_connect_timeout 1s;
        }
    }

    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';

        access_log  /var/log/nginx/access.log  main;

        sendfile        on;
        #tcp_nopush     on;

        keepalive_timeout  65;

        #gzip  on;

        include /etc/nginx/conf.d/*.conf;
    }
    ```
    ```sh
    echo > /etc/nginx/conf.d/default.conf
    vi /etc/nginx/conf.d/jumpserver.conf
    ```
    ```nginx
    upstream core_web {
        # 用户连接时使用 ip_hash 负载
        server 192.168.100.21:8080;
        server 192.168.100.22:8080;
        ip_hash;
    }

    upstream core_media {
        # 获取录像失败时自动到对应的 server 取
        server 192.168.100.21:8080 max_fails=2 fail_timeout=2s;
        server 192.168.100.22:8080 max_fails=2 fail_timeout=2s;
        server 192.168.100.31:8080 max_fails=2 fail_timeout=2s;
    }

    upstream core_task {
        # use_task = 1 的任务服务器, 目前只能单任务运行
        server 192.168.100.31:8080;
    }

    server {
        listen 80;
        server_name demo.jumpserver.org;  # 自行修改成你的域名
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name          demo.jumpserver.org;  # 自行修改成你的域名
        ssl_certificate      /etc/nginx/sslkey/1_jumpserver.org.crt;  # 自行设置证书
        ssl_certificate_key  /etc/nginx/sslkey/2_jumpserver.org.key;  # 自行设置证书
        ssl_session_timeout  5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;

        client_max_body_size 4096m;  # 录像上传大小限制

        location ~ /(ops|task|tasks|flower|ws)/ {
            proxy_pass http://core_task;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location ~ /replay/ {
            proxy_pass http://core_media;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504 http_404;
            proxy_next_upstream_tries 5;
        }

        location / {
            proxy_pass http://core_web;
            proxy_buffering  off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }
    }
    ```
    ```sh
    nginx -t
    ```

!!! tip "启动 Nginx"
    ```sh
    systemctl enable nginx
    systemctl start nginx
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
    ```vim
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
    ## 请自行修改账号密码并牢记, 丢失后可以删掉容器后重新用新密码创建, 数据不会丢失
    # 9000                                  # 访问端口
    # MINIO_ROOT_USER=minio                 # minip 账号
    # MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q  # minio 密码
    ```
    ```sh
    docker run --name jms_minio -d -p 9000:9000 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q -v /opt/jumpserver/minio/data:/data -v /opt/jumpserver/minio/config:/root/.minio --restart=always minio/minio:latest server /data
    ```

!!! tip "设置 MinIO"
    - 访问 http://192.168.100.41:9000, 输入刚才设置的 MinIO 账号密码登录
    - 点击右下角的 + 号, 选择 Create bucket 创建桶, Bucket Name 输入 jumpserver 回车确认

!!! tip "设置 JumpServer"
    - 访问 JumpServer Web 页面并使用管理员账号进行登录
    - 点击左侧菜单栏的 [终端管理], 在页面的上方选择 [存储配置], 在 [录像存储] 下方选择 [创建] 选择 [Ceph]
    - 根据下方的说明进行填写, 保存后在 [终端管理] 页面对所有组件进行 [更新], 录像存储选择 [jms-mino], 提交

| 选项            | 参考值                      | 说明                |
| :-------------  | :------------------------- | :------------------ |
| 名称 (Name)     | jms-minio                  | 标识, 不可重复       |
| 类型 (Type)     | Ceph                       | 固定, 不可更改       |
| 桶名称 (Bucket) | jumpserver                 | Bucket Name         |
| Access key      | minio                      | MINIO_ROOT_USER     |
| Secret key      | KXOeyNgDeTdpeu9q           | MINIO_ROOT_PASSWORD |
| 端点 (Endpoint) | http://192.168.184.41:9000 | minio 服务访问地址   |
