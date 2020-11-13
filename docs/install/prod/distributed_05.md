# Core 部署

## 环境

!!! tip ""
    - 系统: CentOS 7
    - IP: 192.168.100.30

    ```
    +----------+------------+-----------------+---------------+-------------------------+
    | Protocol | ServerName |        IP       |      Port     |         Used By         |
    +==========+============+=================+===============+=========================+
    |    TCP   |    Core    | 192.168.100.30  |   8070,8080   |         Tengine         |
    +----------+------------+-----------------+---------------+-------------------------+
    |    TCP   |    Core    | 192.168.100.31  |   8070,8080   |         Tengine         |
    +----------+------------+-----------------+---------------+-------------------------+
    ```

## 安装步骤

### 1. 安装 epel 库

!!! tip ""
    ```sh
    yum upgrade -y
    yum -y install epel-release wget
    ```

### 2. 配置防火墙

!!! tip ""
    ```sh
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="8080" accept"
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="8070" accept"
    firewall-cmd --reload
    setsebool -P httpd_can_network_connect 1
    ```

!!! tip "192.168.100.100 为 tengine 服务器 ip, 请根据实际情况修改"

### 3. 安装 git

!!! tip ""
    ```sh
    yum -y install gcc git
    ```

### 4. 安装 python3.6

!!! tip ""
    ```sh
    yum -y install python36 python36-devel
    ```

### 5. 配置 py3 虚拟环境

!!! tip ""
    ```sh
    python3.6 -m venv /opt/py3
    source /opt/py3/bin/activate
    ```

### 6. 下载 core

!!! tip ""
    ```sh
    cd /opt && \
    wget https://github.com/jumpserver/jumpserver/releases/download/v2.4.4/jumpserver-v2.4.4.tar.gz
    ```
    ```sh
    tar xf jumpserver-v2.4.4.tar.gz
    mv jumpserver-v2.4.4 jumpserver
    ```

### 7. 安装 rpm 依赖包

!!! tip ""
    ```sh
    yum -y install $(cat /opt/jumpserver/requirements/rpm_requirements.txt)
    ```

### 8. 安装 python 依赖

!!! tip ""
    ```sh
    pip install wheel
    pip install --upgrade pip setuptools
    pip install -r /opt/jumpserver/requirements/requirements.txt
    ```

### 9. 修改配置文件

!!! tip ""
    ```sh
    cd /opt/jumpserver
    ```

    ```sh
    cp config_example.yml config.yml
    ```

    ```sh
    SECRET_KEY=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 50`
    echo "SECRET_KEY=$SECRET_KEY" >> ~/.bashrc
    BOOTSTRAP_TOKEN=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`
    echo "BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN" >> ~/.bashrc
    ```

    ```sh
    sed -i "s/SECRET_KEY:/SECRET_KEY: $SECRET_KEY/g" /opt/jumpserver/config.yml
    sed -i "s/BOOTSTRAP_TOKEN:/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/jumpserver/config.yml
    sed -i "s/# DEBUG: true/DEBUG: false/g" /opt/jumpserver/config.yml
    sed -i "s/# LOG_LEVEL: DEBUG/LOG_LEVEL: ERROR/g" /opt/jumpserver/config.yml
    sed -i "s/# SESSION_EXPIRE_AT_BROWSER_CLOSE: false/SESSION_EXPIRE_AT_BROWSER_CLOSE: true/g" /opt/jumpserver/config.yml
    ```

    ```sh
    echo -e "\033[31m 你的SECRET_KEY是 $SECRET_KEY \033[0m"
    echo -e "\033[31m 你的BOOTSTRAP_TOKEN是 $BOOTSTRAP_TOKEN \033[0m"
    ```

    ```sh
    vi config.yml
    ```

