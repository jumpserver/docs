# Core 环境部署
## 1 Core 组件简述
!!! tip ""
    - [Core][core] 是 JumpServer 的核心组件，由 [Django][django] 二次开发而来，内置了 [Gunicorn][gunicorn] [Celery][celery] Beat [Flower][flower] [Daphne][daphne] 服务。

### 1.1 环境要求
!!! tip ""

    | Name    | Core                     | Python |
    | :------ | :----------------------- | :----- |
    | Version | {{ jumpserver.tag }}     | 3.9    |

### 1.2 下载源代码
!!! tip ""
    - 可以从 [Github][core] 网站上获取最新的 [Release][core_release] 副本。这些版本是最新代码的稳定快照，从项目网站下载的源将采用 .tar.gz 存档的形式，通过命令行中提取该存档：

!!! tip ""
    ```bash
    cd /opt
    mkdir /opt/jumpserver-{{ jumpserver.tag }}
    wget -O /opt/jumpserver-{{ jumpserver.tag }}.tar.gz https://github.com/jumpserver/jumpserver/archive/refs/tags/{{ jumpserver.tag }}.tar.gz
    tar -xf jumpserver-{{ jumpserver.tag }}.tar.gz -C /opt/jumpserver-{{ jumpserver.tag }} --strip-components 1
    cd jumpserver-{{ jumpserver.tag }}
    rm -f apps/common/utils/ip/geoip/GeoLite2-City.mmdb apps/common/utils/ip/ipip/ipipfree.ipdb
    wget https://download.jumpserver.org/files/ip/GeoLite2-City.mmdb -O apps/common/utils/ip/geoip/GeoLite2-City.mmdb
    wget https://download.jumpserver.org/files/ip/ipipfree.ipdb -O apps/common/utils/ip/ipip/ipipfree.ipdb
    ```

    ```bash
    ls -l requirements/
    ```
    ```vim
    requirements/           # 对应操作系统需要的依赖包
    ├── apk_pkg.sh          # Alpine
    ├── deb_pkg.sh          # 基于 Debian 的发行版(如: Ubuntu)
    ├── issues.txt          # macOS 一些问题及解决方案
    ├── mac_pkg.sh          # macOS
    ├── requirements.txt    # python
    └── rpm_pkg.sh          # 基于 RedHat 的发行版(如: CentOS)
    ```
!!! tip ""
    === "Ubuntu 20.04"
        ```bash
        apt-get install -y pkg-config libxmlsec1-dev libpq-dev libffi-dev libxml2 libxslt-dev libldap2-dev libsasl2-dev sshpass mariadb-client bash-completion g++ make sshpass
        ```

        !!! warning "如果你安装的是 MySQL, 将 mariadb 开发包自行替换成 mysql, 或者不要将 数据库 和 Core 部署在一起"
        ```bash
        apt-get install -y libmariadb-dev
        ```

