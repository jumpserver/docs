# 在线安装

??? info "国内可以使用由 [华为云](https://www.huaweicloud.com/) 提供的容器镜像服务"
    | 区域          | 镜像仓库地址                         | 配置文件 /opt/jumpserver/config/config.txt                | Kubernetes values.yaml                           | OS/ARCH        |
    | :----------- | :----------------------------------- | -------------------------------------------------------- | ------------------------------------------------ | -------------- |
    | 华北-北京一   | swr.cn-north-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com     | repository: swr.cn-north-1.myhuaweicloud.com     | linux/amd64    |
    | 华南-广州     | swr.cn-south-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com     | repository: swr.cn-south-1.myhuaweicloud.com     | linux/amd64    |
    | 华北-北京四   | swr.cn-north-4.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-4.myhuaweicloud.com     | repository: swr.cn-north-4.myhuaweicloud.com     | linux/arm64    |
    | 华东-上海一   | swr.cn-east-3.myhuaweicloud.com      | DOCKER_IMAGE_PREFIX=swr.cn-east-3.myhuaweicloud.com      | repository: swr.cn-east-3.myhuaweicloud.com      | linux/arm64    |
    | 西南-贵阳一   | swr.cn-southwest-2.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-1.myhuaweicloud.com | repository: swr.ap-southeast-1.myhuaweicloud.com | linux/loong64  |

## 1 环境要求

- Kubernetes 1.20+
- Helm 3.0

## 2 安装部署
### 2.1 添加 JumpServer 的 Helm 源地址
!!! tip ""
    ```sh
    helm repo add jumpserver https://jumpserver.github.io/helm-charts
    helm repo list
    ```

