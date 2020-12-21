# 升级文档

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致, 否则会导致数据库加密数据无法解密"
    - 更新前请一定要做好备份工作
    - [升级前版本小于 1.4.4 请先按照此文档操作](1.0.0-1.4.3.md)
    - [升级前版本小于 1.4.5 请先按照此文档操作](1.4.4.md)
    - [外置数据库迁移到 MySQL5.7 请先参考此文档](mariadb-mysql.md)

!!! tip "环境说明"
    - 从 v2.5 开始, 数据库要求 MySQL >= 5.7

## 迁移说明

!!! tip "v2.6 版本升级说明"
    - 统一企业版本与开源版本安装方式, 企业版和社区版可以无缝切换
    - 今后只会维护此安装方式, 其他安装方式不再提供技术支持

### 迁移步骤

!!! tip "停止 JumpServer 相关进程"
    === "手动部署"
        ```sh
        cd /opt/koko
        ./koko -s stop
        ```
        ```sh
        /etc/init.d/guacd stop
        sh /config/tomcat9/bin/shutdown.sh
        ```
        ```sh
        cd /opt/jumpserver
        source /opt/py3/bin/activate
        ./jms stop
        ```
        ```sh
        cd /opt
        mv /opt/jumpserver /opt/jumpserver_bak
        ```

    === "setuptools 脚本部署"
        ```sh
        cd /opt/setuptools
        ./jmsctl.sh stop
        systemctl disable jms_core
        mv /opt/jumpserver /opt/jumpserver_bak
        ```

    === "docker 部署"
        ```sh
        docker cp jms_all:/opt/jumpserver /opt/jumpserver_bak
        docker exec -it jms_all /bin/bash
        cd /opt/koko
        ./koko -s stop
        /etc/init.d/guacd stop
        sh /config/tomcat9/bin/shutdown.sh
        cd /opt/jumpserver
        source /opt/py3/bin/activate
        ./jms stop
        ```

    === "docker-compose 部署"
        ```sh
        docker cp jms_core:/opt/jumpserver /opt/jumpserver_bak
        docker stop jms_koko
        docker stop jms_guacamole
        docker stop jms_core
        ```

