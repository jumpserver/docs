# 部署 JumpServer 01 节点

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - JumpServer_Node_01 服务器信息如下: 
    
    ```sh 
    192.168.100.21
    ```

## 2 配置 NFS
### 2.1 安装 NFS 依赖包
!!! tip ""
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.11
    ```

### 2.2 挂载 NFS 目录
!!! tip ""
    ```sh
    # 将 Core 持久化目录挂载到 NFS, 默认 /opt/jumpserver/core/data, 请根据实际情况修改
    # JumpServer 持久化目录定义相关参数为 VOLUME_DIR, 在安装 JumpServer 过程中会提示
    mkdir /opt/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /opt/jumpserver/core/data
    ```

### 2.3 配置 NFS 共享目录开机自动挂载
!!! tip ""
    ```sh
    # 可以写入到 /etc/fstab, 重启自动挂载. 注意: 设置后如果 nfs 损坏或者无法连接该服务器将无法启动
    echo "192.168.100.11:/data /opt/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

## 3 安装 JumpServer 
### 3.1 下载 jumpserver-install 软件包
!!! tip ""
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.tag }}/jumpserver-installer-{{ jumpserver.tag }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.tag }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.tag }}
    ```

### 3.2 修改临时配置文件
!!! warning "注意"
    - 配置文件中的 bootstrap_token , SECRET_KEY 必须和要其他 JumpServer 服务器一致, 否则加密的数据将无法解密

!!! tip ""
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="6 11-15 18-23 26-29 32"
    # 修改下面选项, 其他保持默认, 请勿直接复制此处内容

    # 安装配置
    ### 注意持久化目录 VOLUME_DIR, 如果上面 NFS 挂载其他目录, 此处也要修改. 如: NFS 挂载到 /data/jumpserver/core/data, 则 VOLUME_DIR=/data/jumpserver
    VOLUME_DIR=/opt/jumpserver


    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密, 请勿直接复制下面的字符串
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW    # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                                 # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR                                                  # 日志等级
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True                             # 关闭浏览器 session 过期

    # PostgreSQL 配置
    DB_ENGINE=postgresql
    DB_HOST=192.168.100.11
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=KXOeyNgDeTdpeu9q
    DB_NAME=jumpserver

    # Redis 配置

    REDIS_HOST=192.168.100.11
    REDIS_PORT=6379
    REDIS_PASSWORD=KXOeyNgDeTdpeu9q

    # KoKo Lion 配置
    SHARE_ROOM_TYPE=redis                                            # KoKo Lion 使用 redis 共享
    REUSE_CONNECTION=False                                           # Koko 禁用连接复用
    ```

### 3.3 执行脚本安装 JumpServer 服务
!!! tip ""
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

    								                                     Version:  {{ jumpserver.tag }}


    1. 检查配置文件
    配置文件位置: /opt/jumpserver/config
    /opt/jumpserver/config/config.txt  [ √ ]
    /opt/jumpserver/config/nginx/lb_rdp_server.conf  [ √ ]
    /opt/jumpserver/config/nginx/lb_ssh_server.conf  [ √ ]
    /opt/jumpserver/config/nginx/cert/server.crt  [ √ ]
    /opt/jumpserver/config/nginx/cert/server.key  [ √ ]
    完成

    >>> 安装配置 Docker
    1. 安装 Docker
    完成

    2. 配置 Docker
    完成

    3. 启动 Docker
    完成

    >>> 加载 Docker 镜像
    redis:7.0-bullseye <= images/redis:7.0-bullseye.zst 
    Loaded image: redis:7.0-bullseye
    postgres:16.3-bullseye <= images/postgres:16.3-bullseye.zst 
    Loaded image: postgres:16.3-bullseye
    registry.fit2cloud.com/jumpserver/core:v4.10.5-ee <= images/core:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/core:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/koko:v4.10.5-ee <= images/koko:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/koko:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/lion:v4.10.5-ee <= images/lion:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/lion:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/chen:v4.10.5-ee <= images/chen:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/chen:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/web:v4.10.5-ee <= images/web:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/web:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/magnus:v4.10.5-ee <= images/magnus:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/magnus:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/razor:v4.10.5-ee <= images/razor:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/razor:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/video-worker:v4.10.5-ee <= images/video-worker:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/video-worker:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/xrdp:v4.10.5-ee <= images/xrdp:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/xrdp:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/panda:v4.10.5-ee <= images/panda:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/panda:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/nec:v4.10.5-ee <= images/nec:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/nec:v4.10.5-ee
    registry.fit2cloud.com/jumpserver/facelive:v4.10.5-ee <= images/facelive:v4.10.5-ee.zst 
    Loaded image: registry.fit2cloud.com/jumpserver/facelive:v4.10.5-ee
    完成

    >>> 安装配置 JumpServer
    1. 配置加密密钥
    完成

    2. 配置持久化目录
    是否需要自订持久化储存的路径？不自订将使用默认目录 /data/jumpserver? (y/n)  (默认为 n): n
    完成

    3. 配置数据库
    是否使用外部 PostgreSQL? (y/n)  (默认为 n): y
    请输入数据库的主机地址 (无默认值): 192.168.100.11
    请输入数据库的端口 (默认为 5432): 5432
    请输入数据库的名称 (无默认值): jumpserver
    请输入数据库的用户名 (无默认值): jumpserver
    请输入数据库的密码 (无默认值):  KXOeyNgDeTdpeu9q
    完成

    4. 配置 Redis
    请输入 Redis 模式? (redis/sentinel)  (默认为 redis): 
    是否使用外部 Redis? (y/n)  (默认为 n): y
    请输入 Redis 的主机地址 (无默认值): 192.168.100.11
    请输入 Redis 的端口 (默认为6379): 6379
    请输入 Redis 的密码 (无默认值): KXOeyNgDeTdpeu9q
    完成

    5.  配置外部访问
    是否需要配置 JumpServer 对外访问端口? (y/n)  (默认为 n): n
    完成

    6. 初始化数据库
    [+] Running 4/4
    ✔ Network jms_net           Created                                                                                                                                                                         0.1s 
    ✔ Container jms_redis       Started                                                                                                                                                                         0.4s 
    ✔ Container jms_core        Started                                                                                                                                                                         0.4s 
    ✔ Container jms_postgresql  Started         
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
    cd /root/jumpserver-installer-{{ jumpserver.tag }}
    ./jmsctl.sh start

    2. 其它一些管理命令
    ./jmsctl.sh stop
    ./jmsctl.sh restart
    ./jmsctl.sh backup
    ./jmsctl.sh upgrade
    更多还有一些命令, 你可以 ./jmsctl.sh --help 来了解

    3. Web 访问
    http://192.168.100.212:80
    默认用户: admin  默认密码: ChangeMe

    4. SSH/SFTP 访问
    ssh -p2222 admin@192.168.100.212
    sftp -P2222 admin@192.168.100.212

    5. 更多信息
    我们的官网: https://www.jumpserver.org/
    我们的文档: https://docs.jumpserver.org/
    ```

### 3.4 启动 JumpServer 服务
!!! tip ""
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_lion      ... done
    Creating jms_koko      ... done
    Creating jms_magnus    ... done
    Creating jms_web       ... done
    ```

