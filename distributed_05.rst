分布式部署文档 - Core 部署
----------------------------------------------------

说明
~~~~~~~
-  # 开头的行表示注释
-  $ 开头的行表示需要执行的命令

环境
~~~~~~~

-  系统: CentOS 7
-  IP: 192.168.100.30

+----------+------------+-----------------+---------------+-------------------------+
| Protocol | ServerName |        IP       |      Port     |         Used By         |
+==========+============+=================+===============+=========================+
|    TCP   | JumpServer | 192.168.100.30  |       80      |         Tengine         |
+----------+------------+-----------------+---------------+-------------------------+
|    TCP   | JumpServer | 192.168.100.31  |       80      |         Tengine         |
+----------+------------+-----------------+---------------+-------------------------+

开始安装
~~~~~~~~~~~~

.. code-block:: shell

    # 升级系统
    $ yum upgrade -y

    # 安装依赖包
    $ yum -y install gcc epel-release git

    # 开放 80 给 tengine 访问
    $ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="80" accept"
    $ firewall-cmd --reload
    $ setsebool -P httpd_can_network_connect 1

    # 安装 Python3.6
    $ yum -y install python36 python36-devel

    # 配置 py3 虚拟环境
    $ python3.6 -m venv /opt/py3
    $ source /opt/py3/bin/activate

    # 下载 JumpServer
    $ cd /opt
    $ git clone --depth=1 https://github.com/jumpserver/jumpserver.git

    # 安装依赖 RPM 包
    $ yum -y install $(cat /opt/jumpserver/requirements/rpm_requirements.txt)

    # 安装 Python 库依赖
    $ pip install wheel
    $ pip install --upgrade pip setuptools
    $ pip install -r /opt/jumpserver/requirements/requirements.txt

    # 修改 jumpserver 配置文件
    $ cd /opt/jumpserver
    $ cp config_example.yml config.yml

    $ SECRET_KEY=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 50`  # 生成随机SECRET_KEY
    $ echo "SECRET_KEY=$SECRET_KEY" >> ~/.bashrc
    $ BOOTSTRAP_TOKEN=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`  # 生成随机BOOTSTRAP_TOKEN
    $ echo "BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN" >> ~/.bashrc

    $ sed -i "s/SECRET_KEY:/SECRET_KEY: $SECRET_KEY/g" /opt/jumpserver/config.yml
    $ sed -i "s/BOOTSTRAP_TOKEN:/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/jumpserver/config.yml
    $ sed -i "s/# DEBUG: true/DEBUG: false/g" /opt/jumpserver/config.yml
    $ sed -i "s/# LOG_LEVEL: DEBUG/LOG_LEVEL: ERROR/g" /opt/jumpserver/config.yml
    $ sed -i "s/# SESSION_EXPIRE_AT_BROWSER_CLOSE: false/SESSION_EXPIRE_AT_BROWSER_CLOSE: true/g" /opt/jumpserver/config.yml

    $ echo -e "\033[31m 你的SECRET_KEY是 $SECRET_KEY \033[0m"
    $ echo -e "\033[31m 你的BOOTSTRAP_TOKEN是 $BOOTSTRAP_TOKEN \033[0m"

    $ vi config.yml  # 主节点编辑好此配置文件后, 其他节点之间复制过去使用

.. code-block:: yaml

    # SECURITY WARNING: keep the secret key used in production secret!
    # 加密秘钥 生产环境中请修改为随机字符串, 请勿外泄, 升级或者迁移请保持不变
    SECRET_KEY:

    # SECURITY WARNING: keep the bootstrap token used in production secret!
    # 预共享Token koko和guacamole用来注册服务账号, 不在使用原来的注册接受机制
    BOOTSTRAP_TOKEN:

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
    DB_HOST: 192.168.100.10
    DB_PORT: 3306
    DB_USER: jumpserver
    DB_PASSWORD: weakPassword
    DB_NAME: jumpserver

    # When Django start it will bind this host and port
    # ./manage.py runserver 127.0.0.1:8080
    # 运行时绑定端口
    HTTP_BIND_HOST: 0.0.0.0
    HTTP_LISTEN_PORT: 8080

    # Use Redis as broker for celery and web socket
    # Redis配置
    REDIS_HOST: 192.168.100.20
    REDIS_PORT: 6379
    REDIS_PASSWORD: weakPassword
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
    # OTP_ISSUER_NAME: JumpServer