!!! tip "备份原来的数据库"
    ```yaml
    # 从 jumpserver/config.yml 获取数据库信息
    DB_HOST: 127.0.0.1   # 数据库服务器 IP
    DB_PORT: 3306        # 数据库服务器 端口
    DB_USER: jumpserver  # 连接数据库的用户
    DB_PASSWORD: ******  # 连接数据库用户的密码
    DB_NAME: jumpserver  # JumpServer 使用的数据库
    # mysqldump -h<DB_HOST> -P<DB_PORT> -u<DB_USER> -p<DB_PASSWORD> <DB_NAME> > /opt/<DB_NAME>.sql
    ```
    ```sh
    mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
    ```
    ```sh
    if grep -q 'COLLATE=utf8_bin' /opt/jumpserver.sql; then
        echo "备份数据库字符集正确";
    else
        cp /opt/jumpserver.sql /opt/jumpserver_bak.sql
        sed -i 's@CHARSET=utf8;@CHARSET=utf8 COLLATE=utf8_bin;@' /opt/jumpserver.sql
    fi
    ```

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/v2.6.1/jumpserver-installer-v2.6.1.tar.gz
    tar -xf jumpserver-installer-v2.6.1.tar.gz
    cd jumpserver-installer-v2.6.1
    ```
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="6 7"
    # 修改下面选项, 其他保持默认
    ### 注意: SECRET_KEY 与旧版本不一致, 加密的数据将无法解密

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=                           # 从旧版本的配置文件获取后填入 (*)
    BOOTSTRAP_TOKEN=                      # 从旧版本的配置文件获取后填入 (*)
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true  # 关闭浏览器后 session 过期
    ```
    ```sh
    export DOCKER_IMAGE_PREFIX=docker.mirrors.ustc.edu.cn
    ```
    ```sh
    ./jmsctl.sh install
    ```
    ```nginx hl_lines="26 40 44 48 61 65"

           ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
           ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
      ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
      ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
       ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

    								                             Version:  v2.6.1


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

    设置持久化卷存储目录 (默认为/opt/jumpserver): /data/jumpserver
    完成

    7. 配置MySQL
    是否使用外部mysql (y/n)  (默认为n): n
    完成

    8. 配置Redis
    是否使用外部redis  (y/n)  (默认为n): n
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
    Docker: Pulling from jumpserver/core:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/koko:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/luna:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/guacamole:v2.6.1 	[ OK ]

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
    ```sh
    ./jmsctl.sh stop
    ```
    ```nginx
    Stopping jms_core      ... done
    Stopping jms_koko      ... done
    Stopping jms_guacamole ... done
    Stopping jms_lina      ... done
    Stopping jms_luna      ... done
    Stopping jms_nginx     ... done
    Stopping jms_celery    ... done
    Removing jms_core      ... done
    Removing jms_koko      ... done
    Removing jms_guacamole ... done
    Removing jms_lina      ... done
    Removing jms_luna      ... done
    Removing jms_nginx     ... done
    Removing jms_celery    ... done
    ```
    ```sh
    ./jmsctl.sh restore_db /opt/jumpserver.sql
    ```
    ```nginx
    开始还原数据库: /opt/jumpserver.sql
    mysql: [Warning] Using a password on the command line interface can be insecure.
    数据库恢复成功！
    ```
    ```sh
    mv /opt/jumpserver_bak/data /opt/jumpserver/core/
    ```
    ```sh
    ./jmsctl.sh start
    ```


## 升级说明

!!! tip "要求说明"
    - jumpserver 版本 >= v2.6.0

### 升级步骤

!!! tip "升级到最新版本"
    ```sh
    ./jmsctl.sh check_update
    ```
    ```nginx hl_lines="4"

    最新版本是: v2.6.1
    当前版本是: v2.6.0

    你确定要升级到 v2.6.1 版本吗? (y/n)  (默认为n): y

    1. 检查配置变更
    完成

    2. 检查程序文件变更
    完成

    3. 升级镜像文件
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/lina:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2 	    [ OK ]
    Docker: Pulling from jumpserver/koko:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/luna:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/core:v2.6.1         [ OK ]
    Docker: Pulling from jumpserver/guacamole:v2.6.1 	[ OK ]

    4. 备份数据库
    正在备份...
    mysqldump: [Warning] Using a password on the command line interface can be insecure.
    备份成功! 备份文件已存放至: /opt/jumpserver/db_backup/jumpserver-2020-12-18_12:43:10.sql.gz

    5. 进行数据库变更
    表结构变更可能需要一段时间，请耐心等待 (请确保数据库在运行)
    2020-12-18 12:43:12 Collect static files
    2020-12-18 12:43:12 Collect static files done
    2020-12-18 12:43:12 Check database structure change ...
    2020-12-18 12:43:12 Migrate model change to database ...

    472 static files copied to '/opt/jumpserver/data/static'.
    Operations to perform:
      Apply all migrations: admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, ops, orgs, perms, sessions, settings, terminal, tickets, users
    Running migrations:
      No migrations to apply.
    完成

    6. 升级成功, 可以重启程序了
    ./jmsctl.sh restart
    ```

    ```sh
    ./jmsctl.sh restart
    ```


### 失败处理

!!! tip "如果升级失败可以使用 upgrade 重新升级"
    ```sh
    ./jmsctl.sh upgrade
    ```
    ```nginx hl_lines="1"
    你确定要升级到 v2.6.1 版本吗? (y/n)  (默认为n): y
    1. 检查配置变更
    完成

    2. 检查程序文件变更
    完成

    3. 升级镜像文件
    Docker: Pulling from jumpserver/koko:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/guacamole:v2.6.1 	[ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2 	    [ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/luna:v2.6.1 	    [ OK ]
    Docker: Pulling from jumpserver/core:v2.6.1 	    [ OK ]
    完成
    4. 备份数据库
    正在备份...
    mysqldump: [Warning] Using a password on the command line interface can be insecure.
    备份成功! 备份文件已存放至: /opt/jumpserver/db_backup/jumpserver-2020-12-18_12:47:43.sql.gz

    5. 进行数据库变更
    表结构变更可能需要一段时间，请耐心等待 (请确保数据库在运行)
    2020-12-18 12:47:45 Collect static files
    2020-12-18 12:47:45 Collect static files done
    2020-12-18 12:47:45 Check database structure change ...
    2020-12-18 12:47:45 Migrate model change to database ...

    472 static files copied to '/opt/jumpserver/data/static'.
    Operations to perform:
      Apply all migrations: admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, ops, orgs, perms, sessions, settings, terminal, tickets, users
    Running migrations:
      No migrations to apply.
    完成

    6. 升级成功, 可以重启程序了
    ./jmsctl.sh restart
    ```
    ```sh
    ./jmsctl.sh restart
    ```
