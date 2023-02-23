# Magnus 环境部署
## 1 Magnus 环境部署
### 1.1 环境要求
!!! tip ""
    - 可以从 [Github][magnus] 网站上获取最新的 [Release][magnus_release] 副本。

    | 操作系统      | 架构类型    | 名称                                                                                                  |
    | :------ | :------ | :---------------------------------------------------------------------------------------------------- |
    | Linux   | amd64   | [magnus-{{ jumpserver.version }}-linux-amd64.tar.gz][magnus-{{ jumpserver.version }}-linux-amd64]     |
    | Linux   | arm64   | [magnus-{{ jumpserver.version }}-linux-arm64.tar.gz][magnus-{{ jumpserver.version }}-linux-arm64]     |
    | Linux   | loong64 | [magnus-{{ jumpserver.version }}-linux-loong64.tar.gz][magnus-{{ jumpserver.version }}-linux-loong64] |
    | Darwin  | amd64   | [magnus-{{ jumpserver.version }}-darwin-amd64.tar.gz][magnus-{{ jumpserver.version }}-darwin-amd64]   |
    | Darwin  | arm64   | [magnus-{{ jumpserver.version }}-darwin-arm64.tar.gz][magnus-{{ jumpserver.version }}-darwin-arm64]   |

!!! tip ""
    - Magnus 需要使用 Wisp 与 JumpServer 通信，从 [Github][wisp] 网站上获取最新的 [Release][wisp_release] 副本。

    | 操作系统      | 架构类型    | 名称                                                                                        |
    | :------ | :------ | :------------------------------------------------------------------------------------------ |
    | Linux   | amd64   | [wisp-{{ jumpserver.wisp }}-linux-amd64.tar.gz][wisp-{{ jumpserver.wisp }}-linux-amd64]     |
    | Linux   | arm64   | [wisp-{{ jumpserver.wisp }}-linux-arm64.tar.gz][wisp-{{ jumpserver.wisp }}-linux-arm64]     |
    | Linux   | loong64 | [wisp-{{ jumpserver.wisp }}-linux-loong64.tar.gz][wisp-{{ jumpserver.wisp }}-linux-loong64] |
    | Darwin  | amd64   | [wisp-{{ jumpserver.wisp }}-darwin-amd64.tar.gz][wisp-{{ jumpserver.wisp }}-darwin-amd64]   |
    | Darwin  | arm64   | [wisp-{{ jumpserver.wisp }}-darwin-arm64.tar.gz][wisp-{{ jumpserver.wisp }}-darwin-arm64]   |
    | Windows | amd64   | [wisp-{{ jumpserver.wisp }}-windows-amd64.tar.gz][wisp-{{ jumpserver.wisp }}-windows-amd64] |

