更新升级
-------------

**升级及迁移请保持 SECRET_KEY 与旧版本一致, 否则会导致数据库加密数据无法解密**

1.0.0-1.4.3 升级到 1.4.4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**请务必认真详细阅读每一个文字并理解后才能操作升级事宜**

- 请先检查自己各组件的当前版本
- 不支持从 0.x 版本升级到 1.x 版本
- 本文档仅针对 1.0.x - 1.4.3 的版本升级教程
- 从 1.4.x 版本开始 mysql 版本需要大于等于 5.6, mariadb 版本需要大于等于 5.5.56
- 更新配置文件需要把对应旧版本的设置复制到新的配置文件

0. 检查数据库表结构文件是否完整

.. code-block:: shell

    # 为了保证能顺利升级, 请先检查数据库表结构文件是否完整
    $ cd /opt/jumpserver/apps
    $ for d in $(ls); do if [ -d $d ] && [ -d $d/migrations ]; then ll ${d}/migrations/*.py | grep -v __init__.py; fi; done

    # 新开一个终端, 连接到 jumpserver 的数据库服务器
    $ mysql -uroot -p
    > use jumpserver;
    > select app, name from django_migrations where app in('assets', 'audits', 'common', 'ops', 'orgs', 'perms', 'terminal', 'users') order by app asc;

    # 如果左右对比信息不一致, 通过升级常见问题解决

丢失表结构文件参考 `升级常见问题 <faq_upgrade.html>`_

1. 备份 JumpServer

.. code-block:: shell

    $ cp -r /opt/jumpserver /opt/jumpserver_bak
    $ mysqldump -uroot -p jumpserver > /opt/jumpserver.sql

.. code-block:: shell

    # 通过 releases 包升级需要还原这些文件, 通过 git pull 升级不需要执行
    $ cd /opt/jumpserver_bak/apps
    $ for d in $(ls);do
        if [ -d $d ] && [ -d $d/migrations ];then
          cp ${d}/migrations/*.py /opt/jumpserver/apps/${d}/migrations/
        fi
      done

2. 升级 JumpServer

.. code-block:: shell

    $ cd /opt/jumpserver
    $ source /opt/py3/bin/activate
    $ ./jms stop
    $ git fetch
    $ git checkout 1.4.4

.. code-block:: shell

    $ mv config.py config_old.bak
    $ cp config_example.py config.py
    $ vi config.py  # 把 config_old.bak 里面的对应设置填到新的配置文件

.. code-block:: python

    """
        jumpserver.config
        ~~~~~~~~~~~~~~~~~

        JumpServer project setting file

        :copyright: (c) 2014-2017 by JumpServer Team
        :license: GPL v2, see LICENSE for more details.
    """
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


    class Config:
        # Use it to encrypt or decrypt data

        # JumpServer 使用 SECRET_KEY 进行加密, 请务必修改以下设置
        # 保持与你原来的 SECRET_KEY 一致, 可查看 config_old.bak
        SECRET_KEY = os.environ.get('SECRET_KEY') or '2vym+ky!997d5kkcc64mnz06y1mmui3lut#(^wd=%s_qj$1%x'

        # Django security setting, if your disable debug model, you should setting that
        ALLOWED_HOSTS = ['*']

        # DEBUG 模式 True为开启 False为关闭, 默认开启, 生产环境推荐关闭
        # 注意：如果设置了DEBUG = False, 访问8080端口页面会显示不正常, 需要搭建 nginx 代理才可以正常访问
        DEBUG = os.environ.get("DEBUG") or False

        # 日志级别, 默认为DEBUG, 可调整为INFO, WARNING, ERROR, CRITICAL, 默认INFO
        LOG_LEVEL = os.environ.get("LOG_LEVEL") or 'WARNING'
        LOG_DIR = os.path.join(BASE_DIR, 'logs')

        # 使用的数据库配置, 支持sqlite3, mysql, postgres等, 默认使用sqlite3
        # See https://docs.djangoproject.com/en/1.10/ref/settings/#databases

        # 默认使用SQLite3, 如果使用其他数据库请注释下面两行
        # DB_ENGINE = 'sqlite3'
        # DB_NAME = os.path.join(BASE_DIR, 'data', 'db.sqlite3')

        # 请手动修改下面数据库设置, 保持与你原来的设置一致, 可查看config_old.bak
        DB_ENGINE = os.environ.get("DB_ENGINE") or 'mysql'
        DB_HOST = os.environ.get("DB_HOST") or '127.0.0.1'
        DB_PORT = os.environ.get("DB_PORT") or 3306
        DB_USER = os.environ.get("DB_USER") or 'jumpserver'
        DB_PASSWORD = os.environ.get("DB_PASSWORD") or 'weakPassword'
        DB_NAME = os.environ.get("DB_NAME") or 'jumpserver'

        # Django 监听的ip和端口
        # ./manage.py runserver 127.0.0.1:8080
        HTTP_BIND_HOST = '0.0.0.0'
        HTTP_LISTEN_PORT = 8080

        # 请手动修改下面 Redis 设置, 保持与你原来的设置一致, 可查看config_old.bak
        REDIS_HOST = os.environ.get("REDIS_HOST") or '127.0.0.1'
        REDIS_PORT = os.environ.get("REDIS_PORT") or 6379
        REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD") or ''
        REDIS_DB_CELERY = os.environ.get('REDIS_DB') or 3
        REDIS_DB_CACHE = os.environ.get('REDIS_DB') or 4

        def __init__(self):
            pass

        def __getattr__(self, item):
            return None


    class DevelopmentConfig(Config):
        pass


    class TestConfig(Config):
        pass


    class ProductionConfig(Config):
        pass


    # Default using Config settings, you can write if/else for different env
    config = DevelopmentConfig()

.. code-block:: shell

    $ pip install -r requirements/requirements.txt
    $ cd utils
    $ sh make_migrations.sh

.. code-block:: shell

    # 升级前版本小于 1.1.0 需要执行此步骤
    $ sh 2018_04_11_migrate_permissions.sh

.. code-block:: shell

    # 升级前版本小于 1.4.0 需要执行此步骤, 没有此文件则跳过
    $ sh 2018_07_15_set_win_protocol_to_ssh.sh

.. code-block:: shell

    # 启动 jumpserver
    $ cd ../
    $ ./jms start -d

.. code-block:: nginx

    # 升级前版本小于 1.4.2 需要执行此步骤
    $ vi /etc/nginx/conf.d/jumpserver.conf  # 部分用户的配置文件是/etc/nginx/nginx.conf

    server {
        listen 80;

        client_max_body_size 100m;  # 录像及文件上传大小限制

        location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
        }

        location /media/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
        }

        location /static/ {
            root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        }

        location /koko/ {
            proxy_pass       http://localhost:5000;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /guacamole/ {
            proxy_pass       http://localhost:8081/;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /ws/ {
            proxy_pass http://localhost:8070;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

.. code-block:: shell

    # 保存后重新载入配置
    $ nginx -s reload

1.4.4 版本升级到最新版本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**请务必认真详细阅读每一个文字并理解后才能操作升级事宜**

- 当前版本必须是 1.4.4 版本, 否则请先升级到 1.4.4
- 从 1.4.5 版本开始, 由官方维护唯一 migrations
- 更新配置文件需要把对应旧版本的设置复制到新的配置文件

**JumpServer**

.. code-block:: shell

    $ cd /opt/jumpserver
    $ source /opt/py3/bin/activate
    $ ./jms stop

.. code-block:: shell

    # 备份 JumpServer
    $ cp -r /opt/jumpserver /opt/jumpserver_1.4.4_bak

.. code-block:: shell

    $ cd /opt/jumpserver
    $ git fetch
    $ git checkout master
    $ git pull
    $ git clean -df  # 清除未跟踪文件, 请一定要做好备份后再操作此步骤
    $ git reset --hard  # 还原所有修改, 请一定要做好备份后再操作此步骤
    $ git pull

    # 更新 config.yml, 请根据你原备份的 config.yml 内容进行修改
    $ mv config.py config_1.4.4.bak
    $ cp config_example.yml config.yml
    $ BOOTSTRAP_TOKEN=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`  # 生成随机 BOOTSTRAP_TOKEN
    $ sed -i "s/BOOTSTRAP_TOKEN:/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/jumpserver/config.yml
    $ echo "BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN" >> ~/.bashrc
    $ vi config.yml

.. code-block:: vim

    # SECURITY WARNING: keep the secret key used in production secret!
    # 加密秘钥 升级请保证与你原来的 SECRET_KEY 一致, 可以从旧版本的config_1.4.4.bak配置文件里面获取
    SECRET_KEY: *****

    # SECURITY WARNING: keep the bootstrap token used in production secret!
    # 预共享Token koko和guacamole用来注册服务账号, 不在使用原来的注册接受机制, 可随机生成
    BOOTSTRAP_TOKEN: *****

    # Development env open this, when error occur display the full process track, Production disable it
    # DEBUG 模式 开启DEBUG后遇到错误时可以看到更多日志
    DEBUG: false

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    # 日志级别
    LOG_LEVEL: ERROR
    # LOG_DIR:

    # Session expiration setting, Default 24 hour, Also set expired on on browser close
    # 浏览器Session过期时间, 默认24小时, 也可以设置浏览器关闭则过期
    # SESSION_COOKIE_AGE: 86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE: true

    # Database setting, Support sqlite3, mysql, postgres ....
    # 数据库设置
    # See https://docs.djangoproject.com/en/1.10/ref/settings/#databases

    # SQLite setting:
    # 使用单文件sqlite数据库
    # DB_ENGINE: sqlite3
    # DB_NAME:

    # MySQL or postgres setting like:
    # 使用Mysql作为数据库
    DB_ENGINE: mysql
    DB_HOST: 127.0.0.1
    DB_PORT: 3306
    DB_USER: jumpserver
    DB_PASSWORD: *****
    DB_NAME: jumpserver

    # When Django start it will bind this host and port
    # ./manage.py runserver 127.0.0.1:8080
    # 运行时绑定端口
    HTTP_BIND_HOST: 0.0.0.0
    HTTP_LISTEN_PORT: 8080

    # Use Redis as broker for celery and web socket
    # Redis配置
    REDIS_HOST: 127.0.0.1
    REDIS_PORT: 6379
    # REDIS_PASSWORD:
    # REDIS_DB_CELERY: 3
    # REDIS_DB_CACHE: 4

    # Use OpenID authorization
    # 使用OpenID 来进行认证设置
    # BASE_SITE_URL: http://localhost:8080
    # AUTH_OPENID: false  # True or False
    # AUTH_OPENID_SERVER_URL: https://openid-auth-server.com/
    # AUTH_OPENID_REALM_NAME: realm-name
    # AUTH_OPENID_CLIENT_ID: client-id
    # AUTH_OPENID_CLIENT_SECRET: client-secret

    # OTP settings
    # OTP/MFA 配置
    # OTP_VALID_WINDOW: 0
    # OTP_ISSUER_NAME: Jumpserver

.. code-block:: shell

    $ pip install wheel
    $ pip install --upgrade pip setuptools
    $ pip install -r requirements/requirements.txt
    $ cd utils
    $ vi 1.4.4_to_1.4.5_migrations.sh

.. code-block:: vim

    #!/bin/bash
    #

    host=127.0.0.1  # 修改成 JumpServer 数据库服务器IP
    port=3306  # 修改成 JumpServer 数据库服务器端口
    username=root  # 修改成有权限对数据库进行删改的用户
    db=jumpserver  # 修改成 JumpServer 数据库名称

    echo "备份原来的 migrations"
    mysqldump -u${username} -h${host} -P${port} -p ${db} django_migrations > django_migrations.sql.bak
    ret=$?

    if [ ${ret} == "0" ];then
        echo "开始使用新的migrations文件"
        mysql -u${username} -h${host} -P${port} -p ${db} < django_migrations.sql
    else
        echo "Not valid"
    fi

.. code-block:: shell

    $ sh 1.4.4_to_1.4.5_migrations.sh

    $ cd ../
    $ ./jms start -d

.. code-block:: nginx

    $ vi /etc/nginx/conf.d/jumpserver.conf  # 部分用户的配置文件是/etc/nginx/nginx.conf

    server {
        listen 80;

        client_max_body_size 100m;  # 录像及文件上传大小限制

        location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
        }

        location /media/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
        }

        location /static/ {
            root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        }

        location /koko/ {
            proxy_pass       http://localhost:5000;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /guacamole/ {
            proxy_pass       http://localhost:8081/;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /ws/ {
            proxy_pass http://localhost:8070;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

.. code-block:: shell

    # 保存后重新载入配置
    $ nginx -s reload

**Luna**

说明: 直接下载 release 包

.. code-block:: shell

    $ cd /opt
    $ rm -rf luna luna.tar.gz
    $ wget https://github.com/jumpserver/luna/releases/download/1.5.7/luna.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/luna/1.5.7/luna.tar.gz

    $ tar xf luna.tar.gz
    $ chown -R root:root luna

    # 注意把浏览器缓存清理下

**Koko**

.. code-block:: shell

    $ cd /opt
    $ wget https://github.com/jumpserver/koko/releases/download/1.5.7/koko-master-linux-amd64.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/koko/1.5.7/koko-master-linux-amd64.tar.gz

    $ tar xf koko-master-linux-amd64.tar.gz
    $ chown -R root:root kokodir
    $ cd kokodir
    $ cp config_example.yml config.yml
    $ sed -i "s/BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/kokodir/config.yml
    $ sed -i "s/# LOG_LEVEL: INFO/LOG_LEVEL: ERROR/g" /opt/kokodir/config.yml
    $ vim config.yml

    $ ./koko  # 后台运行可以使用 ./koko -d

docker 部署的 koko

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 koko 组件
    $ docker stop jms_koko
    $ docker rm jms_koko
    $ docker pull jumpserver/jms_koko:1.5.7
    $ docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> -e LOG_LEVEL=ERROR --restart=always jumpserver/jms_koko:<Tag>
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 -e LOG_LEVEL=ERROR --restart=always jumpserver/jms_koko:1.5.7

**Guacamole**

正常部署的 guacamole

.. code-block:: shell

    $ /etc/init.d/guacd stop
    $ sh /config/tomcat8/bin/shutdown.sh
    $ cd /opt/docker-guacamole
    $ git pull
    $ cd /config
    $ rm -rf /config/tomcat8

    # 访问 https://tomcat.apache.org/download-90.cgi 下载最新的 tomcat9
    $ wget http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-9/v9.0.33/bin/apache-tomcat-9.0.33.tar.gz
    $ tar xf apache-tomcat-9.0.33.tar.gz
    $ mv apache-tomcat-9.0.33 tomcat9
    $ rm -rf /config/tomcat9/webapps/*
    $ sed -i 's/Connector port="8080"/Connector port="8081"/g' /config/tomcat9/conf/server.xml
    $ echo "java.util.logging.ConsoleHandler.encoding = UTF-8" >> /config/tomcat9/conf/logging.properties
    $ ln -sf /opt/docker-guacamole/guacamole-1.0.0.war /config/tomcat9/webapps/ROOT.war
    $ ln -sf /opt/docker-guacamole/guacamole-auth-jumpserver-1.0.0.jar /config/guacamole/extensions/guacamole-auth-jumpserver-1.0.0.jar
    $ ln -sf /opt/docker-guacamole/root/app/guacamole/guacamole.properties /config/guacamole/guacamole.properties

    $ wget https://github.com/ibuler/ssh-forward/releases/download/v0.0.5/linux-amd64.tar.gz
    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/ssh-forward/v0.0.5/linux-amd64.tar.gz

    $ tar xf linux-amd64.tar.gz -C /bin/
    $ chmod +x /bin/ssh-forward

    # BOOTSTRAP_TOKEN 请和 jumpserver/config.yml 配置文件中保持一致
    $ export BOOTSTRAP_TOKEN=*****
    $ echo "export BOOTSTRAP_TOKEN=*****" >> ~/.bashrc

    $ /etc/init.d/guacd start
    $ sh /config/tomcat9/bin/startup.sh

docker 部署的 guacamole

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 guacamole 组件
    $ docker stop jms_guacamole
    $ docker rm jms_guacamole
    $ docker pull jumpserver/jms_guacamole:1.5.7

    $ docker run --name jms_guacamole -d -p 8081:8080 -e JUMPSERVER_SERVER=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:<Tag>
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_guacamole -d -p 8081:8080 -e JUMPSERVER_SERVER=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:1.5.7

到 Web 会话管理 - 终端管理 查看组件是否已经在线

1.4.5-1.4.7 升级到最新版本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**请务必认真详细阅读每一个文字并理解后才能操作升级事宜**

- 更新配置文件需要把对应旧版本的设置复制到新的配置文件

**JumpServer**

.. code-block:: shell

    $ cd /opt/jumpserver
    $ source /opt/py3/bin/activate
    $ ./jms stop
    $ cd /opt/jumpserver
    $ git pull

    # 更新 config.yml, 请根据你原来的 config.bak 内容进行修改
    $ mv config.py config_1.4.5.bak
    $ cp config_example.yml config.yml
    $ vi config.yml

.. code-block:: vim

    # SECURITY WARNING: keep the secret key used in production secret!
    # 加密秘钥 升级请保证与你原来的 SECRET_KEY 一致, 可以从旧版本的config_1.4.5.bak配置文件里面获取
    SECRET_KEY: *****

    # SECURITY WARNING: keep the bootstrap token used in production secret!
    # 预共享Token koko和guacamole用来注册服务账号, 不在使用原来的注册接受机制, 可随机生成
    BOOTSTRAP_TOKEN: *****

    # Development env open this, when error occur display the full process track, Production disable it
    # DEBUG 模式 开启DEBUG后遇到错误时可以看到更多日志
    DEBUG: false

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    # 日志级别
    LOG_LEVEL: ERROR
    # LOG_DIR:

    # Session expiration setting, Default 24 hour, Also set expired on on browser close
    # 浏览器Session过期时间, 默认24小时, 也可以设置浏览器关闭则过期
    # SESSION_COOKIE_AGE: 86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE: true

    # Database setting, Support sqlite3, mysql, postgres ....
    # 数据库设置
    # See https://docs.djangoproject.com/en/1.10/ref/settings/#databases

    # SQLite setting:
    # 使用单文件sqlite数据库
    # DB_ENGINE: sqlite3
    # DB_NAME:

    # MySQL or postgres setting like:
    # 使用Mysql作为数据库
    DB_ENGINE: mysql
    DB_HOST: 127.0.0.1
    DB_PORT: 3306
    DB_USER: jumpserver
    DB_PASSWORD: *****
    DB_NAME: jumpserver

    # When Django start it will bind this host and port
    # ./manage.py runserver 127.0.0.1:8080
    # 运行时绑定端口
    HTTP_BIND_HOST: 0.0.0.0
    HTTP_LISTEN_PORT: 8080

    # Use Redis as broker for celery and web socket
    # Redis配置
    REDIS_HOST: 127.0.0.1
    REDIS_PORT: 6379
    # REDIS_PASSWORD:
    # REDIS_DB_CELERY: 3
    # REDIS_DB_CACHE: 4

    # Use OpenID authorization
    # 使用OpenID 来进行认证设置
    # BASE_SITE_URL: http://localhost:8080
    # AUTH_OPENID: false  # True or False
    # AUTH_OPENID_SERVER_URL: https://openid-auth-server.com/
    # AUTH_OPENID_REALM_NAME: realm-name
    # AUTH_OPENID_CLIENT_ID: client-id
    # AUTH_OPENID_CLIENT_SECRET: client-secret

    # OTP settings
    # OTP/MFA 配置
    # OTP_VALID_WINDOW: 0
    # OTP_ISSUER_NAME: Jumpserver

.. code-block:: shell

    $ pip install wheel
    $ pip install --upgrade pip setuptools
    $ pip install -r requirements/requirements.txt
    $ ./jms start -d

.. code-block:: nginx

    $ vi /etc/nginx/conf.d/jumpserver.conf  # 部分用户的配置文件是/etc/nginx/nginx.conf

    server {
        listen 80;

        client_max_body_size 100m;  # 录像及文件上传大小限制

        location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
        }

        location /media/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
        }

        location /static/ {
            root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        }

        location /koko/ {
            proxy_pass       http://localhost:5000;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /guacamole/ {
            proxy_pass       http://localhost:8081/;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /ws/ {
            proxy_pass http://localhost:8070;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

.. code-block:: shell

    # 保存后重新载入配置
    $ nginx -s reload


**Luna**

说明: 直接下载 release 包

.. code-block:: shell

    $ cd /opt
    $ rm -rf luna luna.tar.gz
    $ wget https://github.com/jumpserver/luna/releases/download/1.5.7/luna.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/luna/1.5.7/luna.tar.gz

    $ tar xf luna.tar.gz
    $ chown -R root:root luna

    # 注意把浏览器缓存清理下

**Koko**

.. code-block:: shell

    $ cd /opt
    $ wget https://github.com/jumpserver/koko/releases/download/1.5.7/koko-master-linux-amd64.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/koko/1.5.7/koko-master-linux-amd64.tar.gz

    $ tar xf koko-master-linux-amd64.tar.gz
    $ chown -R root:root kokodir
    $ cd kokodir
    $ cp config_example.yml config.yml
    $ sed -i "s/BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/kokodir/config.yml
    $ sed -i "s/# LOG_LEVEL: INFO/LOG_LEVEL: ERROR/g" /opt/kokodir/config.yml
    $ vim config.yml

    $ ./koko  # 后台运行可以使用 ./koko -d

docker 部署的 koko

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 koko 组件
    $ docker stop jms_koko
    $ docker rm jms_koko
    $ docker pull jumpserver/jms_koko:1.5.7
    $ docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> -e LOG_LEVEL=ERROR --restart=always jumpserver/jms_koko:<Tag>
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 -e LOG_LEVEL=ERROR --restart=always jumpserver/jms_koko:1.5.7

**Guacamole**

正常部署的 guacamole

.. code-block:: shell

    $ /etc/init.d/guacd stop
    $ sh /config/tomcat8/bin/shutdown.sh
    $ cd /opt/docker-guacamole
    $ git pull
    $ cd /config
    $ rm -rf /config/tomcat8

    # 访问 https://tomcat.apache.org/download-90.cgi 下载最新的 tomcat9
    $ wget http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-9/v9.0.33/bin/apache-tomcat-9.0.33.tar.gz
    $ tar xf apache-tomcat-9.0.33.tar.gz
    $ mv apache-tomcat-9.0.33 tomcat9
    $ rm -rf /config/tomcat9/webapps/*
    $ sed -i 's/Connector port="8080"/Connector port="8081"/g' /config/tomcat9/conf/server.xml
    $ echo "java.util.logging.ConsoleHandler.encoding = UTF-8" >> /config/tomcat9/conf/logging.properties
    $ ln -sf /opt/docker-guacamole/guacamole-1.0.0.war /config/tomcat9/webapps/ROOT.war
    $ ln -sf /opt/docker-guacamole/guacamole-auth-jumpserver-1.0.0.jar /config/guacamole/extensions/guacamole-auth-jumpserver-1.0.0.jar
    $ ln -sf /opt/docker-guacamole/root/app/guacamole/guacamole.properties /config/guacamole/guacamole.properties

    $ wget https://github.com/ibuler/ssh-forward/releases/download/v0.0.5/linux-amd64.tar.gz
    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/ssh-forward/v0.0.5/linux-amd64.tar.gz

    $ tar xf linux-amd64.tar.gz -C /bin/
    $ chmod +x /bin/ssh-forward

    # BOOTSTRAP_TOKEN 请和 jumpserver/config.yml 配置文件中保持一致
    $ export BOOTSTRAP_TOKEN=*****
    $ echo "export BOOTSTRAP_TOKEN=*****" >> ~/.bashrc

    $ /etc/init.d/guacd start
    $ sh /config/tomcat9/bin/startup.sh

docker 部署的 guacamole

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 guacamole 组件
    $ docker stop jms_guacamole
    $ docker rm jms_guacamole
    $ docker pull jumpserver/jms_guacamole:1.5.7

    $ docker run --name jms_guacamole -d -p 8081:8080 -e JUMPSERVER_SERVER=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:1.5.7
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_guacamole -d -p 8081:8080 -e JUMPSERVER_SERVER=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:1.5.7

到 Web 会话管理 - 终端管理 查看组件是否已经在线

1.4.8-1.4.10 升级到最新版本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**JumpServer**

.. code-block:: shell

    $ cd /opt/jumpserver
    $ source /opt/py3/bin/activate
    $ ./jms stop
    $ git checkout master
    $ git pull
    $ pip install wheel
    $ pip install --upgrade pip setuptools
    $ pip install -r requirements/requirements.txt

    $ ./jms start -d

.. code-block:: nginx

    $ vi /etc/nginx/conf.d/jumpserver.conf  # 部分用户的配置文件是/etc/nginx/nginx.conf

    server {
        listen 80;

        client_max_body_size 100m;  # 录像及文件上传大小限制

        location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
        }

        location /media/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
        }

        location /static/ {
            root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        }

        location /koko/ {
            proxy_pass       http://localhost:5000;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /guacamole/ {
            proxy_pass       http://localhost:8081/;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /ws/ {
            proxy_pass http://localhost:8070;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

.. code-block:: shell

    # 保存后重新载入配置
    $ nginx -s reload

**Luna**

说明: 直接下载 release 包

.. code-block:: shell

    $ cd /opt
    $ rm -rf luna luna.tar.gz
    $ wget https://github.com/jumpserver/luna/releases/download/1.5.7/luna.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/luna/1.5.7/luna.tar.gz

    $ tar xf luna.tar.gz
    $ chown -R root:root luna

    # 注意把浏览器缓存清理下

**Koko**

.. code-block:: shell

    $ cd /opt
    $ wget https://github.com/jumpserver/koko/releases/download/1.5.7/koko-master-linux-amd64.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/koko/1.5.7/koko-master-linux-amd64.tar.gz

    $ tar xf koko-master-linux-amd64.tar.gz
    $ chown -R root:root kokodir
    $ cd kokodir
    $ cp config_example.yml config.yml
    $ sed -i "s/BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/kokodir/config.yml
    $ sed -i "s/# LOG_LEVEL: INFO/LOG_LEVEL: ERROR/g" /opt/kokodir/config.yml
    $ vim config.yml

    $ ./koko  # 后台运行可以使用 ./koko -d

docker 部署的 koko

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 koko 组件
    $ docker stop jms_koko
    $ docker rm jms_koko
    $ docker pull jumpserver/jms_koko:1.5.7
    $ docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> -e LOG_LEVEL=ERROR --restart=always jumpserver/jms_koko:<Tag>
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 -e LOG_LEVEL=ERROR --restart=always jumpserver/jms_koko:1.5.7

**Guacamole**

正常部署的 guacamole

.. code-block:: shell

    $ /etc/init.d/guacd stop
    $ sh /config/tomcat8/bin/shutdown.sh
    $ cd /opt/docker-guacamole
    $ git pull
    $ cd /config
    $ rm -rf /config/tomcat8

    # 访问 https://tomcat.apache.org/download-90.cgi 下载最新的 tomcat9
    $ wget http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-9/v9.0.33/bin/apache-tomcat-9.0.33.tar.gz
    $ tar xf apache-tomcat-9.0.33.tar.gz
    $ mv apache-tomcat-9.0.33 tomcat9
    $ rm -rf /config/tomcat9/webapps/*
    $ sed -i 's/Connector port="8080"/Connector port="8081"/g' /config/tomcat9/conf/server.xml
    $ echo "java.util.logging.ConsoleHandler.encoding = UTF-8" >> /config/tomcat9/conf/logging.properties
    $ ln -sf /opt/docker-guacamole/guacamole-1.0.0.war /config/tomcat9/webapps/ROOT.war
    $ ln -sf /opt/docker-guacamole/guacamole-auth-jumpserver-1.0.0.jar /config/guacamole/extensions/guacamole-auth-jumpserver-1.0.0.jar
    $ ln -sf /opt/docker-guacamole/root/app/guacamole/guacamole.properties /config/guacamole/guacamole.properties

    $ wget https://github.com/ibuler/ssh-forward/releases/download/v0.0.5/linux-amd64.tar.gz
    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/ssh-forward/v0.0.5/linux-amd64.tar.gz

    $ tar xf linux-amd64.tar.gz -C /bin/
    $ chmod +x /bin/ssh-forward

    # BOOTSTRAP_TOKEN 请和 jumpserver/config.yml 配置文件中保持一致
    $ export BOOTSTRAP_TOKEN=*****
    $ echo "export BOOTSTRAP_TOKEN=*****" >> ~/.bashrc

    $ /etc/init.d/guacd start
    $ sh /config/tomcat9/bin/startup.sh

docker 部署的 guacamole

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 guacamole 组件
    $ docker stop jms_guacamole
    $ docker rm jms_guacamole
    $ docker pull jumpserver/jms_guacamole:1.5.7

    $ docker run --name jms_guacamole -d -p 8081:8080 -e JUMPSERVER_SERVER=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:1.5.7
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_guacamole -d -p 8081:8080 -e JUMPSERVER_SERVER=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:1.5.7

到 Web 会话管理 - 终端管理 查看组件是否已经在线

1.5.0 及之后版本升级到最新版本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**JumpServer**

.. code-block:: shell

    $ cd /opt/jumpserver
    $ source /opt/py3/bin/activate
    $ ./jms stop
    $ git pull
    $ pip install wheel
    $ pip install --upgrade pip setuptools
    $ pip install -r requirements/requirements.txt

    $ ./jms start -d

.. code-block:: nginx

    $ vi /etc/nginx/conf.d/jumpserver.conf  # 部分用户的配置文件是/etc/nginx/nginx.conf

    server {
        listen 80;

        client_max_body_size 100m;  # 录像及文件上传大小限制

        location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
        }

        location /media/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
        }

        location /static/ {
            root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        }

        location /ws/ {
            proxy_pass http://localhost:8070;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /koko/ {
            proxy_pass       http://localhost:5000;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /guacamole/ {
            proxy_pass       http://localhost:8081/;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

.. code-block:: shell

    # 保存后重新载入配置
    $ nginx -s reload

**Luna**

说明: 直接下载 release 包

.. code-block:: shell

    $ cd /opt
    $ rm -rf luna luna.tar.gz
    $ wget https://github.com/jumpserver/luna/releases/download/1.5.7/luna.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/luna/1.5.7/luna.tar.gz

    $ tar xf luna.tar.gz
    $ chown -R root:root luna

    # 注意把浏览器缓存清理下

**Koko**

.. code-block:: shell

    $ cd /opt
    $ wget https://github.com/jumpserver/koko/releases/download/1.5.7/koko-master-linux-amd64.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/koko/1.5.7/koko-master-linux-amd64.tar.gz

    $ tar xf koko-master-linux-amd64.tar.gz
    $ chown -R root:root kokodir
    $ cd kokodir
    $ cp config_example.yml config.yml
    $ sed -i "s/BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/kokodir/config.yml
    $ sed -i "s/# LOG_LEVEL: INFO/LOG_LEVEL: ERROR/g" /opt/kokodir/config.yml
    $ vim config.yml

    $ ./koko  # 后台运行可以使用 ./koko -d

docker 部署的 koko

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 koko 组件
    $ docker stop jms_koko
    $ docker rm jms_koko
    $ docker pull jumpserver/jms_koko:1.5.7
    $ docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> -e LOG_LEVEL=ERROR --restart=always jumpserver/jms_koko:<Tag>
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 -e LOG_LEVEL=ERROR --restart=always jumpserver/jms_koko:1.5.7

**Guacamole**

正常部署的 guacamole

.. code-block:: shell

    $ /etc/init.d/guacd stop
    $ sh /config/tomcat8/bin/shutdown.sh
    $ cd /opt/docker-guacamole
    $ git pull
    $ cd /config
    $ rm -rf /config/tomcat8

    # 访问 https://tomcat.apache.org/download-90.cgi 下载最新的 tomcat9
    $ wget http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-9/v9.0.33/bin/apache-tomcat-9.0.33.tar.gz
    $ tar xf apache-tomcat-9.0.33.tar.gz
    $ mv apache-tomcat-9.0.33 tomcat9
    $ rm -rf /config/tomcat9/webapps/*
    $ sed -i 's/Connector port="8080"/Connector port="8081"/g' /config/tomcat9/conf/server.xml
    $ echo "java.util.logging.ConsoleHandler.encoding = UTF-8" >> /config/tomcat9/conf/logging.properties
    $ ln -sf /opt/docker-guacamole/guacamole-1.0.0.war /config/tomcat9/webapps/ROOT.war
    $ ln -sf /opt/docker-guacamole/guacamole-auth-jumpserver-1.0.0.jar /config/guacamole/extensions/guacamole-auth-jumpserver-1.0.0.jar
    $ ln -sf /opt/docker-guacamole/root/app/guacamole/guacamole.properties /config/guacamole/guacamole.properties

    $ /etc/init.d/guacd start
    $ sh /config/tomcat9/bin/startup.sh

docker 部署的 guacamole

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 guacamole 组件
    $ docker stop jms_guacamole
    $ docker rm jms_guacamole
    $ docker pull jumpserver/jms_guacamole:1.5.7

    $ docker run --name jms_guacamole -d -p 8081:8080 -e JUMPSERVER_SERVER=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:<Tag>
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_guacamole -d -p 8081:8080 -e JUMPSERVER_SERVER=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:1.5.7

到 Web 会话管理 - 终端管理 查看组件是否已经在线
