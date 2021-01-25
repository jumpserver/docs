# Guacamole 常见问题

!!! info "请先确认下面选项"
    请在 `web` - `系统设置` - `安全设置` 里面允许 `终端注册`  
    Docker 容器部署的 `JUMPSERVER_SERVER` 不可以使用 `http://127.0.0.1:8080`

### 1. guacamole 启动异常

!!! question "启动异常"
    - ERROR o.a.g.a.j.r.JumpserverRegisterService 121 - 注册终端失败

    在 web - 会话管理 - 终端管理 里面删除 guacamole 的注册 ( 在线显示红色的[gua]xxx )  

    ```sh
    rm -f /opt/jumpserver/guacamole/data/keys/jumpserver.key
    docker restart jms_guacamole
    ```

    Windows 文件上传可以直接把文件拖拽到 Windows 窗口, 上传后文件在 计算机 - G盘, 下载把文件放到 G 盘的 download  目录即可弹出下载窗口, 快捷键上传下载工具栏 ++ctrl+alt+shift++

### 2. 频繁断开临时解决方案

!!! question "Win7/2008 Linux VNC 频繁断开临时解决方案"
    - 使用此方式后将无法使用网域功能
    - <= 2.6.6  使用 image: guacamole/guacd:1.2.0
    - >= 2.7.0  使用 image: guacamole/guacd:1.3.0

    ```sh
    vi compose/docker-compose-app.yml
    ```
    ```vim hl_lines="107-116"
    version: '2.2'

    services:
      nginx:
        image: jumpserver/nginx:alpine2
        container_name: jms_nginx
        restart: always
        ports:
          - ${HTTP_PORT}:80
          - ${HTTPS_PORT}:443
        volumes:
          - ./config_static/http_server.conf:/etc/nginx/conf.d/default.conf
          - ${CONFIG_DIR}/nginx/cert:/etc/nginx/cert
          - ${VOLUME_DIR}/core/data:/data
          - ${VOLUME_DIR}/nginx/log:/var/log/nginx
        depends_on:
          - core
          - luna
          - koko
          - guacamole
        healthcheck:
          test: ["CMD", "test", "-f", "/var/run/nginx.pid"]
          interval: 10s
          timeout: 5s
          retries: 2
        networks:
          - net

      core:
        image: jumpserver/core:${VERSION}
        container_name: jms_core
        restart: always
        tty: true
        command: start web
        env_file:
          - ${CONFIG_FILE}
        volumes:
          - ${CONFIG_DIR}/core/config.yml:/opt/jumpserver/config.yml
          - ${VOLUME_DIR}/core/data:/opt/jumpserver/data
          - ${VOLUME_DIR}/core/logs:/opt/jumpserver/logs
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8080/api/health/"]
          interval: 10s
          timeout: 5s
          retries: 10
        networks:
          - net

      koko:
        image: jumpserver/koko:${VERSION}
        container_name: jms_koko
        restart: always
        tty: true
        env_file:
          - ${CONFIG_FILE}
        ports:
          - ${SSH_PORT}:2222
        depends_on:
          core:
            condition: service_healthy
        volumes:
          - ${CONFIG_DIR}/koko/config.yml:/opt/koko/config.yml
          - ${VOLUME_DIR}/koko/data:/opt/koko/data
        privileged: true
        healthcheck:
          test: "ps axu | grep 'koko'"
          interval: 10s
          timeout: 5s
          retries: 3
        networks:
          - net

      luna:
        image: jumpserver/luna:${VERSION}
        container_name: jms_luna
        restart: always
        env_file:
          - ${CONFIG_FILE}
        depends_on:
          core:
            condition: service_healthy
        healthcheck:
          test: "wget http://localhost/luna/ -O -"
          interval: 10s
          timeout: 5s
          retries: 3
        networks:
          - net

      lina:
        image: jumpserver/lina:${VERSION}
        container_name: jms_lina
        restart: always
        env_file:
          - ${CONFIG_FILE}
        depends_on:
          core:
            condition: service_healthy
        healthcheck:
          test: "wget http://localhost/ -O -"
          interval: 10s
          timeout: 5s
          retries: 3
        networks:
          - net

      guacd:
        image: guacamole/guacd:1.3.0
        container_name: jms_guacd
        environment:
          GUACD_LOG_LEVEL: error
        restart: always
        volumes:
          - ${VOLUME_DIR}/guacamole/data:/config/guacamole/data
        networks:
          - net

      guacamole:
        image: jumpserver/guacamole:${VERSION}
        container_name: jms_guacamole
        env_file:
          - ${CONFIG_FILE}
        restart: always
        volumes:
          - ${VOLUME_DIR}/guacamole/data:/config/guacamole/data
        depends_on:
          core:
            condition: service_healthy
        healthcheck:
          test: ["CMD", "curl", "http://localhost:8080"]
          interval: 10s
          timeout: 5s
          retries: 3
        networks:
          - net
    ```
    ```sh
    vi guacamole.properties
    ```
    ```vim
    enable-clipboard-integration: true
    guacd-hostname: jms_guacd
    guacd-port: 4822
    ```
    ```sh
    docker cp guacamole.properties jms_guacamole:/config/guacamole/guacamole.properties
    ./jmsctl.sh start
    docker restart jms_guacamole
    ```

### 3. RDP VNC 显示效果优化

!!! question ""
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim hl_lines="11-14"
    ... 省略
    # Guacamole 配置
    JUMPSERVER_SERVER=http://core:8080
    JUMPSERVER_KEY_DIR=/config/guacamole/data/key/
    JUMPSERVER_RECORD_PATH=/config/guacamole/data/record/
    JUMPSERVER_DRIVE_PATH=/config/guacamole/data/drive/
    JUMPSERVER_ENABLE_DRIVE=true
    JUMPSERVER_CLEAR_DRIVE_SESSION=true
    JUMPSERVER_CLEAR_DRIVE_SCHEDULE=24
    # 添加下面内容
    JUMPSERVER_COLOR_DEPTH=32               # 远程桌面使用 32 位真彩
    JUMPSERVER_DPI=120                      # 远程桌面 DPI
    JUMPSERVER_DISABLE_BITMAP_CACHING=true  # 禁用RDP的内置位图缓存功能
    JUMPSERVER_DISABLE_GLYPH_CACHING=true   # 禁用RDP会话中的字形缓存
    ```
    ```sh
    ./jmsctl.sh restart
    ```
