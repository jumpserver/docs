# KoKo 环境部署
## 1 KoKo 组件概述
!!! tip ""
    Koko 是 Go 版本的 coco，重构了 coco 的 SSH/SFTP 服务和 Web Terminal 服务。

### 1.1 环境要求
!!! tip ""

    | Name    | KoKo                     | Go   | Node  | Redis Client |
    | :------ | :----------------------- | :--  | :---- | :----------- |
    | Version | {{ jumpserver.tag }}     | 1.24.7 | 20.15.1  | >= 6.0       |

### 1.2 选择部署方式
!!! tip ""
    === "源代码部署"

        - 下载源代码。
        - 从项目网站下载 Source code.tar.gz 源代码，通过命令行中提取该存档：

        ```bash
        cd /opt
        mkdir /opt/koko
        wget -O /opt/koko.tar.gz https://github.com/jumpserver/koko/archive/refs/tags/{{ jumpserver.tag }}.tar.gz
        tar -xf koko-{{ jumpserver.tag }}.tar.gz -C /opt/koko --strip-components 1
        ```

        - 安装 Node。
        - 从 [Node][node] 官方网站参考文档部署 Node.js，请根据 [环境要求](#_10)，通过命令行中判断是否安装完成。

        ```bash
        node -v
        ```
        `v20.15.1`

        - 安装 Client 依赖。

        === "Ubuntu 22.04"
            ```bash
            
            apt-get update
            apt install software-properties-common
            add-apt-repository -y ppa:redislabs/redis
            apt-get install -y  bash-completion redis-tools jq less ca-certificates
            cd /opt
            mkdir /opt/kubectl-aliases
            wget https://github.com/ahmetb/kubectl-aliases/raw/master/.kubectl_aliases
            tar -xf kubectl_aliases.tar.gz -C /opt/kubectl-aliases
            ```

        - 安装 Go。
        - [Go][go] 官方网站参考文档部署 golang，请根据 [环境要求](#_14)，通过命令行中判断是否安装完成：

        === "Ubuntu 22.04"
            ```bash
            cd /opt
            wget wget https://go.dev/dl/go1.24.7.linux-amd64.tar.gz
            tar -xf go1.24.7.linux-amd64.tar.gz -C /usr/local/
            chown -R root:root /usr/local/go
            export PATH=/usr/local/go/bin:$PATH
            echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc
            ```

        ```bash
        go version
        ```
        `go version go1.24.7 linux/amd64`

        - 编译。

        | OS    | Arch  | Command     |
        | :---- | :---- | :---------- |
        | Linux | amd64 | make linux  |
        | macOS | amd64 | make darwin |

        ```bash
        cd /opt/koko
        make
        cp build/koko-{{ jumpserver.tag }}-linux-amd64.tar.gz /opt
        go mod download
        ```

        !!! tip "构建完成后, 生成在 build 目录下"

    === "使用 Release"

        - 下载 Release 文件。
        - 从 [Github][koko] 网站上获取最新的 [Release][koko_release] 副本。这些版本是最新代码的稳定快照。

        | OS     | Arch    | Name                                                                                              |
        | :----- | :------ | :------------------------------------------------------------------------------------------------ |
        | Linux  | amd64   | [koko-{{ jumpserver.tag }}-linux-amd64.tar.gz][koko-{{ jumpserver.tag }}-linux-amd64]     |
        | Linux  | arm64   | [koko-{{ jumpserver.tag }}-linux-arm64.tar.gz][koko-{{ jumpserver.tag }}-linux-arm64]     |
        | linux  | loong64 | [koko-{{ jumpserver.tag }}-linux-loong64.tar.gz][koko-{{ jumpserver.tag }}-linux-loong64] |
        | Darwin | amd64   | [koko-{{ jumpserver.tag }}-darwin-amd64.tar.gz][koko-{{ jumpserver.tag }}-darwin-amd64]   |
        | Darwin | arm64   | [koko-{{ jumpserver.tag }}-darwin-arm64.tar.gz][koko-{{ jumpserver.tag }}-darwin-arm64]   |

        === "Linux/amd64"
            ```bash
            cd /opt
            wget https://download.jumpserver.org/public/kubectl-linux-amd64.tar.gz -O kubectl.tar.gz
            tar -xf kubectl.tar.gz
            mv kubectl /usr/local/bin/rawkubectl
            wget https://download.jumpserver.org/public/helm-v3.9.0-linux-amd64.tar.gz
            tar -xf helm-v3.9.0-linux-amd64.tar.gz
            mv linux-amd64/helm /usr/local/bin/rawhelm
            chmod 755 /usr/local/bin/rawkubectl /usr/local/bin/rawhelm
            chown root:root /usr/local/bin/rawkubectl /usr/local/bin/rawhelm
            rm -rf linux-amd64
            wget https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-linux-amd64.tar.gz
            tar -xf koko-{{ jumpserver.tag }}-linux-amd64.tar.gz -C /opt
            cd koko-{{ jumpserver.tag }}-linux-amd64
            mv kubectl /usr/local/bin/kubectl
            ```

        === "Linux/arm64"
            ```bash
            cd /opt
            wget https://download.jumpserver.org/public/kubectl-linux-arm64.tar.gz -O kubectl.tar.gz
            tar -xzf kubectl.tar.gz
            mv kubectl /usr/local/bin/rawkubectl
            wget https://download.jumpserver.org/public/helm-v3.9.0-linux-arm64.tar.gz
            tar -xf helm-v3.9.0-linux-arm64.tar.gz
            mv linux-arm64/helm /usr/local/bin/rawhelm
            chmod 755 /usr/local/bin/rawkubectl /usr/local/bin/rawhelm
            chown root:root /usr/local/bin/rawkubectl /usr/local/bin/rawhelm
            rm -rf linux-arm64
            wget https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-linux-arm64.tar.gz
            tar -xf koko-{{ jumpserver.tag }}-linux-arm64.tar.gz -C /opt
            cd koko-{{ jumpserver.tag }}-linux-arm64
            mv kubectl /usr/local/bin/kubectl
            ```

### 1.3 修改配置文件
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

    # Bootstrap Token, 预共享秘钥, 用来注册coco使用的service account和terminal
    # 请和jumpserver 配置文件中保持一致，注册完成后可以删除
    BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>

    # 启动时绑定的ip, 默认 0.0.0.0
    # BIND_HOST: 0.0.0.0

    # 监听的SSH端口号, 默认2222
    # SSHD_PORT: 2222

    # 监听的HTTP/WS端口号，默认5000
    # HTTPD_PORT: 5000

    # 设置日志级别 [DEBUG, INFO, WARN, ERROR, FATAL, CRITICAL]
    # LOG_LEVEL: INFO

    # SSH连接超时时间 (default 15 seconds)
    # SSH_TIMEOUT: 15

    # Api Http请求的超时时间 (default 30 seconds)
    # HTTP_REQUEST_TIMEOUT: 30

    # 语言 [en,zh]
    # LANGUAGE_CODE: zh

    # SFTP是否显示隐藏文件
    # SFTP_SHOW_HIDDEN_FILE: false

    # 是否复用和用户后端资产已建立的连接(用户不会复用其他用户的连接)
    # REUSE_CONNECTION: true

    # 资产加载策略, 可根据资产规模自行调整. 默认异步加载资产, 异步搜索分页; 如果为all, 则资产全部加载, 本地搜索分页.
    # ASSET_LOAD_POLICY:

    # zip压缩的最大额度 (单位: M)
    # ZIP_MAX_SIZE: 1024M

    # zip压缩存放的临时目录 /tmp
    # ZIP_TMP_PATH: /tmp

    # 向 SSH Client 连接发送心跳的时间间隔 (单位: 秒)，默认为30, 0则表示不发送
    # CLIENT_ALIVE_INTERVAL: 30

    # 向资产发送心跳包的重试次数，默认为3
    # RETRY_ALIVE_COUNT_MAX: 3

    # 会话共享使用的类型 [local, redis], 默认local
    # SHARE_ROOM_TYPE: local

    # Redis配置
    # REDIS_HOST: 127.0.0.1
    # REDIS_PORT: 6379
    # REDIS_PASSWORD:
    # REDIS_CLUSTERS:
    # REDIS_DB_ROOM:

    # 是否开启本地转发 (目前仅对 vscode remote ssh 有效果)
    # ENABLE_LOCAL_PORT_FORWARD: false

    # 是否开启 针对 vscode 的 remote-ssh 远程开发支持 (前置条件: 必须开启 ENABLE_LOCAL_PORT_FORWARD )
    # ENABLE_VSCODE_SUPPORT: false
    ```

### 1.4 编译并启动 KoKo
!!! tip ""
    ```bash
    cd /opt/koko/ui
    yarn install
    yarn build

    cd ..
    go run cmd/koko/koko.go
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
