# 迁移文档

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致，否则会导致数据库加密数据无法解密"

## 迁移说明

!!! tip "v2.6 版本升级说明"
    - 统一企业版本与开源版本安装方式，企业版和社区版可以无缝切换
    - 今后只会维护此安装方式，其他安装方式不再提供技术支持
    - 安装完成后配置文件在 /opt/jumpserver/config/config.txt

## 迁移步骤

!!! tip "备份数据库"
    ```yaml
    # 从 jumpserver/config.yml 获取数据库信息
    DB_HOST: 127.0.0.1   # 数据库服务器 IP
    DB_PORT: 3306        # 数据库服务器 端口
    DB_USER: jumpserver  # 连接数据库的用户
    DB_PASSWORD: ******  # 连接数据库用户的密码
    DB_NAME: jumpserver  # JumpServer 使用的数据库
    # mysqldump -h<DB_HOST> -P<DB_PORT> -u<DB_USER> -p<DB_PASSWORD> <DB_NAME> > /opt/<DB_NAME>.sql
    ```

    === "installer 部署"
        ```sh
        # 记录 SECRET_KEY 和 BOOTSTRAP_TOKEN
        cat /opt/jumpserver/config/config.txt | egrep "SECRET_KEY|BOOTSTRAP_TOKEN"
        ```
        ```sh
        ./jmsctl.sh backup_db
        ```

    === "源码部署"
        ```sh
        cd /opt/koko
        ./koko -s stop
        # 更老的版本使用的 coco guacamole
        # cd /opt/coco
        # ./cocod stop
        # /etc/init.d/guacd stop
        # sh /config/tomcat9/bin/shutdown.sh
        ```
        ```sh
        cd /opt/lion
        ps aux | grep lion | awk '{print $2}' | xargs kill -9
        ```
        ```sh
        cd /opt/jumpserver

        # 记录 SECRET_KEY 和 BOOTSTRAP_TOKEN
        cat config.yml | egrep "SECRET_KEY|BOOTSTRAP_TOKEN"
        ```
        ```sh
        source /opt/py3/bin/activate
        ./jms stop
        ```
        ```sh
        cd /opt
        mv /opt/jumpserver /opt/jumpserver_bak
        ```
        ```sh
        mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
        ```

    === "组件容器化部署"
        ```sh
        docker stop jms_koko jms_lion     
        docker rm jms_koko jms_lion     
        # 更老的版本使用的 coco guacamole
        # docker stop jms_coco jms_guacamole
        # docker rm jms_coco jms_guacamole
        ```
        ```sh
        cd /opt/jumpserver

        # 记录 SECRET_KEY 和 BOOTSTRAP_TOKEN
        cat config.yml | egrep "SECRET_KEY|BOOTSTRAP_TOKEN"
        ```
        ```sh
        source /opt/py3/bin/activate
        ./jms stop
        ```
        ```sh
        cd /opt
        mv /opt/jumpserver /opt/jumpserver_bak
        ```
        ```sh
        mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
        ```

    === "setuptools 脚本部署"
        ```sh
        cd /opt/setuptools

        # 记录 SECRET_KEY 和 BOOTSTRAP_TOKEN
        cat config.conf | egrep "SECRET_KEY|BOOTSTRAP_TOKEN"
        ```
        ```sh
        ./jmsctl.sh stop
        docker rm jms_koko jms_guacamole
        systemctl disable jms_core
        mv /opt/jumpserver /opt/jumpserver_bak
        ```
        ```sh
        mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
        ```

    === "docker 部署"
        ```sh
        docker cp jms_all:/opt/jumpserver /opt/jumpserver_bak

        # 记录 SECRET_KEY 和 BOOTSTRAP_TOKEN
        docker exec -it jms_all env | egrep "SECRET_KEY|BOOTSTRAP_TOKEN"
        ```
        ```sh
        docker exec -it jms_all /bin/bash
        mysqldump -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASSWORD $DB_NAME > /opt/jumpserver.sql
        exit
        ```
        ```sh
        docker cp jms_all:/opt/jumpserver.sql /opt
        docker stop jms_all
        ```

    === "docker-compose 部署"
        ```sh
        docker cp jms_core:/opt/jumpserver /opt/jumpserver_bak

        # 记录 SECRET_KEY 和 BOOTSTRAP_TOKEN
        docker exec -it jms_core env | egrep "SECRET_KEY|BOOTSTRAP_TOKEN"
        ```
        ```sh
        docker exec -it jms_mysql /bin/bash
        mysqldump -uroot jumpserver > /opt/jumpserver.sql
        exit
        ```
        ```sh
        docker cp jms_mysql:/opt/jumpserver.sql /opt
        cd /opt/Dockerfile
        docker-compose stop
        ```