### 1.3 安装 Python3
!!! tip ""
    - 从 [Python][python] 网站获取部署 Python3 的方法，请根据 [环境要求](#_3)，通过命令行中判断是否安装完成：

!!! tip ""
    ```bash
    apt-get install -y python3.9 python3.9-dev python3-venv
    ```
    ```bash
    python3.9
    ```
    ```python
    Python 3.9.5 (default, Nov 23 2021, 15:27:38)
    [GCC 9.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
    ```

### 1.4 安装 Python 依赖
!!! tip ""
    - 为 JumpServer 项目单独创建 python3 虚拟环境。

    ```bash
    python3.9 -m venv /opt/py3
    source /opt/py3/bin/activate
    ```

    - 每次运行项目都需要先执行 `source /opt/py3/bin/activate` 载入此环境。

    ```bash
    pip install -U pip setuptools wheel
    pip install -r requirements/requirements.txt
    ```

    - 修改配置文件。

    ```bash
    cp config_example.yml config.yml
    vi config.yml
    ```
    ```yaml
    # SECURITY WARNING: keep the secret key used in production secret!
    # 加密秘钥 生产环境中请修改为随机字符串，请勿外泄, 可使用命令生成
    # $ cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 48;echo
    SECRET_KEY: ****************  # 必填项, 长度推荐 50 位以上

    # SECURITY WARNING: keep the bootstrap token used in production secret!
    # 预共享Token koko 和 lion 用来注册服务账号，不在使用原来的注册接受机制
    # $ cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 24;echo
    BOOTSTRAP_TOKEN: ***********  # 必填项, 长度推荐 20 位以上

    # Development env open this, when error occur display the full process track, Production disable it
    # DEBUG 模式 开启DEBUG后遇到错误时可以看到更多日志
    DEBUG: true                   # 开发建议打开 DEBUG, 生产环境应该关闭

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    # 日志级别
    LOG_LEVEL: DEBUG              # 开发建议设置 DEBUG, 生产环境推荐使用 ERROR
    # LOG_DIR:

    # Session expiration setting, Default 24 hour, Also set expired on on browser close
    # 浏览器Session过期时间，默认24小时, 也可以设置浏览器关闭则过期
    # SESSION_COOKIE_AGE: 86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE: true  # 浏览器关闭 session 过期

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
    DB_HOST: 127.0.0.1       # 自行配置 数据库相关
    DB_PORT: 3306
    DB_USER: jumpserver
    DB_PASSWORD: ********
    DB_NAME: jumpserver

    # When Django start it will bind this host and port
    # ./manage.py runserver 127.0.0.1:8080
    # 运行时绑定端口, 将会使用 0.0.0.0:8080 0.0.0.0:8070 端口
    HTTP_BIND_HOST: 0.0.0.0
    HTTP_LISTEN_PORT: 8080
    WS_LISTEN_PORT: 8070

    # Use Redis as broker for celery and web socket
    # Redis配置
    REDIS_HOST: 127.0.0.1    # 自行配置 Redis 相关
    REDIS_PORT: 6379
    REDIS_PASSWORD: ********
    # REDIS_DB_CELERY: 3
    # REDIS_DB_CACHE: 4

    # Use OpenID Authorization
    # 使用 OpenID 进行认证设置
    # AUTH_OPENID: False # True or False
    # BASE_SITE_URL: None
    # AUTH_OPENID_CLIENT_ID: client-id
    # AUTH_OPENID_CLIENT_SECRET: client-secret
    # AUTH_OPENID_PROVIDER_ENDPOINT: https://op-example.com/
    # AUTH_OPENID_PROVIDER_AUTHORIZATION_ENDPOINT: https://op-example.com/authorize
    # AUTH_OPENID_PROVIDER_TOKEN_ENDPOINT: https://op-example.com/token
    # AUTH_OPENID_PROVIDER_JWKS_ENDPOINT: https://op-example.com/jwks
    # AUTH_OPENID_PROVIDER_USERINFO_ENDPOINT: https://op-example.com/userinfo
    # AUTH_OPENID_PROVIDER_END_SESSION_ENDPOINT: https://op-example.com/logout
    # AUTH_OPENID_PROVIDER_SIGNATURE_ALG: HS256
    # AUTH_OPENID_PROVIDER_SIGNATURE_KEY: None
    # AUTH_OPENID_SCOPES: "openid profile email"
    # AUTH_OPENID_ID_TOKEN_MAX_AGE: 60
    # AUTH_OPENID_ID_TOKEN_INCLUDE_CLAIMS: True
    # AUTH_OPENID_USE_STATE: True
    # AUTH_OPENID_USE_NONCE: True
    # AUTH_OPENID_SHARE_SESSION: True
    # AUTH_OPENID_IGNORE_SSL_VERIFICATION: True
    # AUTH_OPENID_ALWAYS_UPDATE_USER: True

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
    # PERM_SINGLE_ASSET_TO_UNGROUP_NODE: False
    #
    # 同一账号仅允许在一台设备登录
    # USER_LOGIN_SINGLE_MACHINE_ENABLED: False
    #
    # 启用定时任务
    # PERIOD_TASK_ENABLE: True
    #
    # 启用二次复合认证配置
    # LOGIN_CONFIRM_ENABLE: False
    #
    # Windows 登录跳过手动输入密码
    # WINDOWS_SKIP_ALL_MANUAL_PASSWORD: False
    ```

    - 处理国际化。

    ```bash
    rm -f apps/locale/zh/LC_MESSAGES/django.mo apps/locale/zh/LC_MESSAGES/djangojs.mo
    python apps/manage.py compilemessages
    ```  

### 1.5 启动 Core
!!! tip ""
    - 后台运行可以加 -d，`./jms start -d`

    ```bash
    ./jms start
    ```

[nginx]: http://nginx.org/
[lina]: https://github.com/jumpserver/lina/
[vue]: https://cn.vuejs.org/
[element_ui]: https://element.eleme.cn/
[luna]: https://github.com/jumpserver/luna/
[angular_cli]: https://github.com/angular/angular-cli
[core]: https://github.com/jumpserver/jumpserver/
[django]: https://docs.djangoproject.com/
[gunicorn]: https://gunicorn.org/
[celery]: https://docs.celeryproject.org/
[flower]: https://github.com/mher/flower/
[daphne]: https://github.com/django/daphne/
[github]: https://github.com/
[core_release]: https://github.com/jumpserver/jumpserver/releases/tag/{{ jumpserver.tag }}
[python]: https://www.python.org/downloads/
[linux_packages]: http://nginx.org/en/linux_packages.html
[lina_release]: https://github.com/jumpserver/lina/releases/tag/{{ jumpserver.tag }}
[node]: https://nodejs.org/
[luna_release]: https://github.com/jumpserver/luna/releases/tag/{{ jumpserver.tag }}
[koko_release]: https://github.com/jumpserver/koko/releases/tag/{{ jumpserver.tag }}
[go]: https://golang.google.cn/
[koko]: https://github.com/jumpserver/koko
[koko_release]: https://github.com/jumpserver/koko/releases/tag/{{ jumpserver.tag }}
[lion]: https://github.com/jumpserver/lion-release
[lion_release]: https://github.com/jumpserver/lion-release/releases/tag/{{ jumpserver.tag }}
[guacamole]: http://guacamole.apache.org/
[apache]: http://www.apache.org/
[guacamole-server]: https://github.com/apache/guacamole-server
[building-guacamole-server]: http://guacamole.apache.org/doc/gug/installing-guacamole.html#building-guacamole-server
[guacd-1.4.0]: http://download.jumpserver.org/public/guacamole-server-1.4.0.tar.gz
[wisp]: https://github.com/jumpserver/wisp
[wisp_release]: https://github.com/jumpserver/wisp/releases/tag/{{ jumpserver.wisp }}
[magnus]: https://github.com/jumpserver/magnus-release
[magnus_release]: https://github.com/jumpserver/magnus-release/releases/tag/{{ jumpserver.tag }}
[lina-{{ jumpserver.tag }}]: https://github.com/jumpserver/lina/releases/download/{{ jumpserver.tag }}/lina-{{ jumpserver.tag }}.tar.gz
[luna-{{ jumpserver.tag }}]: https://github.com/jumpserver/luna/releases/download/{{ jumpserver.tag }}/luna-{{ jumpserver.tag }}.tar.gz
[koko-{{ jumpserver.tag }}-linux-amd64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-linux-amd64.tar.gz
[koko-{{ jumpserver.tag }}-linux-arm64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-linux-arm64.tar.gz
[koko-{{ jumpserver.tag }}-linux-loong64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-linux-loong64.tar.gz
[koko-{{ jumpserver.tag }}-darwin-amd64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-darwin-amd64.tar.gz
[koko-{{ jumpserver.tag }}-darwin-arm64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-darwin-arm64.tar.gz
[lion-{{ jumpserver.tag }}-linux-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-linux-amd64.tar.gz
[lion-{{ jumpserver.tag }}-linux-arm64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-linux-arm64.tar.gz
[lion-{{ jumpserver.tag }}-linux-loong64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-linux-loong64.tar.gz
[lion-{{ jumpserver.tag }}-darwin-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-darwin-amd64.tar.gz
[lion-{{ jumpserver.tag }}-windows-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-windows-amd64.tar.gz
[magnus-{{ jumpserver.tag }}-linux-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-amd64.tar.gz
[magnus-{{ jumpserver.tag }}-linux-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-arm64.tar.gz
[magnus-{{ jumpserver.tag }}-linux-loong64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-loong64.tar.gz
[magnus-{{ jumpserver.tag }}-darwin-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-darwin-amd64.tar.gz
[magnus-{{ jumpserver.tag }}-darwin-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-darwin-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-amd64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-arm64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-loong64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-loong64.tar.gz
[wisp-{{ jumpserver.wisp }}-darwin-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-darwin-amd64.tar.gz
[wisp-{{ jumpserver.wisp }}-darwin-arm64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-darwin-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-windows-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-windows-amd64.tar.gz
