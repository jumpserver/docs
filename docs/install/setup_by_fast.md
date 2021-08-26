# 安装文档

!!! info "说明"
    全新安装的 Linux  
    需要连接 互联网  
    使用 root 用户执行  

??? info "可以使用由 [华为云](https://www.huaweicloud.com/) 提供的容器镜像服务 :heart:{: .heart }"
    | 区域          | 镜像仓库地址                         | 配置文件 /opt/jumpserver/config/config.txt                | Kubernetes values.yaml                          |
    | :----------- | :----------------------------------- | -------------------------------------------------------- | ----------------------------------------------- |
    | 华北-北京一   | swr.cn-north-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com     | repository: swr.cn-north-1.myhuaweicloud.com    |
    | 华北-北京四   | swr.cn-north-4.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-4.myhuaweicloud.com     | repository: swr.cn-north-4.myhuaweicloud.com    |
    | 华南-广州     | swr.cn-south-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com     | repository: swr.cn-south-1.myhuaweicloud.com    |
    | 华东-上海一   | swr.cn-east-3.myhuaweicloud.com      | DOCKER_IMAGE_PREFIX=swr.cn-east-3.myhuaweicloud.com      | repository: swr.cn-east-3.myhuaweicloud.com      |
    | 亚太-香港     | swr.ap-southeast-1.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-1.myhuaweicloud.com | repository: swr.ap-southeast-1.myhuaweicloud.com |
    | 亚太-新加坡   | swr.ap-southeast-3.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-3.myhuaweicloud.com | repository: swr.ap-southeast-3.myhuaweicloud.com |

## 安装方式

- [安装演示视频](https://www.bilibili.com/video/bv19a4y1i7i9)

!!! info "外置环境要求"
    - 推荐使用外置 数据库 和 Redis，方便日后扩展升级

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 6.0  |
| MariaDB | >= 10.2 |    |       |         |

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
        DOCKER_SUBNET_IPV6=2001:db8:10::/64

        ## Nginx 配置, USE_LB=1 表示开启, 为 0 的情况下, HTTPS_PORT 定义不生效
        HTTP_PORT=80
        SSH_PORT=2222
        RDP_PORT=3389

        USE_LB=0
        HTTPS_PORT=443

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=true

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080

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

=== "离线部署(amd64)"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads), 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        unzip jumpserver-installer-{{ jumpserver.version }}-amd64-{{ installer.amd64 }}.zip
        cd jumpserver-installer-{{ jumpserver.version }}-amd64-{{ installer.amd64 }}
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
        DOCKER_SUBNET_IPV6=2001:db8:10::/64

        ## Nginx 配置, USE_LB=1 表示开启, 为 0 的情况下, HTTPS_PORT 定义不生效
        HTTP_PORT=80
        SSH_PORT=2222
        RDP_PORT=3389

        USE_LB=0
        HTTPS_PORT=443

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=true

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080

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

=== "离线部署(arm64)"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/arm64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads), 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        unzip jumpserver-installer-{{ jumpserver.version }}-arm64-{{ installer.arm64 }}.zip
        cd jumpserver-installer-{{ jumpserver.version }}-arm64-{{ installer.arm64 }}
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
        DOCKER_SUBNET_IPV6=2001:db8:10::/64

        ## Nginx 配置, USE_LB=1 表示开启, 为 0 的情况下, HTTPS_PORT 定义不生效
        HTTP_PORT=80
        SSH_PORT=2222
        RDP_PORT=3389

        USE_LB=0
        HTTPS_PORT=443

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=true

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080

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

=== "Kubernetes"
    !!! tip ""
        ```sh
        cd /opt
        git clone https://github.com/jumpserver/helm
        cd /opt/helm
        vi values.yaml
        ```
        ```yaml
        # Default values for jumpserver.
        # This is a YAML-formatted file.
        # Declare variables to be passed into your templates.

        nameOverride: ""
        fullnameOverride: ""

        serviceAccount:
          # Specifies whether a service account should be created
          create: false
          # The name of the service account to use.
          # If not set and create is true, a name is generated using the fullname template
          name:

        imagePullSecrets: []
        # - name: yourImagePullSecret

        ingress:
          enabled: true
          annotations:
            # kubernetes.io/tls-acme: "true"
            compute-full-forwarded-for: "true"
            use-forwarded-headers: "true"
            kubernetes.io/ingress.class: nginx
            nginx.ingress.kubernetes.io/configuration-snippet: |
               proxy_set_header Upgrade "websocket";
               proxy_set_header Connection "Upgrade";
          hosts:
            - "test.jumpserver.org"  # 通过 ingress 暴露对外域名, 自行修改成你的域名
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
            secretKey: "*************"  # 加密 key, 随机生成保管好
            # Generate a new random bootstrap token by execute `cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`
            bootstrapToken: "********"  # 组件组成使用 token
            # Enabled it for debug
            debug: false
            log:
              level: ERROR
            # Fill it with your mysql config
            db:
              engine: mysql         # mysql 相关, 自行搭建后填写对应信息
              host: "192.168.1.1"
              port: 3306
              user: jumpserver
              password: "*******"
              name: jumpserver
            # Fill it with your redis config
            redis:
              host: "192.168.1.1"  # redis 相关, 自行搭建后填写对应信息
              port: 6379
              password: "*******"

          replicaCount: 1          # 副本数, 可以通过 kebuctl scale 实时扩容

          image:
            repository: docker.io/jumpserver/core  # 镜像地址, 默认使用 docker.io
            tag: v2.13.1
            pullPolicy: IfNotPresent

          command: []

          env: []

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
            storageClassName: jumpserver-data  # 请先自行创建 SC, 然后将名称填入此处, 其他组件也要修改
            accessModes:
              - ReadWriteMany                  # 规则必须为 RWM, 多 pod 需要共同读写
            size: 10Gi                         # 生产环境推荐 100G 以上
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
            repository: docker.io/jumpserver/koko
            tag: v2.13.1
            pullPolicy: IfNotPresent

          command: []

          env: []

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
            storageClassName: jumpserver-data  # custom
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
            repository: docker.io/jumpserver/lion
            tag: v2.13.1
            pullPolicy: IfNotPresent

          command: []

          env: []

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
            storageClassName: jumpserver-data  # custom
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
          enabled: false    # 企业版 xpack, 开源版本修改无效, 请保持默认

        omnidb:
          labels:
            app.jumpserver.org/name: jms-omnidb

          config:
            log:
              level: ERROR

          replicaCount: 1

          image:
            repository: registry.fit2cloud.com/jumpserver/omnidb
            tag: v2.13.1
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
            ws:
              port: 8071

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

        xrdp:
          labels:
            app.jumpserver.org/name: jms-xrdp

          config:
            log:
              level: ERROR

          replicaCount: 1

          image:
            repository: registry.fit2cloud.com/jumpserver/xrdp
            tag: v2.13.1
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
            size: 10Gi
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
            repository: docker.io/jumpserver/web
            tag: v2.13.1
            pullPolicy: IfNotPresent

          command: []

          env: []

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
        helm install jumpserver ./ -n default

        # 卸载
        helm uninstall jumpserver -n default

        # 查看
        helm list -n default
        ```

=== "[源码部署](../dev/build.md)"

=== "[Allinone](https://github.com/jumpserver/Dockerfile/tree/master/allinone){:target="_blank"}"



后续的使用请参考 [安全建议](install_security.md) [快速入门](../../admin-guide/quick_start/)  