!!! tip "修改数据库字符集"
    ```sh
    # 如果你不需要或不想处理数据库字符集可以跳过此步骤, 保证迁移前后的数据库字符集一样即可.
    if grep -q 'COLLATE=utf8_bin' /opt/jumpserver.sql; then
        cp /opt/jumpserver.sql /opt/jumpserver_bak.sql
        sed -i 's@ COLLATE=utf8_bin@@g' /opt/jumpserver.sql
        sed -i 's@ COLLATE utf8_bin@@g' /opt/jumpserver.sql
    else
        echo "备份数据库字符集正确";
    fi
    ```

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="3 9-10"
    # 修改下面选项, 其他保持默认
    ### 数据持久化目录, 安装完成后请勿随意更改, 可以使用其他目录如: /data/jumpserver
    VOLUME_DIR=/opt/jumpserver

    ### 注意: SECRET_KEY 与旧版本不一致, 加密的数据将无法解密

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=                           # 从旧版本的配置文件获取后填入 (*)
    BOOTSTRAP_TOKEN=                      # 从旧版本的配置文件获取后填入 (*)
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True  # 关闭浏览器后 session 过期
    ```

!!! tip "开始部署 JumpServer"

    === "使用新的内置数据库"
        ```sh
        ./jmsctl.sh install
        ```
        ```nginx hl_lines="31 48 57 61 65 69"

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
        Docker: Pulling from jumpserver/web:{{ jumpserver.version }}  	    [ OK ]
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
        是否使用外部 MySQL? (y/n)  (默认为 n): n
        完成

        5. 配置 Redis
        是否使用外部 Redis? (y/n)  (默认为 n): n
        完成

        6. 配置对外端口
        是否需要配置 JumpServer 对外访问端口? (y/n)  (默认为 n): n
        完成

        7. 初始化数据库
        Creating network "jms_net" with driver "bridge"
        Creating jms_mysql ... done
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
        ```sh
        docker exec -it jms_mysql /bin/bash
        # arm64 请使用 $MARIADB_ROOT_PASSWORD
        mysql -uroot -p$MYSQL_ROOT_PASSWORD
        ```
        ```mysql
        drop database jumpserver;
        create database jumpserver default charset 'utf8';
        exit
        exit
        ```
        ```sh
        # /opt/jumpserver.sql 为旧版本数据库
        ./jmsctl.sh restore_db /opt/jumpserver.sql
        ```
        ```nginx
        开始还原数据库: /opt/jumpserver.sql
        mysql: [Warning] Using a password on the command line interface can be insecure.
        数据库恢复成功！
        ```
        ```sh
        ./jmsctl.sh start
        ```

    === "使用新的外置数据库"
        ```sh
        # 登录外置数据库操作
        mysql -h192.168.100.11 -P3306 -ujumpserver -pweakPassword
        ```
        ```mysql
        create database jumpserver default charset 'utf8';
        create user 'jumpserver'@'%' identified by 'weakPassword';
        grant all on jumpserver.* to 'jumpserver'@'%';
        flush privileges;
        exit
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
        Docker: Pulling from jumpserver/web:{{ jumpserver.version }}  	    [ OK ]
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
        请输入 MySQL 的端口 (默认为 3306): 3306
        请输入 MySQL 的数据库 (默认为 jumpserver): jumpserver
        请输入 MySQL 的用户名 (无默认值): jumpserver
        请输入 MySQL 的密码 (无默认值): weakPassword
        完成

        5. 配置 Redis
        是否使用外部 Redis? (y/n)  (默认为 n): y
        请输入 Redis 的主机地址 (无默认值): 192.168.100.11
        请输入 Redis 的端口 (默认为 6379): 6379
        请输入 Redis 的密码 (无默认值): weakPassword
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
        ```sh
        ./jmsctl.sh start
        ```
        ```nginx
        Creating network "jms_net" with driver "bridge"
        Creating jms_core      ... done
        Creating jms_celery    ... done
        Creating jms_koko      ... done
        Creating jms_magnus    ... done
        Creating jms_web       ... done
        ```

    === "使用旧的外置数据库"
        ```sh
        # 如果之前使用的数据库符合版本要求, 可以直接使用 (注意备份)
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
        Docker: Pulling from jumpserver/web:{{ jumpserver.version }}  	    [ OK ]
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
        请输入 MySQL 的端口 (默认为 3306): 3306
        请输入 MySQL 的数据库 (默认为 jumpserver): jumpserver
        请输入 MySQL 的用户名 (无默认值): jumpserver
        请输入 MySQL 的密码 (无默认值): weakPassword
        完成

        5. 配置 Redis
        是否使用外部 Redis? (y/n)  (默认为 n): y
        请输入 Redis 的主机地址 (无默认值): 192.168.100.11
        请输入 Redis 的端口 (默认为 6379): 6379
        请输入 Redis 的密码 (无默认值): weakPassword
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
        ```sh
        ./jmsctl.sh start
        ```
        ```nginx
        Creating network "jms_net" with driver "bridge"
        Creating jms_core      ... done
        Creating jms_celery    ... done
        Creating jms_koko      ... done
        Creating jms_magnus    ... done
        Creating jms_web       ... done
        ```
