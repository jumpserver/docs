# Lion 环境搭建
## 1 Lion 组件概述
!!! tip ""
    [Lion][lion] 使用了 [Apache][apache] 软件基金会的开源项目 [Guacamole][guacamole]，JumpServer 使用 Golang 和 Vue 重构了 Guacamole 实现 RDP/VNC 协议跳板机功能。

### 1.1 环境要求
!!! tip ""

    | Name    | JumpServer               | Guacd                  |  Lion                    |
    | :------ | :----------------------- | :--------------------- | :----------------------- |
    | Version | {{ jumpserver.tag }}     | [1.5.5][guacd-1.5.5]   | {{ jumpserver.tag }} |

    - 可以从 [Github][guacamole-server] 网站上获取对应的 guacd 副本。这些版本是最新代码的稳定快照，从项目网站下载 Source code.tar.gz 源代码，通过命令行中提取该存档：

    ```bash
    mkdir /opt/guacamole-{{ jumpserver.tag }}
    cd /opt/guacamole-{{ jumpserver.tag }}
    wget http://download.jumpserver.org/public/guacamole-server-1.4.0.tar.gz
    tar -xzf guacamole-server-1.4.0.tar.gz
    cd guacamole-server-1.4.0/
    ```

    - 参考 [building-guacamole-server][building-guacamole-server] 官方文档，安装对应操作系统的依赖包。

    === "Ubuntu 22.04"
        ```bash
        sudo apt update
        apt install -y build-essential git curl wget ca-certificates  supervisor jq
        apt install -y libcairo2-dev libjpeg62-turbo-dev libpng-dev libtool-bin libossp-uuid-dev libavcodec-dev libavformat-dev libavutil-dev libswscale-dev freerdp2-dev libpango1.0-dev libssh2-1-dev libtelnet-dev libvncserver-dev libwebsockets-dev libpulse-dev libssl-dev libvorbis-dev libwebp-dev
        ```

### 1.2 构建 Guacd
!!! tip ""
    ```bash
    ./configure --with-init-dir=/etc/init.d
    make
    make install
    ldconfig
    ```

    !!! tip ""
    - 如果希望使用 systemd 管理, 可以使用 ./configure --with-systemd-dir=/etc/systemd/system/

### 1.3 下载 Lion
!!! tip ""
    - 可以从 [Github][lion] 网站上获取最新的源代码 。
    ```bash
    cd /opt
    git clone https://github.com/jumpserver/lion.git
    ```
### 1.4 修改配置文件
!!! tip ""
    ```bash
    cp config_example.yml config.yml
    vi config.yml
    ```
    ```yaml
    # 项目名称, 会用来向Jumpserver注册, 识别而已, 不能重复
    # NAME: {{ Hostname }}

    # Jumpserver项目的url, api请求注册会使用
    CORE_HOST: http://127.0.0.1:8080

    # Bootstrap Token, 预共享秘钥, 用来注册使用的service account和terminal
    # 请和jumpserver 配置文件中保持一致，注册完成后可以删除
    BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>

    # 启动时绑定的ip, 默认 0.0.0.0
    # BIND_HOST: 0.0.0.0

    # 监听的HTTP/WS端口号，默认8081
    # HTTPD_PORT: 8081

    # 设置日志级别 [DEBUG, INFO, WARN, ERROR, FATAL, CRITICAL]
    # LOG_LEVEL: INFO

    # Guacamole Server ip， 默认127.0.0.1
    # GUA_HOST: 127.0.0.1

    # Guacamole Server 端口号，默认4822
    # GUA_PORT: 4822

    # 会话共享使用的类型 [local, redis], 默认local
    # SHARE_ROOM_TYPE: local

    # Redis配置
    # REDIS_HOST: 127.0.0.1
    # REDIS_PORT: 6379
    # REDIS_PASSWORD:
    # REDIS_DB_ROOM: 0
    ```

### 1.5 启动 Guacd
!!! tip ""
    ```bash
    /etc/init.d/guacd start
    ```

### 1.6 编译启动 Lion
!!! tip ""
    ```bash
    # 安装依赖和构建前端
    cd /opt/lion/ui
    yarn install
    yarn build

    # 下载后端依赖并构建后端
    cd ..
    go mod download
    # 设置编译版本信息
    export GOFLAGS="-X 'main.Buildstamp=$(date -u '+%Y-%m-%d %I:%M:%S%p')' \
                -X 'main.Githash=$(git rev-parse HEAD)' \
                -X 'main.Goversion=$(go version)' \
                -X 'main.Version=${VERSION}'"
                
    go build -trimpath -ldflags "$GOFLAGS" -o lion .  # 编译后端
    # 启动服务
    chmod +x entrypoint.sh
    supervisord -c supervisord.conf  # 使用 supervisord 管理进程
    
    # 直接启动后端服务
    ./lion # 后端启动命令
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
[lion]: https://github.com/jumpserver/lion
[lion_release]: https://github.com/jumpserver/lion-release/releases/tag/{{ jumpserver.tag }}
[guacamole]: http://guacamole.apache.org/
[apache]: http://www.apache.org/
[guacamole-server]: https://github.com/apache/guacamole-server
[building-guacamole-server]: http://guacamole.apache.org/doc/gug/installing-guacamole.html#building-guacamole-server
[guacd-1.5.5]: http://download.jumpserver.org/public/guacamole-server-1.5.5.tar.gz
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

