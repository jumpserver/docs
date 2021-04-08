# 升级文档

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致, 否则会导致数据库加密数据无法解密"
    - 更新前请一定要做好备份工作
    - [数据库迁移请先参考此文档](mariadb-mysql.md)
    - [升级前版本小于 1.4.4 请先按照此文档操作](1.0.0-1.4.3.md)
    - [升级前版本小于 1.4.5 请先按照此文档操作](1.4.4.md)

!!! tip "环境说明"
    - 从 v2.5 开始, 要求 MySQL >= 5.7
    - 从 v2.6 开始, 要求 Redis >= 5
    - 推荐使用外置 数据库 和 Redis, 方便日后扩展升级

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 5.0  |
| MariaDB | >= 10.2 |    |       |         |

## 迁移说明

!!! tip "v2.6 版本升级说明"
    - 统一企业版本与开源版本安装方式, 企业版和社区版可以无缝切换
    - 今后只会维护此安装方式, 其他安装方式不再提供技术支持
    - 安装完成后配置文件在 /opt/jumpserver/config/config.txt

### 迁移步骤

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

    === "手动部署"
        ```sh
        cd /opt/koko
        ./koko -s stop
        # 更老的版本使用的 coco
        # cd /opt/coco
        # ./cocod stop
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
        ```sh
        mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
        ```

    === "组件容器化部署"
        ```sh
        docker stop jms_koko jms_guacamole
        docker rm jms_koko jms_guacamole
        # 更老的版本使用的 coco
        # docker stop jms_coco
        # docker rm jms_coco
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
        ```sh
        mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
        ```

    === "setuptools 脚本部署"
        ```sh
        cd /opt/setuptools
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
    if grep -q 'COLLATE=utf8_bin' /opt/jumpserver.sql; then
        cp /opt/jumpserver.sql /opt/jumpserver_bak.sql
        sed -i 's@COLLATE=utf8_bin@@g' /opt/jumpserver.sql
        sed -i 's@COLLATE utf8_bin@@g' /opt/jumpserver.sql
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

!!! tip "开始部署 JumpServer"

    === "使用内置数据库"
        ```sh
        ./jmsctl.sh install
        ```
        ```nginx hl_lines="19 23 59 68 72 75"

               ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
               ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
               ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
          ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
          ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
           ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

        								                             Version:  {{ jumpserver.version }}


        >>> 安装配置 Docker
        1. 安装 Docker
        开始下载 Docker 程序 ...
        完成
        开始下载 Docker Compose 程序 ...
        完成

        2. 配置 Docker
        是否需要自定义 Docker 数据目录, 默认将使用 /var/lib/docker 目录? (y/n)  (默认为 n): n
        完成

        3. 启动 Docker
        Docker 版本发生改变 或 Docker 配置文件发生变化，是否要重启? (y/n)  (默认为 y): y
        完成

        >>> 加载 Docker 镜像
        Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
        Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
        Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
        Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
        Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
        Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
        Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
        Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

        >>> 安装配置 JumpServer
        1. 检查配置文件
        配置文件位置: /opt/jumpserver/config
        /opt/jumpserver/config/config.txt                 [ √ ]
        /opt/jumpserver/config/nginx/lb_http_server.conf  [ √ ]
        /opt/jumpserver/config/nginx/lb_ssh_server.conf   [ √ ]
        /opt/jumpserver/config/core/config.yml   [ √ ]
        /opt/jumpserver/config/koko/config.yml   [ √ ]
        /opt/jumpserver/config/mysql/my.cnf      [ √ ]
        /opt/jumpserver/config/redis/redis.conf  [ √ ]
        完成

        2. 配置 Nginx
        配置文件位置:: /opt/jumpserver/config/nginx/cert
        /opt/jumpserver/config/nginx/cert/server.crt  [ √ ]
        /opt/jumpserver/config/nginx/cert/server.key  [ √ ]
        完成

        3. 备份配置文件
        备份至 /opt/jumpserver/config/backup/config.txt.2021-03-19_08-01-51
        完成

        4. 配置网络
        是否需要支持 IPv6? (y/n)  (默认为 n): n
        完成

        5. 配置加密密钥
        SECRETE_KEY:     ICAgIGluZXQ2IDI0MDk6OGE0ZDpjMjg6ZjkwMTo6ZDRjLzEyO
        BOOTSTRAP_TOKEN: ICAgIGluZXQ2IDI0
        完成

        6. 配置持久化目录
        是否需要自定义持久化存储, 默认将使用目录 /opt/jumpserver? (y/n)  (默认为 n): n
        完成

        7. 配置 MySQL
        是否使用外部mysql (y/n)  (默认为n): n

        8. 配置 Redis
        是否使用外部redis  (y/n)  (默认为n): n

        >>> 安装完成了
        1. 可以使用如下命令启动, 然后访问
        ./jmsctl.sh start

        2. 其它一些管理命令
        ./jmsctl.sh stop
        ./jmsctl.sh restart
        ./jmsctl.sh backup
        ./jmsctl.sh upgrade
        更多还有一些命令, 你可以 ./jmsctl.sh --help 来了解

        3. Web 访问
        http://192.168.100.248:8080
        https://192.168.100.248:8443
        默认用户: admin  默认密码: admin

        4. SSH/SFTP 访问
        ssh admin@192.168.100.248 -p2222
        sftp -P2222 admin@192.168.100.248

        5. 更多信息
        我们的官网: https://www.jumpserver.org/
        我们的文档: https://docs.jumpserver.org/
        ```

    === "使用外置数据库"
        ```sh
        ./jmsctl.sh install
        ```
        ```nginx hl_lines="19 23 59 68 72-77 81-84"

               ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
               ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
               ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
          ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
          ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
           ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

        								                             Version:  {{ jumpserver.version }}


        >>> 安装配置 Docker
        1. 安装 Docker
        开始下载 Docker 程序 ...
        完成
        开始下载 Docker Compose 程序 ...
        完成

        2. 配置 Docker
        是否需要自定义 Docker 数据目录, 默认将使用 /var/lib/docker 目录? (y/n)  (默认为 n): n
        完成

        3. 启动 Docker
        Docker 版本发生改变 或 Docker 配置文件发生变化，是否要重启? (y/n)  (默认为 y): y
        完成

        >>> 加载 Docker 镜像
        Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
        Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
        Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
        Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
        Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
        Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
        Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
        Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

        >>> 安装配置 JumpServer
        1. 检查配置文件
        配置文件位置: /opt/jumpserver/config
        /opt/jumpserver/config/config.txt                 [ √ ]
        /opt/jumpserver/config/nginx/lb_http_server.conf  [ √ ]
        /opt/jumpserver/config/nginx/lb_ssh_server.conf   [ √ ]
        /opt/jumpserver/config/core/config.yml   [ √ ]
        /opt/jumpserver/config/koko/config.yml   [ √ ]
        /opt/jumpserver/config/mysql/my.cnf      [ √ ]
        /opt/jumpserver/config/redis/redis.conf  [ √ ]
        完成

        2. 配置 Nginx
        配置文件位置:: /opt/jumpserver/config/nginx/cert
        /opt/jumpserver/config/nginx/cert/server.crt  [ √ ]
        /opt/jumpserver/config/nginx/cert/server.key  [ √ ]
        完成

        3. 备份配置文件
        备份至 /opt/jumpserver/config/backup/config.txt.2021-03-19_08-01-51
        完成

        4. 配置网络
        是否需要支持 IPv6? (y/n)  (默认为 n): n
        完成

        5. 配置加密密钥
        SECRETE_KEY:     ICAgIGluZXQ2IDI0MDk6OGE0ZDpjMjg6ZjkwMTo6ZDRjLzEyO
        BOOTSTRAP_TOKEN: ICAgIGluZXQ2IDI0
        完成

        6. 配置持久化目录
        是否需要自定义持久化存储, 默认将使用目录 /opt/jumpserver? (y/n)  (默认为 n): n
        完成

        7. 配置 MySQL
        是否使用外部mysql (y/n)  (默认为n): y
        请输入mysql的主机地址 (无默认值): 192.168.100.11
        请输入mysql的端口 (默认为3306): 3306
        请输入mysql的数据库(事先做好授权) (默认为jumpserver): jumpserver
        请输入mysql的用户名 (无默认值): jumpserver
        请输入mysql的密码 (无默认值): weakPassword
        完成

        8. 配置 Redis
        是否使用外部redis  (y/n)  (默认为n): y
        请输入redis的主机地址 (无默认值): 192.168.100.11
        请输入redis的端口 (默认为6379): 6379
        请输入redis的密码 (无默认值): weakPassword
        完成

        >>> 安装完成了
        1. 可以使用如下命令启动, 然后访问
        ./jmsctl.sh start

        2. 其它一些管理命令
        ./jmsctl.sh stop
        ./jmsctl.sh restart
        ./jmsctl.sh backup
        ./jmsctl.sh upgrade
        更多还有一些命令, 你可以 ./jmsctl.sh --help 来了解

        3. Web 访问
        http://192.168.100.248:8080
        https://192.168.100.248:8443
        默认用户: admin  默认密码: admin

        4. SSH/SFTP 访问
        ssh admin@192.168.100.248 -p2222
        sftp -P2222 admin@192.168.100.248

        5. 更多信息
        我们的官网: https://www.jumpserver.org/
        我们的文档: https://docs.jumpserver.org/
        ```


    ```sh
    mkdir -p /opt/jumpserver/core/
    mv /opt/jumpserver_bak/data /opt/jumpserver/core/
    ```
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_luna      ... done
    Creating jms_lina      ... done
    Creating jms_guacamole ... done
    Creating jms_koko      ... done
    Creating jms_nginx     ... done
    ```
    ```sh
    docker exec -it jms_mysql /bin/bash
    mysql -uroot -p$DB_PASSWORD
    ```
    ```mysql
    drop database jumpserver;
    create database jumpserver default charset 'utf8';
    exit
    exit
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
    ./jmsctl.sh restart
    ```


