# Lion 环境搭建
## 1 Lion 组件概述
!!! tip ""
    [Lion][lion] 基于 [Apache][apache] 基金会开源项目 [Guacamole][guacamole] 的后端服务，JumpServer 使用 Golang 与 Vue 重构其客户端，实现 RDP/VNC 协议的跳板访问能力。

### 1.1 环境要求
!!! tip ""

    | Name    | JumpServer               | Guacd                | Lion                    |
    | :------ | :----------------------- | :------------------- | :---------------------- |
    | Version | {{ jumpserver.tag }}     | [1.5.5][guacd-1.5.5] | {{ jumpserver.tag }}    |

### 1.2 获取 Guacd 源码
!!! tip ""
    - 可从 [Github][guacamole-server] 获取 Guacamole Server (guacd) 源码，这些版本是稳定发布的快照。下载 Source code 压缩包并解压：

    ```bash
    mkdir /opt/guacamole-{{ jumpserver.tag }}
    cd /opt/guacamole-{{ jumpserver.tag }}
    wget https://archive.apache.org/dist/guacamole/1.5.5/source/guacamole-server-1.5.5.tar.gz
    tar -xzf guacamole-server-1.5.5.tar.gz
    cd guacamole-server-1.5.5/
    ```

    - 参考 [building-guacamole-server][building-guacamole-server] 官方文档安装依赖：

    === "Ubuntu 22.04"
        ```bash
        sudo apt update
        apt install -y build-essential git curl wget ca-certificates supervisor jq
        apt install -y libcairo2-dev libjpeg62-turbo-dev libpng-dev libtool-bin libossp-uuid-dev libavcodec-dev libavformat-dev libavutil-dev libswscale-dev freerdp2-dev libpango1.0-dev libssh2-1-dev libtelnet-dev libvncserver-dev libwebsockets-dev libpulse-dev libssl-dev libvorbis-dev libwebp-dev
        ```

### 1.3 构建 Guacd
!!! tip ""
    ```bash
    ./configure --with-init-dir=/etc/init.d
    make
    make install
    ldconfig
    ```

    - 如果希望使用 systemd 管理，可使用：`./configure --with-systemd-dir=/etc/systemd/system/`

### 1.4 获取 Lion 源代码
!!! tip ""
    - 从 [Github][lion] 获取 Lion 源代码：
    ```bash
    cd /opt
    git clone https://github.com/jumpserver/lion.git
    ```

### 1.5 修改配置文件
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

### 1.6 启动 Guacd
!!! tip ""
    ```bash
    /etc/init.d/guacd start
    ```

### 1.7 启动 Lion
!!! tip ""
    ```bash
    # 启动前端项目
    cd /opt/lion/ui
    yarn install
    npm run dev

    # 下载客户端依赖并启动
    cd ..
    go mod download
    go run main.go

    # 启动 guacd 服务端 (若尚未启动)
    /etc/init.d/guacd start

    # 直接启动后端服务
    ./lion # 后端启动命令
    ```

[lion]: https://github.com/jumpserver/lion
[apache]: http://www.apache.org/
[guacamole]: http://guacamole.apache.org/
[guacamole-server]: https://github.com/apache/guacamole-server
[building-guacamole-server]: http://guacamole.apache.org/doc/gug/installing-guacamole.html#building-guacamole-server
[guacd-1.5.5]: http://download.jumpserver.org/public/guacamole-server-1.5.5.tar.gz

