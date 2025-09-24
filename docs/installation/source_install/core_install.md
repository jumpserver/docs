# Core 环境搭建
## 1 Core 组件概述
!!! tip ""
    - [Core][core] 是 JumpServer 的核心组件，由 [Django][django] 二次开发而来，内置了 [Gunicorn][gunicorn] [Celery][celery] Beat [Flower][flower] [Daphne][daphne] 服务。

### 1.1 环境要求
!!! tip ""

    | Name    | Core                     | Python |
    | :------ | :----------------------- | :----- |
    | Version | {{ jumpserver.tag }}     | 3.11   |

### 1.2 克隆源代码仓库
!!! tip ""
    - 可以从 [Github][core] 网站上获取最新的源代码 。这些版本是最新代码，通过命令行中提取该文件：

!!! tip ""
    ```bash
    cd /opt
    git clone https://github.com/jumpserver/jumpserver.git
    cd jumpserver
    ```

    ```bash
    ls -l requirements/
    bash static_files.sh
    bash apk_pkg.sh # 根据自己的 Linux 发行版选择对应的脚本
    ```
    ```vim
    requirements/           # 对应操作系统需要的依赖包
    ├── apk_pkg.sh          # Alpine Linux 依赖安装脚本
    ├── clean_site_packages.sh  # 清理 Python site-packages 的脚本
    ├── collections.yml      # Ansible 集合配置文件
    ├── deb_pkg.sh           # 基于 Debian 的发行版(如: Ubuntu)依赖安装脚本
    ├── issue.md            # 常见问题及解决方案文档
    ├── mac_pkg.sh           # macOS 依赖安装脚本
    ├── rpm_pkg.sh           # 基于 RedHat 的发行版(如: CentOS)依赖安装脚本
    └── static_files.sh      # 静态文件处理脚本

    ```

    === "Ubuntu 22.04"
            ```bash
            sudo apt update && sudo apt upgrade -y
            sudo apt install -y ca-certificates wget g++ make pkg-config default-libmysqlclient-dev freetds-dev gettext libkrb5-dev libldap2-dev libsasl2-dev cron openssh-client sshpass nmap bubblewrap libx11-dev 
            ```

!!! warning "如果你使用的是 MySQL 数据库，确保安装的是 MySQL 的开发包，而不是 MariaDB 的开发包，或者建议将数据库和 Core 服务部署在不同的主机上。"
    ```bash
    apt-get install -y libmysqlclient-dev
    ```

### 1.3 安装 Python3
!!! tip ""
    - 从 [Python][python] 网站获取部署 Python3 的方法，请根据 [环境要求](#_3)，通过命令行中判断是否安装完成：

!!! tip ""
    ```bash
    apt-get install -y python3.11 python3.11-dev python3.11-venv python3-pip
    ```
    ```bash
    python3.11
    ```
    ```python
    Python 3.11.0rc1 (main, Aug 12 2022, 10:02:14) [GCC 11.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 
    ```

### 1.4 安装 Python 依赖 (通过 uv)
!!! tip ""
    - 为 JumpServer 项目单独创建 python3 虚拟环境。

    ```bash
    python3.11 -m venv /opt/py3
    source /opt/py3/bin/activate
    ```

    - 每次运行项目都需要先执行 `source /opt/py3/bin/activate` 载入此环境。

    ```bash
    uv pip install -r pyproject.toml
    ```

    - 修改配置文件。

    ```bash
    cp config_example.yml config.yml
    vi config.yml
    ```
    ```yaml
    # SECURITY WARNING: keep the secret key used in production secret!
    # 加密密钥 生产环境中请修改为随机字符串，请勿外泄, 可使用命令生成
    # $ cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 49;echo
    SECRET_KEY:

    # SECURITY WARNING: keep the bootstrap token used in production secret!
    # 预共享Token coco和guacamole用来注册服务账号，不在使用原来的注册接受机制
    BOOTSTRAP_TOKEN:

    # Development env open this, when error occur display the full process track, Production disable it
    # DEBUG 模式 开启DEBUG后遇到错误时可以看到更多日志
    # DEBUG: true

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    # 日志级别
    # LOG_LEVEL: DEBUG
    # LOG_DIR:

    # Session expiration setting, Default 1 hour, Also set expired on on browser close
    # 浏览器Session过期时间，默认 1 小时, 也可以设置浏览器关闭则过期
    # SESSION_COOKIE_AGE: 3600
    # SESSION_EXPIRE_AT_BROWSER_CLOSE: false

    # Database setting, Support sqlite3, mysql, postgres ....
    # 数据库设置
    # See https://docs.djangoproject.com/en/1.10/ref/settings/#databases

    # SQLite setting:
    # 使用单文件sqlite数据库
    # DB_ENGINE: sqlite3
    # DB_NAME:
    # MySQL or postgres setting like:
    # 使用 PostgreSQL 作为数据库
    DB_ENGINE: postgresql
    DB_HOST: 127.0.0.1
    DB_PORT: 5432
    DB_USER: jumpserver
    DB_PASSWORD:
    DB_NAME: jumpserver

    # When Django start it will bind this host and port
    # ./manage.py runserver 127.0.0.1:8080
    # 运行时绑定端口
    HTTP_BIND_HOST: 0.0.0.0
    HTTP_LISTEN_PORT: 8080
    WS_LISTEN_PORT: 8070

    # Use Redis as broker for celery and web socket
    # Redis配置
    REDIS_HOST: 127.0.0.1
    REDIS_PORT: 6379
    # REDIS_PASSWORD:
    # REDIS_DB_CELERY: 3
    # REDIS_DB_CACHE: 4

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
    # OTP_ISSUER_NAME: JumpServer

    # 启用定时任务
    # PERIOD_TASK_ENABLED: True
    #

    # 是否开启 Luna 水印
    # SECURITY_WATERMARK_ENABLED: False

    # 浏览器关闭页面后，会话过期
    # SESSION_EXPIRE_AT_BROWSER_CLOSE: False

    # 每次 api 请求，session 续期
    # SESSION_SAVE_EVERY_REQUEST: True

    # 仅允许用户从来源处登录
    # ONLY_ALLOW_AUTH_FROM_SOURCE: False

    # 仅允许已存在的用户登录，不允许第三方认证后，自动创建用户
    # ONLY_ALLOW_EXIST_USER_AUTH: False

    # 开启人脸识别 XPACK 功能
    #FACE_RECOGNITION_ENABLED: true
    #FACE_RECOGNITION_DISTANCE_THRESHOLD': 0.35
    #FACE_RECOGNITION_COSINE_THRESHOLD': 0.95
    ```

    - 编译翻译文件。

    ```bash
    cd apps
    python manage.py compilemessages
    cd ..
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
[core_release]: https://github.com/jumpserver/jumpserver
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
