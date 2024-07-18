# 在线安装

??? info "可以使用由 [华为云](https://www.huaweicloud.com/) 提供的容器镜像服务"
    | 区域          | 镜像仓库地址                         | Kubernetes values.yaml                              | OS/ARCH        |
    | :----------- | :----------------------------------- | --------------------------------------------------- | -------------- |
    | 华北-北京一   | swr.cn-north-1.myhuaweicloud.com     | imageRegistry: swr.cn-north-1.myhuaweicloud.com     | linux/amd64    |
    | 华南-广州     | swr.cn-south-1.myhuaweicloud.com     | imageRegistry: swr.cn-south-1.myhuaweicloud.com     | linux/amd64    |
    | 华北-北京四   | swr.cn-north-4.myhuaweicloud.com     | imageRegistry: swr.cn-north-4.myhuaweicloud.com     | linux/arm64    |
    | 华东-上海一   | swr.cn-east-3.myhuaweicloud.com      | imageRegistry: swr.cn-east-3.myhuaweicloud.com      | linux/arm64    |
    | 西南-贵阳一   | swr.cn-southwest-2.myhuaweicloud.com | imageRegistry: swr.ap-southeast-1.myhuaweicloud.com | linux/loong64  |
    | 拉美-圣保罗一 | swr.sa-brazil-1.myhuaweicloud.com    | imageRegistry: swr.sa-brazil-1.myhuaweicloud.com    | linux/s390x    |

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

!!! tip ""
    | Name                      | Description                                     | Value                   |
    | :------------------------ | :---------------------------------------------- | :---------------------- |
    | global.imageRegistry      | Global Docker image registry                    | docker.io               |
    | global.imageOwner         | Global Docker image owner                       | jumpserver              |
    | global.imagePullSecrets   | Global Docker registry secret names as an array | []                      |
    | global.storageClass       | Global StorageClass for Persistent Volume(s)    | ""                      |
    | externalDatabase.engine   | External database engine                        | postgresql              |
    | externalDatabase.host     | External database host                          | localhost               |
    | externalDatabase.port     | External database port                          | 5432                    |
    | externalDatabase.user     | External database user                          | postgres                |
    | externalDatabase.password | External database password                      | ""                      |
    | externalDatabase.database | External database name                          | jumpserver              |
    | externalRedis.host        | External Redis host                             | localhost               |
    | externalRedis.port        | External Redis port                             | 6379                    |
    | externalRedis.password    | External Redis password                         | ""                      |
    | ingress.enabled           | Enable ingress                                  | true                    |
    | ingress.hosts             | Ingress hosts                                   | ["test.jumpserver.org"] |
    | core.config.secretKey     | Core secret key                                 | ""                      |
    | core.config.bootstrapToken| Core bootstrap token                            | ""                      |
    | core.env.DOMAINS          | CSRF_TRUSTED_ORIGINS                            | "test.jumpserver.org    |

### 2.2 编辑 JumpServer values.yaml 文件
!!! tip ""
    ```sh
    vi values.yaml
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