# 部署 JumpServer 02 节点

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - JumpServer_Node_02 服务器信息如下: 
    
    ```sh 
    192.168.100.22
    ```

## 2 配置 NFS
### 2.1 安装 NFS 依赖包
!!! tip ""
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.11
    ```

### 2.2 挂载 NFS 目录
!!! tip ""
    ```sh
    # 将 Core 持久化目录挂载到 NFS, 默认 /opt/jumpserver/core/data, 请根据实际情况修改
    # JumpServer 持久化目录定义相关参数为 VOLUME_DIR, 在安装 JumpServer 过程中会提示
    mkdir /opt/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /opt/jumpserver/core/data
    ```

### 2.3 配置 NFS 共享目录开机自动挂载
!!! tip ""
    ```sh
    # 可以写入到 /etc/fstab, 重启自动挂载. 注意: 设置后如果 nfs 损坏或者无法连接该服务器将无法启动
    echo "192.168.100.11:/data /opt/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

## 3 安装 JumpServer 
### 3.1 下载 jumpserver-install 软件包
!!! tip ""
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.tag }}/jumpserver-installer-{{ jumpserver.tag }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.tag }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.tag }}
    ```

### 3.2 修改临时配置文件
!!! tip ""
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="6 11-15 18-23 26-29 32"
    # 修改下面选项, 其他保持默认, 请勿直接复制此处内容
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    # 安装配置
    ### 注意持久化目录 VOLUME_DIR, 如果上面 NFS 挂载其他目录, 此处也要修改. 如: NFS 挂载到 /data/jumpserver/core/data, 则 VOLUME_DIR=/data/jumpserver
    VOLUME_DIR=/opt/jumpserver


    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密, 请勿直接复制下面的字符串
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW    # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                                 # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR                                                  # 日志等级
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True                             # 关闭浏览器 session 过期

    # PostgreSQL 配置
    DB_ENGINE=postgresql
    DB_HOST=192.168.100.11
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=KXOeyNgDeTdpeu9q
    DB_NAME=jumpserver

    # Redis 配置

    REDIS_HOST=192.168.100.11
    REDIS_PORT=6379
    REDIS_PASSWORD=KXOeyNgDeTdpeu9q

    # KoKo Lion 配置
    SHARE_ROOM_TYPE=redis                                            # KoKo Lion 使用 redis 共享
    REUSE_CONNECTION=False                                           # Koko 禁用连接复用
    ```

### 3.3 执行脚本安装 JumpServer 服务
!!! tip ""
    ```sh
    ./jmsctl.sh install
    ```

### 3.4 启动 JumpServer 服务
!!! tip ""
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_lion      ... done
    Creating jms_koko      ... done
    Creating jms_magnus    ... done
    Creating jms_web       ... done
    ```