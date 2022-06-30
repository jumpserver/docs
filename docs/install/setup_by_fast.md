# 安装文档

- [在 Windows/macOS 部署说明](setup_by_desktop.md)

!!! info "环境要求"

| OS Version    | Linux Kernel  | Soft Requirement                      |
| :------------ | :------------ | :------------------------------------ |
| Linux Release | >= 4.0        | wget curl tar gettext iptables python |

## 安装方式

- [安装演示视频](https://www.bilibili.com/video/av635028005)

!!! info "外置环境要求"
    - 推荐使用外置 数据库 和 Redis，方便日后扩展升级

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 5.0  |
| MariaDB | >= 10.2 |    |       |         |

### 在线安装

??? info "可以使用由 [华为云](https://www.huaweicloud.com/) 提供的容器镜像服务 :heart:{: .heart }"
    | 区域          | 镜像仓库地址                         | 配置文件 /opt/jumpserver/config/config.txt                | Kubernetes values.yaml                          | OS/ARCH      |
    | :----------- | :----------------------------------- | -------------------------------------------------------- | ----------------------------------------------- | ------------ |
    | 华北-北京一   | swr.cn-north-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com     | repository: swr.cn-north-1.myhuaweicloud.com    | linux/amd64  |
    | 华北-北京四   | swr.cn-north-4.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-4.myhuaweicloud.com     | repository: swr.cn-north-4.myhuaweicloud.com    | linux/amd64  |
    | 华南-广州     | swr.cn-south-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com     | repository: swr.cn-south-1.myhuaweicloud.com    | linux/amd64  |
    | 华东-上海一   | swr.cn-east-3.myhuaweicloud.com      | DOCKER_IMAGE_PREFIX=swr.cn-east-3.myhuaweicloud.com      | repository: swr.cn-east-3.myhuaweicloud.com      | linux/amd64 |
    | 亚太-香港     | swr.ap-southeast-1.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-1.myhuaweicloud.com | repository: swr.ap-southeast-1.myhuaweicloud.com | linux/amd64 |
    | 亚太-新加坡   | swr.ap-southeast-3.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-3.myhuaweicloud.com | repository: swr.ap-southeast-3.myhuaweicloud.com | linux/amd64 |

=== "一键部署"
    !!! tip ""
        ```sh
        # 默认会安装到 /opt/jumpserver-installer-{{ jumpserver.version }} 目录
        curl -sSL https://github.com/jumpserver/jumpserver/releases/download/{{ jumpserver.version }}/quick_start.sh | bash
        cd /opt/jumpserver-installer-{{ jumpserver.version }}
        ```
    !!! tip ""
        ```sh
        # 安装完成后配置文件 /opt/jumpserver/config/config.txt
        ```
        ```sh
        cd /opt/jumpserver-installer-{{ jumpserver.version }}

        # 启动
        ./jmsctl.sh start

        # 停止
        ./jmsctl.sh down

        # 卸载
        ./jmsctl.sh uninstall

        # 帮助
        ./jmsctl.sh -h
        ```

=== "手动部署"
    !!! tip ""
        ```sh
        cd /opt
        wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.version }}
        ```
        ```sh
        # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
        cat config-example.txt
        ```
        ```vim
        # 以下设置如果为空系统会自动生成随机字符串填入
        ## 迁移请修改 SECRET_KEY 和 BOOTSTRAP_TOKEN 为原来的设置
        ## 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ## 安装配置, amd64 默认使用华为云加速下载, arm64 请注释掉 DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        # DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        VOLUME_DIR=/opt/jumpserver
        DOCKER_DIR=/var/lib/docker
        SECRET_KEY=
        BOOTSTRAP_TOKEN=
        LOG_LEVEL=ERROR

        ##  MySQL 配置, USE_EXTERNAL_MYSQL=1 表示使用外置数据库, 请输入正确的 MySQL 信息
        USE_EXTERNAL_MYSQL=0
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        ##  Redis 配置, USE_EXTERNAL_REDIS=1 表示使用外置数据库, 请输入正确的 Redis 信息
        USE_EXTERNAL_REDIS=0
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        ## Compose 项目设置, 如果 192.168.250.0/24 网段与你现有网段冲突, 请修改然后重启 JumpServer
        COMPOSE_PROJECT_NAME=jms
        COMPOSE_HTTP_TIMEOUT=3600
        DOCKER_CLIENT_TIMEOUT=3600
        DOCKER_SUBNET=192.168.250.0/24

        ## IPV6 设置, 容器是否开启 ipv6 nat, USE_IPV6=1 表示开启, 为 0 的情况下 DOCKER_SUBNET_IPV6 定义不生效
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

        ## 访问配置
        HTTP_PORT=80
        SSH_PORT=2222
        MAGNUS_MYSQL_PORT=33060
        MAGNUS_MARIADB_PORT=33061

        ## HTTPS 配置, 参考 https://docs.jumpserver.org/zh/master/admin-guide/proxy/ 配置
        # USE_LB=1
        # HTTPS_PORT=443
        # SERVER_NAME=your_domain_name
        # SSL_CERTIFICATE=your_cert
        # SSL_CERTIFICATE_KEY=your_cert_key

        ## Nginx 文件上传大小
        CLIENT_MAX_BODY_SIZE=4096m

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0
        RDP_PORT=3389
        MAGNUS_POSTGRE_PORT=54320
        TCP_SEND_BUFFER_BYTES=4194304
        TCP_RECV_BUFFER_BYTES=6291456

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=True 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=True

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080
        JUMPSERVER_ENABLE_FONT_SMOOTHING=True

        ## 终端使用宿主 HOSTNAME 标识
        SERVER_HOSTNAME=${HOSTNAME}

        # 额外的配置
        CURRENT_VERSION=
        ```
        ```sh
        # 安装
        ./jmsctl.sh install

        # 启动
        ./jmsctl.sh start
        ```
    !!! tip ""
        ```sh
        # 安装完成后配置文件 /opt/jumpserver/config/config.txt
        ```
        ```sh
        cd /opt/jumpserver-installer-{{ jumpserver.version }}

        # 启动
        ./jmsctl.sh start

        # 停止
        ./jmsctl.sh down

        # 卸载
        ./jmsctl.sh uninstall

        # 帮助
        ./jmsctl.sh -h
        ```

=== "Helm"
    !!! tip ""
        ```sh
        helm repo add jumpserver https://jumpserver.github.io/helm-charts
        helm repo list
        vi values.yaml
        ```
        ```yaml
        # 模板 https://github.com/jumpserver/helm-charts/blob/main/charts/jumpserver/values.yaml
        # Default values for jumpserver.
        # This is a YAML-formatted file.
        # Declare variables to be passed into your templates.

        nameOverride: ""
        fullnameOverride: ""

        ## @param global.imageRegistry Global Docker image registry
        ## @param global.imagePullSecrets Global Docker registry secret names as an array
        ## @param global.storageClass Global StorageClass for Persistent Volume(s)
        ## @param global.redis.password Global Redis&trade; password (overrides `auth.password`)
        ##
        global:
          imageRegistry: "docker.io"    # 国内可以使用华为云加速 swr.cn-south-1.myhuaweicloud.com
          imageTag: {{ jumpserver.version }}             # 版本号
          ## E.g.
          #  imagePullSecrets:
          #    - name: harborsecret
          #
          #  storageClass: "jumpserver-data"
          ##
          imagePullSecrets: []
            # - name: yourSecretKey
          storageClass: ""              # (*必填) NFS SC

        ## Please configure your MySQL server first
        ## Jumpserver will not start the external MySQL server.
        ##
        externalDatabase:               #  (*必填) 数据库相关设置
          engine: mysql
          host: localhost
          port: 3306
          user: root
          password: ""
          database: jumpserver

        ## Please configure your Redis server first
        ## Jumpserver will not start the external Redis server.
        ##
        externalRedis:                  #  (*必填) Redis 设置
          host: localhost
          port: 6379
          password: ""

        serviceAccount:
          # Specifies whether a service account should be created
          create: false
          # The name of the service account to use.
          # If not set and create is true, a name is generated using the fullname template
          name:

        ingress:
          enabled: true                             # 不使用 ingress 可以关闭
          annotations:
            # kubernetes.io/tls-acme: "true"
            compute-full-forwarded-for: "true"
            use-forwarded-headers: "true"
            kubernetes.io/ingress.class: nginx
            nginx.ingress.kubernetes.io/configuration-snippet: |
               proxy_set_header Upgrade "websocket";
               proxy_set_header Connection "Upgrade";
          hosts:
            - "test.jumpserver.org"                 # 对外域名
          tls: []
          #  - secretName: chart-example-tls
          #    hosts:
          #      - chart-example.local

        core:
          enabled: true

          labels:
            app.jumpserver.org/name: jms-core

          config:
            # Generate a new random secret key by execute `cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 50`
            # secretKey: "B3f2w8P2PfxIAS7s4URrD9YmSbtqX4vXdPUL217kL9XPUOWrmy"
            secretKey: ""                            #  (*必填) 加密敏感信息的 secret_key, 长度推荐大于 50 位
            # Generate a new random bootstrap token by execute `cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`
            # bootstrapToken: "7Q11Vz6R2J6BLAdO"
            bootstrapToken: ""                       #  (*必填) 组件认证使用的 token, 长度推荐大于 24 位
            # Enabled it for debug
            debug: false
            log:
              level: ERROR

          replicaCount: 1

          image:
            registry: docker.io
            repository: jumpserver/core
            tag: {{ jumpserver.version }}
            pullPolicy: IfNotPresent

          command: []

          env:
            # See: https://docs.jumpserver.org/zh/master/admin-guide/env/#core
            SESSION_EXPIRE_AT_BROWSER_CLOSE: true
            # SESSION_COOKIE_AGE: 86400
            # SECURITY_VIEW_AUTH_NEED_MFA: true

          livenessProbe:
            failureThreshold: 30
            httpGet:
              path: /api/health/
              port: web

          readinessProbe:
            failureThreshold: 30
            httpGet:
              path: /api/health/
              port: web

          podSecurityContext: {}
            # fsGroup: 2000

          securityContext: {}
            # capabilities:
            #   drop:
            #   - ALL
            # readOnlyRootFilesystem: true
            # runAsNonRoot: true
            # runAsUser: 1000

          service:
            type: ClusterIP
            web:
              port: 8080
            ws:
              port: 8070

          resources: {}
            # We usually recommend not to specify default resources and to leave this as a conscious
            # choice for the user. This also increases chances charts run on environments with little
            # resources, such as Minikube. If you do want to specify resources, uncomment the following
            # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
            # limits:
            #   cpu: 1000m
            #   memory: 2048Mi
            # requests:
            #   cpu: 500m
            #   memory: 1024Mi

          persistence:
            storageClassName: jumpserver-data
            accessModes:
              - ReadWriteMany
            size: 100Gi
            # annotations: {}
            finalizers:
              - kubernetes.io/pvc-protection
            # subPath: ""
            # existingClaim:

          volumeMounts: []

          volumes: []

          nodeSelector: {}

          tolerations: []

          affinity: {}

        koko:
          enabled: true

          labels:
            app.jumpserver.org/name: jms-koko

          config:
            log:
              level: ERROR

          replicaCount: 1

          image:
            registry: docker.io
            repository: jumpserver/koko
            tag: {{ jumpserver.version }}
            pullPolicy: IfNotPresent

          command: []

          env: []
            # See: https://docs.jumpserver.org/zh/master/admin-guide/env/#koko
            # LANGUAGE_CODE: zh
            # REUSE_CONNECTION: true
            # ENABLE_LOCAL_PORT_FORWARD: true
            # ENABLE_VSCODE_SUPPORT: true

          livenessProbe:
            failureThreshold: 30
            httpGet:
              path: /koko/health/
              port: web

          readinessProbe:
            failureThreshold: 30
            httpGet:
              path: /koko/health/
              port: web

          podSecurityContext: {}
            # fsGroup: 2000

          securityContext:
            privileged: true
            # capabilities:
            #   drop:
            #   - ALL
            # readOnlyRootFilesystem: true
            # runAsNonRoot: true
            # runAsUser: 1000

          service:
            type: ClusterIP
            web:
              port: 5000
            ssh:
              port: 2222

          resources: {}
            # We usually recommend not to specify default resources and to leave this as a conscious
            # choice for the user. This also increases chances charts run on environments with little
            # resources, such as Minikube. If you do want to specify resources, uncomment the following
            # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
            # limits:
            #   cpu: 100m
            #   memory: 128Mi
            # requests:
            #   cpu: 100m
            #   memory: 128Mi

          persistence:
            storageClassName: jumpserver-data
            accessModes:
              - ReadWriteMany
            size: 10Gi
            # annotations: {}
            finalizers:
              - kubernetes.io/pvc-protection

          volumeMounts: []

          volumes: []

          nodeSelector: {}

          tolerations: []

          affinity: {}

        lion:
          enabled: true

          labels:
            app.jumpserver.org/name: jms-lion

          config:
            log:
              level: ERROR

          replicaCount: 1

          image:
            registry: docker.io
            repository: jumpserver/lion
            tag: {{ jumpserver.version }}
            pullPolicy: IfNotPresent

          command: []

          env:
            # See: https://docs.jumpserver.org/zh/master/admin-guide/env/#lion
            JUMPSERVER_ENABLE_FONT_SMOOTHING: true
            # JUMPSERVER_COLOR_DEPTH: 32
            # JUMPSERVER_ENABLE_WALLPAPER: true
            # JUMPSERVER_ENABLE_THEMING: true
            # JUMPSERVER_ENABLE_FULL_WINDOW_DRAG: true
            # JUMPSERVER_ENABLE_DESKTOP_COMPOSITION: true
            # JUMPSERVER_ENABLE_MENU_ANIMATIONS: true

          livenessProbe:
            failureThreshold: 30
            httpGet:
              path: /lion/health/
              port: web

          readinessProbe:
            failureThreshold: 30
            httpGet:
              path: /lion/health/
              port: web

          podSecurityContext: {}
            # fsGroup: 2000

          securityContext: {}
            # capabilities:
            #   drop:
            #   - ALL
            # readOnlyRootFilesystem: true
            # runAsNonRoot: true
            # runAsUser: 1000

          service:
            type: ClusterIP
            web:
              port: 8081

          resources: {}
            # We usually recommend not to specify default resources and to leave this as a conscious
            # choice for the user. This also increases chances charts run on environments with little
            # resources, such as Minikube. If you do want to specify resources, uncomment the following
            # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
            # limits:
            #   cpu: 100m
            #   memory: 512Mi
            # requests:
            #   cpu: 100m
            #   memory: 512Mi

          persistence:
            storageClassName: jumpserver-data
            accessModes:
              - ReadWriteMany
            size: 50Gi
            # annotations: {}
            finalizers:
              - kubernetes.io/pvc-protection

          volumeMounts: []

          volumes: []

          nodeSelector: {}

          tolerations: []

          affinity: {}

        magnus:
          enabled: true

          labels:
            app.jumpserver.org/name: jms-magnus

          config:
            log:
              level: ERROR

          replicaCount: 1

          image:
            registry: docker.io
            repository: jumpserver/magnus
            tag: v2.21.0
            pullPolicy: IfNotPresent

          command: []

          env: []

          livenessProbe:
            failureThreshold: 30
            tcpSocket:
              port: mysql

          readinessProbe:
            failureThreshold: 30
            tcpSocket:
              port: mysql

          podSecurityContext: {}
            # fsGroup: 2000

          securityContext: {}
            # capabilities:
            #   drop:
            #   - ALL
            # readOnlyRootFilesystem: true
            # runAsNonRoot: true
            # runAsUser: 1000

          service:
            type: ClusterIP
            mysql:
              port: 33060
            mariadb:
              port: 33061
            postgre:
              port: 54320

          resources: {}
            # We usually recommend not to specify default resources and to leave this as a conscious
            # choice for the user. This also increases chances charts run on environments with little
            # resources, such as Minikube. If you do want to specify resources, uncomment the following
            # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
            # limits:
            #   cpu: 100m
            #   memory: 512Mi
            # requests:
            #   cpu: 100m
            #   memory: 512Mi

          persistence:
            storageClassName: jumpserver-data
            accessModes:
              - ReadWriteMany
            size: 10Gi
            # annotations: {}
            finalizers:
              - kubernetes.io/pvc-protection

          volumeMounts: []

          volumes: []

          nodeSelector: {}

          tolerations: []

          affinity: {}

        xpack:
          enabled: false      # 企业版本打开此选项

        omnidb:
          labels:
            app.jumpserver.org/name: jms-omnidb

          config:
            log:
              level: ERROR

          replicaCount: 1

          image:
            registry: registry.fit2cloud.com
            repository: jumpserver/omnidb
            tag: {{ jumpserver.version }}
            pullPolicy: IfNotPresent

          command: []

          env: []

          livenessProbe:
            failureThreshold: 30
            tcpSocket:
              port: web

          readinessProbe:
            failureThreshold: 30
            tcpSocket:
              port: web

          podSecurityContext: {}
            # fsGroup: 2000

          securityContext: {}
            # capabilities:
            #   drop:
            #   - ALL
            # readOnlyRootFilesystem: true
            # runAsNonRoot: true
            # runAsUser: 1000

          service:
            type: ClusterIP
            web:
              port: 8082

          resources: {}
            # We usually recommend not to specify default resources and to leave this as a conscious
            # choice for the user. This also increases chances charts run on environments with little
            # resources, such as Minikube. If you do want to specify resources, uncomment the following
            # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
            # limits:
            #   cpu: 100m
            #   memory: 128Mi
            # requests:
            #   cpu: 100m
            #   memory: 128Mi

          persistence:
            storageClassName: jumpserver-data
            accessModes:
              - ReadWriteMany
            size: 10Gi
            # annotations: {}
            finalizers:
              - kubernetes.io/pvc-protection

          volumeMounts: []

          volumes: []

          nodeSelector: {}

          tolerations: []

          affinity: {}

        razor:
          labels:
            app.jumpserver.org/name: jms-razor

          config:
            log:
              level: ERROR

          replicaCount: 1

          image:
            registry: registry.fit2cloud.com
            repository: jumpserver/razor
            tag: {{ jumpserver.version }}
            pullPolicy: IfNotPresent

          command: []

          env: []

          livenessProbe:
            failureThreshold: 30
            tcpSocket:
              port: rdp

          readinessProbe:
            failureThreshold: 30
            tcpSocket:
              port: rdp

          podSecurityContext: {}
            # fsGroup: 2000

          securityContext: {}
            # capabilities:
            #   drop:
            #   - ALL
            # readOnlyRootFilesystem: true
            # runAsNonRoot: true
            # runAsUser: 1000

          service:
            type: ClusterIP
            rdp:
              port: 3389

          resources: {}
            # We usually recommend not to specify default resources and to leave this as a conscious
            # choice for the user. This also increases chances charts run on environments with little
            # resources, such as Minikube. If you do want to specify resources, uncomment the following
            # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
            # limits:
            #   cpu: 100m
            #   memory: 128Mi
            # requests:
            #   cpu: 100m
            #   memory: 128Mi

          persistence:
            storageClassName: jumpserver-data
            accessModes:
              - ReadWriteMany
            size: 50Gi
            # annotations: {}
            finalizers:
              - kubernetes.io/pvc-protection

          volumeMounts: []

          volumes: []

          nodeSelector: {}

          tolerations: []

          affinity: {}

        web:
          enabled: true

          labels:
            app.jumpserver.org/name: jms-web

          replicaCount: 1

          image:
            registry: docker.io
            repository: jumpserver/web
            tag: {{ jumpserver.version }}
            pullPolicy: IfNotPresent

          command: []

          env: []
            # nginx client_max_body_size, default 4G
            # CLIENT_MAX_BODY_SIZE: 4096m

          livenessProbe:
            failureThreshold: 30
            httpGet:
              path: /api/health/
              port: web

          readinessProbe:
            failureThreshold: 30
            httpGet:
              path: /api/health/
              port: web

          podSecurityContext: {}
            # fsGroup: 2000

          securityContext: {}
            # capabilities:
            #   drop:
            #   - ALL
            # readOnlyRootFilesystem: true
            # runAsNonRoot: true
            # runAsUser: 1000

          service:
            type: ClusterIP
            web:
              port: 80

          resources: {}
            # We usually recommend not to specify default resources and to leave this as a conscious
            # choice for the user. This also increases chances charts run on environments with little
            # resources, such as Minikube. If you do want to specify resources, uncomment the following
            # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
            # limits:
            #   cpu: 100m
            #   memory: 128Mi
            # requests:
            #   cpu: 100m
            #   memory: 128Mi

          persistence:
            storageClassName: jumpserver-data
            accessModes:
              - ReadWriteMany
            size: 1Gi
            # annotations: {}
            finalizers:
              - kubernetes.io/pvc-protection

          volumeMounts: []

          volumes: []

          nodeSelector: {}

          tolerations: []

          affinity: {}
        ```
        ```sh
        # 安装
        helm install jms-k8s jumpserver/jumpserver -n default -f values.yaml

        # 卸载
        helm uninstall jms-k8s -n default
        ```

=== "[源码部署](../dev/build.md)"

=== "[Allinone](https://github.com/jumpserver/Dockerfile/tree/master/allinone){:target="_blank"}"

### 离线安装

| OS      | Architecture | Arch    | Offline Name                                                                                 |
| :------ | :----------- | :------ | :------------------------------------------------------------------------------------------- |
| Linux   | x86_64       | amd64   | jumpserver-offline-installer-{{ jumpserver.version }}-amd64-{{ installer.version }}.tar.gz   |
| Linux   | aarch64      | arm64   | jumpserver-offline-installer-{{ jumpserver.version }}-arm64-{{ installer.version }}.tar.gz   |
| Linux   | loongarch64  | loong64 | jumpserver-offline-installer-{{ jumpserver.version }}-loong64-{{ installer.version }}.tar.gz |

=== "linux/amd64"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.version }}-amd64-{{ installer.version }}.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.version }}-amd64-{{ installer.version }}
        ```
        ```sh
        # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
        cat config-example.txt
        ```
        ```vim
        # 以下设置如果为空系统会自动生成随机字符串填入
        ## 迁移请修改 SECRET_KEY 和 BOOTSTRAP_TOKEN 为原来的设置
        ## 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ## 安装配置, amd64 默认使用华为云加速下载, arm64 请注释掉 DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        # DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        VOLUME_DIR=/opt/jumpserver
        DOCKER_DIR=/var/lib/docker
        SECRET_KEY=
        BOOTSTRAP_TOKEN=
        LOG_LEVEL=ERROR

        ##  MySQL 配置, USE_EXTERNAL_MYSQL=1 表示使用外置数据库, 请输入正确的 MySQL 信息
        USE_EXTERNAL_MYSQL=0
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        ##  Redis 配置, USE_EXTERNAL_REDIS=1 表示使用外置数据库, 请输入正确的 Redis 信息
        USE_EXTERNAL_REDIS=0
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        ## Compose 项目设置, 如果 192.168.250.0/24 网段与你现有网段冲突, 请修改然后重启 JumpServer
        COMPOSE_PROJECT_NAME=jms
        COMPOSE_HTTP_TIMEOUT=3600
        DOCKER_CLIENT_TIMEOUT=3600
        DOCKER_SUBNET=192.168.250.0/24

        ## IPV6 设置, 容器是否开启 ipv6 nat, USE_IPV6=1 表示开启, 为 0 的情况下 DOCKER_SUBNET_IPV6 定义不生效
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

        ## 访问配置
        HTTP_PORT=80
        SSH_PORT=2222
        MAGNUS_MYSQL_PORT=33060
        MAGNUS_MARIADB_PORT=33061

        ## HTTPS 配置, 参考 https://docs.jumpserver.org/zh/master/admin-guide/proxy/ 配置
        # USE_LB=1
        # HTTPS_PORT=443
        # SERVER_NAME=your_domain_name
        # SSL_CERTIFICATE=your_cert
        # SSL_CERTIFICATE_KEY=your_cert_key

        ## Nginx 文件上传大小
        CLIENT_MAX_BODY_SIZE=4096m

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0
        RDP_PORT=3389
        MAGNUS_POSTGRE_PORT=54320
        TCP_SEND_BUFFER_BYTES=4194304
        TCP_RECV_BUFFER_BYTES=6291456

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=True 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=True

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080
        JUMPSERVER_ENABLE_FONT_SMOOTHING=True

        ## 终端使用宿主 HOSTNAME 标识
        SERVER_HOSTNAME=${HOSTNAME}

        # 额外的配置
        CURRENT_VERSION=
        ```
        ```sh
        # 安装
        ./jmsctl.sh install

        # 启动
        ./jmsctl.sh start
        ```
    !!! tip ""
        ```sh
        # 安装完成后配置文件 /opt/jumpserver/config/config.txt
        ```
        ```sh
        cd jumpserver-offline-release-{{ jumpserver.version }}-amd64-{{ installer.version }}

        # 启动
        ./jmsctl.sh start

        # 停止
        ./jmsctl.sh down

        # 卸载
        ./jmsctl.sh uninstall

        # 帮助
        ./jmsctl.sh -h
        ```

=== "linux/arm64"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/arm64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.version }}-arm64-{{ installer.version }}.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.version }}-arm64-{{ installer.version }}
        ```
        ```sh
        # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
        cat config-example.txt
        ```
        ```vim
        # 以下设置如果为空系统会自动生成随机字符串填入
        ## 迁移请修改 SECRET_KEY 和 BOOTSTRAP_TOKEN 为原来的设置
        ## 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ## 安装配置, amd64 默认使用华为云加速下载, arm64 请注释掉 DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        # DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        VOLUME_DIR=/opt/jumpserver
        DOCKER_DIR=/var/lib/docker
        SECRET_KEY=
        BOOTSTRAP_TOKEN=
        LOG_LEVEL=ERROR

        ##  MySQL 配置, USE_EXTERNAL_MYSQL=1 表示使用外置数据库, 请输入正确的 MySQL 信息
        USE_EXTERNAL_MYSQL=0
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        ##  Redis 配置, USE_EXTERNAL_REDIS=1 表示使用外置数据库, 请输入正确的 Redis 信息
        USE_EXTERNAL_REDIS=0
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        ## Compose 项目设置, 如果 192.168.250.0/24 网段与你现有网段冲突, 请修改然后重启 JumpServer
        COMPOSE_PROJECT_NAME=jms
        COMPOSE_HTTP_TIMEOUT=3600
        DOCKER_CLIENT_TIMEOUT=3600
        DOCKER_SUBNET=192.168.250.0/24

        ## IPV6 设置, 容器是否开启 ipv6 nat, USE_IPV6=1 表示开启, 为 0 的情况下 DOCKER_SUBNET_IPV6 定义不生效
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

        ## 访问配置
        HTTP_PORT=80
        SSH_PORT=2222
        MAGNUS_MYSQL_PORT=33060
        MAGNUS_MARIADB_PORT=33061

        ## HTTPS 配置, 参考 https://docs.jumpserver.org/zh/master/admin-guide/proxy/ 配置
        # USE_LB=1
        # HTTPS_PORT=443
        # SERVER_NAME=your_domain_name
        # SSL_CERTIFICATE=your_cert
        # SSL_CERTIFICATE_KEY=your_cert_key

        ## Nginx 文件上传大小
        CLIENT_MAX_BODY_SIZE=4096m

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0
        RDP_PORT=3389
        MAGNUS_POSTGRE_PORT=54320
        TCP_SEND_BUFFER_BYTES=4194304
        TCP_RECV_BUFFER_BYTES=6291456

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=True 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=True

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080
        JUMPSERVER_ENABLE_FONT_SMOOTHING=True

        ## 终端使用宿主 HOSTNAME 标识
        SERVER_HOSTNAME=${HOSTNAME}

        # 额外的配置
        CURRENT_VERSION=
        ```
        ```sh
        # 安装
        ./jmsctl.sh install

        # 启动
        ./jmsctl.sh start
        ```
    !!! tip ""
        ```sh
        # 安装完成后配置文件 /opt/jumpserver/config/config.txt
        ```
        ```sh
        cd jumpserver-offline-release-{{ jumpserver.version }}-arm64-{{ installer.version }}

        # 启动
        ./jmsctl.sh start

        # 停止
        ./jmsctl.sh down

        # 卸载
        ./jmsctl.sh uninstall

        # 帮助
        ./jmsctl.sh -h
        ```

