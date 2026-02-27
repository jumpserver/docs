# Online Installation

## 1 Environment Requirements

- Kubernetes 1.20+
- Helm 3.0

## 2 Install and Deploy
### 2.1 Add JumpServer Helm Repository
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
    | externalDatabase.password | External database password                      | postgres                |
    | externalDatabase.database | External database name                          | jumpserver              |
    | core.env.DOMAINS          | CSRF_TRUSTED_ORIGINS                            | "test.jumpserver.org"   |

### 2.2 Edit JumpServer values.yaml File
!!! tip ""
    ```sh
    helm show values jumpserver/jumpserver > values.yaml
    vim values.yaml
    ```

### 2.3 Install JumpServer

!!! tip ""
    ```sh
    helm install jms-k8s jumpserver/jumpserver -n default -f values.yaml
    ```

### 2.4 Uninstall JumpServer

!!! tip ""
    ```sh
    helm uninstall jms-k8s -n default
    ```