### 1.2 选择部署方式
!!! tip ""
    === "Linux/amd64"
    
        - 解压缩包。
    
        ```bash
        cd /opt
        wget https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-linux-amd64.tar.gz
        tar -xf magnus-{{ jumpserver.version }}-linux-amd64.tar.gz
        cd magnus-{{ jumpserver.version }}-linux-amd64
        ```
        ```bash
        wget https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-amd64.tar.gz
        tar -xf wisp-{{ jumpserver.wisp }}-linux-amd64.tar.gz
        mv wisp-{{ jumpserver.wisp }}-linux-amd64/wisp /usr/local/bin/
        chown root:root /usr/local/bin/wisp /opt/magnus-{{ jumpserver.version }}-linux-amd64/magnus
        chmod 755 /usr/local/bin/wisp /opt/magnus-{{ jumpserver.version }}-linux-amd64/magnus
        ```
    
        - 修改配置文件。
    
        ```bash
        cp config_example.yml config.yml
        vi config.yml
        ```
        ```yaml
        # Jumpserver项目的url, api请求注册会使用
        CORE_HOST: http://127.0.0.1:8080   # Core 的地址
    
        # Bootstrap Token, 预共享秘钥, 用来注册使用的service account和terminal
        # 请和jumpserver 配置文件中保持一致，注册完成后可以删除
        BOOTSTRAP_TOKEN: ********  # 和 Core config.yml 的值保持一致
    
        # 服务 bind 地址
        BIND_HOST: "0.0.0.0"
    
        # 数据库代理暴露的端口
        MYSQL_PORT: 33060
        MARIA_DB_PORT: 33061
        POSTGRESQL_PORT: 54320
    
        # 日志级别
        LOG_LEVEL: "info"
    
        # jumpserver api grpc 组件地址
        WISP_HOST: "localhost"
        WISP_PORT: 9090
        ```
    
        - 启动 Wisp。
    
        ```bash
        export CORE_HOST="http://127.0.0.1:8080"   # Core 的地址
        export BOOTSTRAP_TOKEN=********            # 和 Core config.yml 的值保持一致
        export WORK_DIR="/opt/magnus-{{ jumpserver.version }}-linux-amd64"
        export COMPONENT_NAME="magnus"
        export EXECUTE_PROGRAM="/opt/magnus-{{ jumpserver.version }}-linux-amd64/magnus"
        wisp
        ```
    
    === "Linux/arm64"
    
        - 解压缩包。
    
        ```bash
        cd /opt
        wget https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-linux-arm64.tar.gz
        tar -xf magnus-{{ jumpserver.version }}-linux-arm64.tar.gz
        cd magnus-{{ jumpserver.version }}-linux-arm64
        ```
        ```bash
        wget https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-arm64.tar.gz
        tar -xf wisp-{{ jumpserver.wisp }}-linux-arm64.tar.gz
        mv wisp-{{ jumpserver.wisp }}-linux-arm64/wisp /usr/local/bin/
        chown root:root /usr/local/bin/wisp /opt/magnus-{{ jumpserver.version }}-linux-arm64/magnus
        chmod 755 /usr/local/bin/wisp /opt/magnus-{{ jumpserver.version }}-linux-arm64/magnus
        ```
    
        - 修改配置文件。
    
        ```bash
        cp config_example.yml config.yml
        vi config.yml
        ```
        ```yaml
        # Jumpserver项目的url, api请求注册会使用
        CORE_HOST: http://127.0.0.1:8080   # Core 的地址
    
        # Bootstrap Token, 预共享秘钥, 用来注册使用的service account和terminal
        # 请和jumpserver 配置文件中保持一致，注册完成后可以删除
        BOOTSTRAP_TOKEN: ********  # 和 Core config.yml 的值保持一致
    
        # 服务 bind 地址
        BIND_HOST: "0.0.0.0"
    
        # 数据库代理暴露的端口
        MYSQL_PORT: 33060
        MARIA_DB_PORT: 33061
        POSTGRESQL_PORT: 54320
    
        # 日志级别
        LOG_LEVEL: "info"
    
        # jumpserver api grpc 组件地址
        WISP_HOST: "localhost"
        WISP_PORT: 9090
        ```
    
        - 启动 Wisp。
    
        ```bash
        export CORE_HOST="http://127.0.0.1:8080"   # Core 的地址
        export BOOTSTRAP_TOKEN=********            # 和 Core config.yml 的值保持一致
        export WORK_DIR="/opt/magnus-{{ jumpserver.version }}-linux-arm64"
        export COMPONENT_NAME="magnus"
        export EXECUTE_PROGRAM="/opt/magnus-{{ jumpserver.version }}-linux-arm64/magnus"
        wisp
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
[core_release]: https://github.com/jumpserver/jumpserver/releases/tag/{{ jumpserver.version }}
[python]: https://www.python.org/downloads/
[linux_packages]: http://nginx.org/en/linux_packages.html
[lina_release]: https://github.com/jumpserver/lina/releases/tag/{{ jumpserver.version }}
[node]: https://nodejs.org/
[luna_release]: https://github.com/jumpserver/luna/releases/tag/{{ jumpserver.version }}
[koko_release]: https://github.com/jumpserver/koko/releases/tag/{{ jumpserver.version }}
[go]: https://golang.google.cn/
[koko]: https://github.com/jumpserver/koko
[koko_release]: https://github.com/jumpserver/koko/releases/tag/{{ jumpserver.version }}
[lion]: https://github.com/jumpserver/lion-release
[lion_release]: https://github.com/jumpserver/lion-release/releases/tag/{{ jumpserver.version }}
[guacamole]: http://guacamole.apache.org/
[apache]: http://www.apache.org/
[guacamole-server]: https://github.com/apache/guacamole-server
[building-guacamole-server]: http://guacamole.apache.org/doc/gug/installing-guacamole.html#building-guacamole-server
[guacd-1.4.0]: http://download.jumpserver.org/public/guacamole-server-1.4.0.tar.gz
[wisp]: https://github.com/jumpserver/wisp
[wisp_release]: https://github.com/jumpserver/wisp/releases/tag/{{ jumpserver.wisp }}
[magnus]: https://github.com/jumpserver/magnus-release
[magnus_release]: https://github.com/jumpserver/magnus-release/releases/tag/{{ jumpserver.version }}
[lina-{{ jumpserver.version }}]: https://github.com/jumpserver/lina/releases/download/{{ jumpserver.version }}/lina-{{ jumpserver.version }}.tar.gz
[luna-{{ jumpserver.version }}]: https://github.com/jumpserver/luna/releases/download/{{ jumpserver.version }}/luna-{{ jumpserver.version }}.tar.gz
[koko-{{ jumpserver.version }}-linux-amd64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-linux-amd64.tar.gz
[koko-{{ jumpserver.version }}-linux-arm64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-linux-arm64.tar.gz
[koko-{{ jumpserver.version }}-linux-loong64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-linux-loong64.tar.gz
[koko-{{ jumpserver.version }}-darwin-amd64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-darwin-amd64.tar.gz
[koko-{{ jumpserver.version }}-darwin-arm64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-darwin-arm64.tar.gz
[lion-{{ jumpserver.version }}-linux-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-linux-amd64.tar.gz
[lion-{{ jumpserver.version }}-linux-arm64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-linux-arm64.tar.gz
[lion-{{ jumpserver.version }}-linux-loong64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-linux-loong64.tar.gz
[lion-{{ jumpserver.version }}-darwin-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-darwin-amd64.tar.gz
[lion-{{ jumpserver.version }}-windows-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-windows-amd64.tar.gz
[magnus-{{ jumpserver.version }}-linux-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-linux-amd64.tar.gz
[magnus-{{ jumpserver.version }}-linux-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-linux-arm64.tar.gz
[magnus-{{ jumpserver.version }}-linux-loong64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-linux-loong64.tar.gz
[magnus-{{ jumpserver.version }}-darwin-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-darwin-amd64.tar.gz
[magnus-{{ jumpserver.version }}-darwin-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-darwin-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-amd64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-arm64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-loong64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-loong64.tar.gz
[wisp-{{ jumpserver.wisp }}-darwin-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-darwin-amd64.tar.gz
[wisp-{{ jumpserver.wisp }}-darwin-arm64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-darwin-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-windows-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-windows-amd64.tar.gz