=== "linux/loong64"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/loong64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.version }}-loong64-{{ installer.version }}.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.version }}-loong64-{{ installer.version }}
        ```
        ```sh
        # 根据需要修改配置文件模板, 如果不清楚用途可以跳过修改
        cat config-example.txt
        ```
        ```vim
        # 以下设置如果为空系统会自动生成随机字符串填入
        ## 迁移请修改 SECRET_KEY 和 BOOTSTRAP_TOKEN 为原来的设置
        ## 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ## 安装配置, amd64 默认使用华为云加速下载, arm64 请注释掉 DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        # DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        VOLUME_DIR=/opt/jumpserver
        DOCKER_DIR=/var/lib/docker
        SECRET_KEY=
        BOOTSTRAP_TOKEN=
        LOG_LEVEL=ERROR

        ##  MySQL 配置, USE_EXTERNAL_MYSQL=1 表示使用外置数据库, 请输入正确的 MySQL 信息
        USE_EXTERNAL_MYSQL=0
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        ##  Redis 配置, USE_EXTERNAL_REDIS=1 表示使用外置数据库, 请输入正确的 Redis 信息
        USE_EXTERNAL_REDIS=0
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        ## Compose 项目设置, 如果 192.168.250.0/24 网段与你现有网段冲突, 请修改然后重启 JumpServer
        COMPOSE_PROJECT_NAME=jms
        COMPOSE_HTTP_TIMEOUT=3600
        DOCKER_CLIENT_TIMEOUT=3600
        DOCKER_SUBNET=192.168.250.0/24

        ## IPV6 设置, 容器是否开启 ipv6 nat, USE_IPV6=1 表示开启, 为 0 的情况下 DOCKER_SUBNET_IPV6 定义不生效
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=fc00:1010:1111:200::/64

        ## 访问配置
        HTTP_PORT=80
        SSH_PORT=2222
        MAGNUS_MYSQL_PORT=33060
        MAGNUS_MARIADB_PORT=33061

        ## HTTPS 配置, 参考 https://docs.jumpserver.org/zh/master/admin-guide/proxy/ 配置
        # USE_LB=1
        # HTTPS_PORT=443
        # SERVER_NAME=your_domain_name
        # SSL_CERTIFICATE=your_cert
        # SSL_CERTIFICATE_KEY=your_cert_key

        ## Nginx 文件上传大小
        CLIENT_MAX_BODY_SIZE=4096m

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0
        RDP_PORT=3389
        MAGNUS_POSTGRE_PORT=54320
        TCP_SEND_BUFFER_BYTES=4194304
        TCP_RECV_BUFFER_BYTES=6291456

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=True 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=True

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080
        JUMPSERVER_ENABLE_FONT_SMOOTHING=True

        ## 终端使用宿主 HOSTNAME 标识
        SERVER_HOSTNAME=${HOSTNAME}

        # 额外的配置
        CURRENT_VERSION=
        ```
        ```sh
        # 安装
        ./jmsctl.sh install

        # 启动
        ./jmsctl.sh start
        ```
    !!! tip ""
        ```sh
        # 安装完成后配置文件 /opt/jumpserver/config/config.txt
        ```
        ```sh
        cd jumpserver-offline-release-{{ jumpserver.version }}-loong64-{{ installer.version }}

        # 启动
        ./jmsctl.sh start

        # 停止
        ./jmsctl.sh down

        # 卸载
        ./jmsctl.sh uninstall

        # 帮助
        ./jmsctl.sh -h
        ```

更多内容参考 [安全建议](install_security.md) [快速入门](../../admin-guide/quick_start/)  