## 升级说明

!!! tip "要求说明"
    - jumpserver 版本 >= v2.6.0
    - jumpserver 版本 <  v2.6.0 的请先参考上面的迁移文档迁移到最新版本

### 升级步骤

!!! tip "操作步骤"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```
    ```sh
    ./jmsctl.sh upgrade
    ```
    ```nginx hl_lines="1 35"
    是否将版本更新至 {{ jumpserver.version }} ? (y/n)  (默认为 n): y

    1. 检查配置变更
    /opt/jumpserver/config/nginx/lb_http_server.conf  [ √ ]
    /opt/jumpserver/config/nginx/lb_ssh_server.conf   [ √ ]
    /opt/jumpserver/config/core/config.yml   [ √ ]
    /opt/jumpserver/config/koko/config.yml   [ √ ]
    /opt/jumpserver/config/mysql/my.cnf      [ √ ]
    /opt/jumpserver/config/redis/redis.conf  [ √ ]
    完成

    2. 检查程序文件变更
    完成
    完成

    3. 升级镜像文件
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

    完成

    4. 备份数据库
    正在备份...
    mysqldump: [Warning] Using a password on the command line interface can be insecure.
    [SUCCESS] 备份成功! 备份文件已存放至: /opt/jumpserver/db_backup/jumpserver-2021-03-19_08:32:39.sql

    5. 进行数据库变更
    表结构变更可能需要一段时间, 请耐心等待
    检测到 jms_core 正在运行, 是否需要关闭 jms_core 并继续升级? (y/n)  (默认为 n): y
    jms_core
    jms_core
    2021-03-19 08:32:44 Collect static files
    2021-03-19 08:32:44 Collect static files done
    2021-03-19 08:32:44 Check database structure change ...
    2021-03-19 08:32:44 Migrate model change to database ...

    473 static files copied to '/opt/jumpserver/data/static'.
    Operations to perform:
      Apply all migrations: acls, admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, ops, orgs, perms, sessions, settings, terminal, tickets, users
    Running migrations:
      No migrations to apply.
    完成

    6. 升级成功, 可以重启程序了
    ./jmsctl.sh restart
    ```
    ```sh
    ./jmsctl.sh restart
    ```