??? info "注意不能使用纯数字字符串, BOOTSTRAP_TOKEN 给其他组件使用, redis 信息要给 koko 使用"
    以下模板仅供参考  
    ```yaml
    # SECURITY WARNING: keep the secret key used in production secret!
    # 加密秘钥 生产环境中请修改为随机字符串，请勿外泄, 可使用命令生成
    # cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 49;echo
    SECRET_KEY: W5Ic3fMXNZ0p5RIy5DhJYJllppTfcfkW8Yuf94VBMfpcssbfu

    # SECURITY WARNING: keep the bootstrap token used in production secret!
    # 预共享Token coco和guacamole用来注册服务账号，不在使用原来的注册接受机制
    BOOTSTRAP_TOKEN: zxffNymGjP79j6BN

    # Development env open this, when error occur display the full process track, Production disable it
    # DEBUG 模式 开启DEBUG后遇到错误时可以看到更多日志
    DEBUG: false

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    # 日志级别
    LOG_LEVEL: ERROR
    # LOG_DIR:

    # Session expiration setting, Default 24 hour, Also set expired on on browser close
    # 浏览器Session过期时间，默认24小时, 也可以设置浏览器关闭则过期
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
    WS_LISTEN_PORT: 8070

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
    # AUTH_OPENID_IGNORE_SSL_VERIFICATION: True
    # AUTH_OPENID_SHARE_SESSION: True

    # Use Radius authorization
    # 使用Radius来认证
    # AUTH_RADIUS: false
    # RADIUS_SERVER: localhost
    # RADIUS_PORT: 1812
    # RADIUS_SECRET:

    # CAS 配置
    # AUTH_CAS': False,
    # CAS_SERVER_URL': "http://host/cas/",
    # CAS_ROOT_PROXIED_AS': 'http://jumpserver-host:port',  
    # CAS_LOGOUT_COMPLETELY': True,
    # CAS_VERSION': 3,

    # LDAP/AD settings
    # LDAP 搜索分页数量
    # AUTH_LDAP_SEARCH_PAGED_SIZE: 1000
    #
    # 定时同步用户
    # 启用 / 禁用
    # AUTH_LDAP_SYNC_IS_PERIODIC: True
    # 同步间隔 (单位: 时) (优先）
    # AUTH_LDAP_SYNC_INTERVAL: 12
    # Crontab 表达式
    # AUTH_LDAP_SYNC_CRONTAB: * 6 * * *
    #
    # LDAP 用户登录时仅允许在用户列表中的用户执行 LDAP Server 认证
    # AUTH_LDAP_USER_LOGIN_ONLY_IN_USERS: False
    #
    # LDAP 认证时如果日志中出现以下信息将参数设置为 0 (详情参见：https://www.python-ldap.org/en/latest/faq.html)
    # In order to perform this operation a successful bind must be completed on the connection
    # AUTH_LDAP_OPTIONS_OPT_REFERRALS: -1

    # OTP settings
    # OTP/MFA 配置
    # OTP_VALID_WINDOW: 0
    # OTP_ISSUER_NAME: Jumpserver

    # Perm show single asset to ungrouped node
    # 是否把未授权节点资产放入到 未分组 节点中
    # PERM_SINGLE_ASSET_TO_UNGROUP_NODE: false
    #
    # 启用定时任务
    # PERIOD_TASK_ENABLE: True
    #
    # 启用二次复合认证配置
    # LOGIN_CONFIRM_ENABLE: False
    #
    # Windows 登录跳过手动输入密码
    WINDOWS_SKIP_ALL_MANUAL_PASSWORD: True
    ```

### 10. 挂载 nfs

!!! tip ""
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.99
    mount -t nfs 192.168.100.99:/data /opt/jumpserver/data
    ```

!!! warning "192.168.100.99 为 nfs 服务器 ip, 请根据实际情况更改"

!!! tip ""
    ```sh
    vi /etc/fstab
    ```
    ```vim
    192.168.100.99:/data /opt/jumpserver/data nfs defaults 0 0
    ```


### 11. 运行 core

!!! tip ""
    ```sh
    cd /opt/jumpserver
    ./jms start -d
    ```

## 多节点部署

!!! info "多节点部署与上面一致, config.yml 不需要重新生成, 直接复制主节点的配置文件即可"

- 登录到新的节点服务器

!!! tip ""
    ```sh
    yum upgrade -y
    yum -y install gcc epel-release git
    yum -y install python36 python36-devel
    python3.6 -m venv /opt/py3
    source /opt/py3/bin/activate
    wget https://github.com/jumpserver/jumpserver/releases/download/v2.4.4/jumpserver-v2.4.4.tar.gz
    tar xf jumpserver-v2.4.4.tar.gz
    mv jumpserver-v2.4.4 jumpserver
    yum -y install $(cat /opt/jumpserver/requirements/rpm_requirements.txt)
    pip install wheel
    pip install --upgrade pip setuptools
    pip install -r /opt/jumpserver/requirements/requirements.txt
    ```

- 复制主节点 config.yml 到 /opt/jumpserver

!!! tip ""
    ```sh
    scp root@192.168.100.30:/opt/jumpserver/config.yml /opt/jumpserver
    ```

!!! info "192.168.100.30 为主 core 服务器 ip，按照提示输入密码"

- 配置 nfs

!!! tip ""
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.99
    mount -t nfs 192.168.100.99:/data /opt/jumpserver/data
    echo "192.168.100.99:/data /opt/jumpserver/data nfs defaults 0 0" >> /etc/fstab
    ```

!!! info "192.168.100.99 为 nfs 服务器"

- 启动 core

!!! tip ""
    ```sh
    cd /opt/jumpserver
    ./jms start -d
    ```

- 复制主节点的 jumpserver.conf 到当前节点

!!! tip ""
    ```sh
    scp root@192.168.100.30:/etc/nginx/conf.d/jumpserver.conf /etc/nginx/conf.d/
    ```

!!! tip "192.168.100.30 为主 core 服务器 ip，按照提示输入密码"
