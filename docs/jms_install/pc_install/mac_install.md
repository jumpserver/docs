# Mac 环境部署

## 1 环境要求
!!! tip ""
    得益于 Docker 跨平台应用，JumpServer 理论上可以部署在任何可以运行 Docker 的宿主机。

    我们并非是只支持 Linux 操作系统，我们是支持可以部署 Docker 的任意 x86_64 的宿主机（Windows / Linux / macOS）。


    | OS      | OS Version | Soft Requirement                                                                                           |
    | :-------| :----------| :--------------------------------------------------------------------------------------------------------- |
    | macOS   | >= 10.14   | Git [Docker Desktop](https://docs.docker.com/desktop/mac/install/)                                         |

## 2 安装部署
!!! warning "先正确安装 Git 和 Docker Desktop"

### 2.1 Git clone 项目文件
!!! tip ""
    ```sh
    git clone https://github.com/jumpserver/Dockerfile ~/jumpserver
    ```

### 2.2 编辑环境变量
!!! tip ""
    ```sh
    cd ~/jumpserver
    cp config_example.conf .env
    vi .env
    ```
    ```vim
    # 版本号可以自己根据项目的版本修改
    Version={{ jumpserver.version }}

    # 构建参数, 支持 amd64/arm64
    TARGETARCH=amd64

    # Compose
    COMPOSE_PROJECT_NAME=jms
    COMPOSE_HTTP_TIMEOUT=3600
    DOCKER_CLIENT_TIMEOUT=3600
    DOCKER_SUBNET=192.168.250.0/24

    # 持久化存储
    VOLUME_DIR=/d/jumpserver  # 挂载 Windows D 盘 jumpserver 目录 D:\jumpserver, 自行替换

    # MySQL, 自行修改 DB_PASSWORD
    DB_HOST=mysql
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=nu4x599Wq7u0Bn8EABh3J91G
    DB_NAME=jumpserver

    # Redis, 自行修改 REDIS_PASSWORD
    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_PASSWORD=8URXPL2x3HZMi7xoGTdk3Upj

    # Core, 自行修改 SECRET_KEY 和 BOOTSTRAP_TOKEN
    SECRET_KEY=B3f2w8P2PfxIAS7s4URrD9YmSbtqX4vXdPUL217kL9XPUOWrmy
    BOOTSTRAP_TOKEN=7Q11Vz6R2J6BLAdO
    DEBUG=False
    LOG_LEVEL=ERROR

    ##
    # SECRET_KEY 保护签名数据的密匙, 首次安装请一定要修改并牢记, 后续升级和迁移不可更改, 否则将导致加密的数据不可解密。
    # BOOTSTRAP_TOKEN 为组件认证使用的密钥, 仅组件注册时使用。组件指 koko、guacamole
    ```

### 2.3 配置数据库启动
!!! tip ""
    === "内置数据库启动"
        ```sh
        cd ~/jumpserver
        docker-compose -f docker-compose-network.yml -f docker-compose-redis.yml -f docker-compose-mariadb.yml -f docker-compose-init-db.yml up -d
        docker exec -i jms_core bash -c './jms upgrade_db'
        docker-compose -f docker-compose-network.yml -f docker-compose-redis.yml -f docker-compose-mariadb.yml -f docker-compose.yml up -d
        ```
    === "外置数据库启动"
        ```sh
        cd ~/jumpserver
        docker-compose -f docker-compose-network.yml -f docker-compose-init-db.yml up -d
        docker exec -i jms_core bash -c './jms upgrade_db'
        docker-compose -f docker-compose-network.yml -f docker-compose.yml up -d
        ```