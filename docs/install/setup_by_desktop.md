# Docker Desktop

!!! info "环境要求"

| OS      | OS Version | Soft Requirement                                                                                           |
| :-------| :----------| :--------------------------------------------------------------------------------------------------------- |
| Windows | >= 10      | [Git](https://git-scm.com/download/win) [Docker Desktop](https://docs.docker.com/desktop/windows/install/) |
| macOS   | >= 10.14   | Git [Docker Desktop](https://docs.docker.com/desktop/mac/install/)                                         |

## 部署说明

!!! warning "先正确安装 Git 和 Docker Desktop"

!!! tip ""
    === "Windows"
        ```sh
        # Run from Git Bash
        git clone https://github.com/jumpserver/Dockerfile ~/jumpserver
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

    === "macOS"
        ```sh
        git clone https://github.com/jumpserver/Dockerfile ~/jumpserver
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
        VOLUME_DIR=/opt/jumpserver

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

## 升级步骤

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致，否则会导致数据库加密数据无法解密"
    - 更新前请一定要做好备份工作

!!! tip "备份数据库"
    ```sh
    docker exec -it jms_core bash
    mysqldump --skip-lock-tables --single-transaction --host=${DB_HOST} --port=${DB_PORT} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} > /opt/jumpserver.sql
    exit
    docker cp jms_core:/opt/jumpserver.sql ~/jumpserver/jumpserver.sql
    ```

!!! tip "修改版本号"
    ```sh
    cd ~/jumpserver
    vi .env
    ```
    ```vim
    # 修改版本号为你要升级的版本, 其他选项保持默认
    Version={{ jumpserver.version }}
    ```

!!! tip ""
    === "内置数据库升级"
        ```sh
        cd ~/jumpserver
        docker-compose -f docker-compose-network.yml -f docker-compose-redis.yml -f docker-compose-mariadb.yml -f docker-compose.yml down -v
        docker-compose -f docker-compose-network.yml -f docker-compose-redis.yml -f docker-compose-mariadb.yml -f docker-compose-init-db.yml up -d
        docker exec -i jms_core bash -c './jms upgrade_db'
        docker-compose -f docker-compose-network.yml -f docker-compose-redis.yml -f docker-compose-mariadb.yml -f docker-compose.yml up -d
        ```
    === "外置数据库升级"
        ```sh
        cd ~/jumpserver
        docker-compose -f docker-compose-network.yml -f docker-compose.yml down -v
        docker-compose -f docker-compose-network.yml -f docker-compose-init-db.yml up -d
        docker exec -i jms_core bash -c './jms upgrade_db'
        docker-compose -f docker-compose-network.yml -f docker-compose.yml up -d
        ```