### 2.2 编辑 JumpServer values.yaml 文件
!!! tip ""
    ```sh
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
      imageRegistry: ghcr.io
      imageOwner: jumpserver
      ## E.g.
      #  imagePullSecrets:
      #  - myRegistryKeySecretName
      ##
      imagePullSecrets: []
      storageClass: ""

    ## Please configure your MySQL server first
    ## Jumpserver will not start the external MySQL server.
    ##
    externalDatabase:
      engine: mysql
      host: localhost
      port: 3306
      user: root
      password: ""
      database: jumpserver

    ## Please configure your Redis server first
    ## Jumpserver will not start the external Redis server.
    ##
    externalSentinel: {}
      # hosts: mymaster/localhost:26379,localhost:26380,localhost:26381
      # password: ""
      # socketTimeout: 5

    ## Sentinel or Redis one of them must be configured.

    externalRedis:
      host: localhost
      port: 6379
      password: ""

    serviceAccount:
      ## Specifies whether a service account should be created
      create: false
      ## The name of the service account to use.
      ## If not set and create is true, a name is generated using the fullname template
      name:

    ingress:
      enabled: true
      annotations:
        # kubernetes.io/tls-acme: "true"
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-body-size: "4096m"
        nginx.ingress.kubernetes.io/server-snippets: |
          proxy_set_header Upgrade "websocket";
          proxy_set_header Connection "Upgrade";
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

      hosts:
        - "test.jumpserver.org"
      tls: []
      #  - secretName: chart-example-tls
      #    hosts:
      #      - chart-example.local

    core:
      enabled: true

      labels:
        app.jumpserver.org/name: jms-core

      config:
        ## Generate a new random secret key by execute `cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 50`
        secretKey: ""
        ## Generate a new random bootstrap token by execute `cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 24`
        bootstrapToken: ""
        ## Enabled it for debug
        debug: false
        log:
          level: ERROR

      replicaCount: 1

      image:
        registry: docker.io
        pullPolicy: IfNotPresent

      env:
        ## See: https://docs.jumpserver.org/zh/master/admin-guide/env/#core
        SESSION_EXPIRE_AT_BROWSER_CLOSE: true
        # SESSION_COOKIE_AGE: 86400
        # SECURITY_VIEW_AUTH_NEED_MFA: true
        ## Django CSRF_TRUSTED_ORIGINS need to be set to the domain name of the jumpserver (https://docs.jumpserver.org/zh/v3/installation/upgrade_notice/)
        # DOMAINS: "demo.jumpserver.org:443, 172.17.200.11:80"

      livenessProbe:
        initialDelaySeconds: 90
        failureThreshold: 3
        timeoutSeconds: 5
        exec:
          command:
          - curl
          - -fsL
          - http://localhost:8080/api/health/

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

      resources: {}
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

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
        pullPolicy: IfNotPresent

      env: []
        ## See: https://docs.jumpserver.org/zh/master/admin-guide/env/#koko
        # LANGUAGE_CODE: zh
        # REUSE_CONNECTION: true
        # ENABLE_LOCAL_PORT_FORWARD: true
        # ENABLE_VSCODE_SUPPORT: true

      livenessProbe:
        initialDelaySeconds: 10
        failureThreshold: 3
        timeoutSeconds: 5
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
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

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
        pullPolicy: IfNotPresent

      env:
        ## See: https://docs.jumpserver.org/zh/master/admin-guide/env/#lion
        JUMPSERVER_ENABLE_FONT_SMOOTHING: true
        # JUMPSERVER_COLOR_DEPTH: 32
        # JUMPSERVER_ENABLE_WALLPAPER: true
        # JUMPSERVER_ENABLE_THEMING: true
        # JUMPSERVER_ENABLE_FULL_WINDOW_DRAG: true
        # JUMPSERVER_ENABLE_DESKTOP_COMPOSITION: true
        # JUMPSERVER_ENABLE_MENU_ANIMATIONS: true

      livenessProbe:
        initialDelaySeconds: 90
        failureThreshold: 3
        timeoutSeconds: 5
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
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

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
        pullPolicy: IfNotPresent

      env: []

      livenessProbe:
        initialDelaySeconds: 10
        failureThreshold: 3
        timeoutSeconds: 5
        tcpSocket:
          port: 9090

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
          port: 33061
        mariadb:
          port: 33062
        redis:
          port: 63790
        postgresql:
          port: 54320
        sqlserver:
          port: 14330
        oracle:
          ports: 30000-30100

      resources: {}
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

      volumeMounts: []

      volumes: []

      nodeSelector: {}

      tolerations: []

      affinity: {}

    chen:
      enabled: true

      labels:
        app.jumpserver.org/name: jms-chen

      config:
        log:
          level: ERROR

      replicaCount: 1

      image:
        registry: docker.io
        pullPolicy: IfNotPresent

      env: []

      livenessProbe:
        initialDelaySeconds: 60
        failureThreshold: 3
        timeoutSeconds: 5
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
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

      volumeMounts: []

      volumes: []

      nodeSelector: {}

      tolerations: []

      affinity: {}

    kael:
      enabled: true

      labels:
        app.jumpserver.org/name: jms-kael

      config:
        log:
          level: ERROR

      replicaCount: 1

      image:
        registry: docker.io
        pullPolicy: IfNotPresent

      env: []

      livenessProbe:
        initialDelaySeconds: 10
        failureThreshold: 3
        timeoutSeconds: 5
        httpGet:
          path: /kael/health/
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
          port: 8083

      resources: {}
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

      volumeMounts: []

      volumes: []

      nodeSelector: {}

      tolerations: []

      affinity: {}

    xpack:
      enabled: false

    xrdp:
      labels:
        app.jumpserver.org/name: jms-xrdp

      config:
        log:
          level: ERROR

      replicaCount: 1

      image:
        registry: registry.fit2cloud.com
        pullPolicy: IfNotPresent

      env: []

      livenessProbe:
        initialDelaySeconds: 10
        failureThreshold: 3
        timeoutSeconds: 5
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
          port: 3390

      resources: {}
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

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
        pullPolicy: IfNotPresent

      env: []

      livenessProbe:
        initialDelaySeconds: 10
        failureThreshold: 3
        timeoutSeconds: 5
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
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

      volumeMounts: []

      volumes: []

      nodeSelector: {}

      tolerations: []

      affinity: {}

    video:
      labels:
        app.jumpserver.org/name: jms-video

      config:
        log:
          level: ERROR

      replicaCount: 1

      image:
        registry: registry.fit2cloud.com
        pullPolicy: IfNotPresent

      env: []

      livenessProbe:
        initialDelaySeconds: 10
        failureThreshold: 3
        timeoutSeconds: 5
        httpGet:
          path: /video-worker/health/
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
        service:
        type: ClusterIP
        web:
          port: 9000

      resources: {}
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

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
        pullPolicy: IfNotPresent

      env:
        # nginx client_max_body_size, default 4G
        CLIENT_MAX_BODY_SIZE: 4096m
        ## See: https://github.com/jumpserver/docker-web/blob/master/init.sh#L37
        # USE_LB: 1, then nginx use 'proxy_set_header X-Forwarded-For $remote_addr'
        # USE_LB: 0, then nginx use 'proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for'
        USE_LB: 0

      livenessProbe:
        initialDelaySeconds: 10
        failureThreshold: 3
        timeoutSeconds: 5
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
        ## We usually recommend not to specify default resources and to leave this as a conscious
        ## choice for the user. This also increases chances charts run on environments with little
        ## resources, such as Minikube. If you do want to specify resources, uncomment the following
        ## lines, adjust them as necessary, and remove the curly braces after 'resources:'.
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
        annotations:
          "helm.sh/resource-policy": keep
        finalizers:
          - kubernetes.io/pvc-protection
        # subPath: ""
        # existingClaim: ""

      volumeMounts: []

      volumes: []

      nodeSelector: {}

      tolerations: []

      affinity: {}
    ```

### 2.3 安装 JumpServer

!!! tip ""
    ```sh
    helm install jms-k8s jumpserver/jumpserver -n default -f values.yaml
    ```

### 2.4 卸载 JumpServer

!!! tip ""
    ```sh
    helm uninstall jms-k8s -n default
    ```