.. code-block:: shell

    # 挂载 NFS 共享文件夹
    $ yum -y install nfs-utils
    $ showmount -e 192.168.100.99  # 连接 NFS 服务器检查
    $ mount -t nfs 192.168.100.99:/data /opt/jumpserver/data  # 挂载到 jumpserver/data

.. code-block:: vim

    # 写入自启
    $ vi /etc/fstab

    192.168.100.99:/data /opt/jumpserver/data nfs defaults 0 0

.. code-block:: shell

    # 运行 JumpServer
    $ cd /opt/jumpserver
    $ ./jms start -d  # 后台运行使用 -d 参数./jms start -d
    # 新版本更新了运行脚本, 使用方式./jms start|stop|status all  后台运行请添加 -d 参数

    # 部署 Nginx 反向代理
    $ vi /etc/yum.repos.d/nginx.repo

    [nginx]
    name=nginx repo
    baseurl=http://nginx.org/packages/centos/7/$basearch/
    gpgcheck=0
    enabled=1

    $ yum -y install nginx
    $ systemctl enable nginx

    # 配置 Nginx 整合各组件
    $ echo > /etc/nginx/conf.d/default.conf

.. code-block:: shell

    $ vi /etc/nginx/conf.d/jumpserver.conf

    server {
        listen 80;

        client_max_body_size 100m;  # 录像及文件上传大小限制

        location /media/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
        }

        location /static/ {
            root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        }

        location /ws/ {
            proxy_pass http://localhost:8070;
            proxy_http_version 1.1;
            proxy_buffering off;
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
            access_log off;
        }
    }

.. code-block:: shell

    # 运行 Nginx
    $ nginx -t   # 确保配置没有问题, 有问题请先解决
    $ systemctl start nginx

多节点部署
~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # 多节点部署与上面一致, config.yml 不需要重新生成, 直接复制主节点的配置文件即可
    # 登录到新的节点服务器
    $ yum upgrade -y
    $ yum -y install gcc epel-release git
    $ yum -y install python36 python36-devel
    $ python3.6 -m venv /opt/py3
    $ source /opt/py3/bin/activate
    $ git clone --depth=1 https://github.com/jumpserver/jumpserver.git
    $ yum -y install $(cat /opt/jumpserver/requirements/rpm_requirements.txt)
    $ pip install wheel
    $ pip install --upgrade pip setuptools
    $ pip install -r /opt/jumpserver/requirements/requirements.txt

    # 到此, 复制主节点 config.yml 到 /opt/jumpserver
    $ scp root@192.168.100.30:/opt/jumpserver/config.yml /opt/jumpserver
    # 输入密码即可

    $ yum -y install nfs-utils
    $ showmount -e 192.168.100.99
    $ mount -t nfs 192.168.100.99:/data /opt/jumpserver/data
    $ echo "192.168.100.99:/data /opt/jumpserver/data nfs defaults 0 0" >> /etc/fstab

    $ cd /opt/jumpserver
    $ ./jms start -d

    $ echo -e "[nginx-stable]\nname=nginx stable repo\nbaseurl=http://nginx.org/packages/centos/\$releasever/\$basearch/\ngpgcheck=1\nenabled=1\ngpgkey=https://nginx.org/keys/nginx_signing.key" > /etc/yum.repos.d/nginx.repo
    $ rpm --import https://nginx.org/keys/nginx_signing.key
    $ yum -y install nginx
    $ systemctl enable nginx

    $ echo > /etc/nginx/conf.d/default.conf
    # 复制主节点的 jumpserver.conf 到当前节点
    $ scp root@192.168.100.30:/etc/nginx/conf.d/jumpserver.conf /etc/nginx/conf.d/

    # 运行 Nginx
    $ nginx -t   # 确保配置没有问题, 有问题请先解决
    $ systemctl start nginx
