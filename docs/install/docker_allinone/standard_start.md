# 标准启动

## 1 环境说明
!!! tip "提示"
    - 使用外置 MySQL 数据库和 Redis。
    - 外置数据库要求 MySQL 版本大于等于 5.7
    - 外置 Redis 要求 Redis 版本大于等于 6.0

## 2 数据库环境准备
### 2.1 创建 MySQL 数据库
!!! tip "提示"
    - 自行部署 MySQL 可以参考 [MySQL 服务部署](../linux_lb/mysql_install.md)

!!! tip ""
    - 创建 MySQL 用户并赋予权限。
    ```sh
    # 登入 MySQL 数据库
    mysql -u root -p
    ```
    ```sh
    create database jumpserver default charset 'utf8';
    create user 'jumpserver'@'%' identified by 'nu4x599Wq7u0Bn8EABh3J91G';
    grant all on jumpserver.* to 'jumpserver'@'%';
    flush privileges;
    ```

### 2.2 创建 Redis 数据库
!!! tip "提示"
    - 自行部署 Redis 可以参考 [Redis 服务部署](../linux_lb/redis_install.md)

## 3 环境部署
### 3.1 设置环境变量
!!! tip "提示"
    - 自己下面设置的这些信息一定要记录下来，升级时需要重新输入使用。
!!! tip ""
    ```sh
    - SECRET_KEY = xxxxx                # 自行生成随机的字符串, 不要包含特殊字符串, 长度推荐大于等于 50
    - BOOTSTRAP_TOKEN = xxxxx           # 自行生成随机的字符串, 不要包含特殊字符串, 长度推荐大于等于 24
    - LOG_LEVEL = ERROR                 # 日志等级, 测试环境推荐设置为 DEBUG
    
    - DB_ENGINE = mysql                 # 使用 MySQL 数据库
    - DB_HOST = mysql_host              # MySQL 数据库 IP 地址
    - DB_PORT = 3306                    # MySQL 数据库 端口
    - DB_USER = xxx                     # MySQL 数据库认证用户
    - DB_PASSWORD = xxxx                # MySQL 数据库认证密码
    - DB_NAME = jumpserver              # JumpServer 使用的数据库名称
    
    - REDIS_HOST = redis_host           # 使用 Redis 缓存
    - REDIS_PORT = 6379                 # Redis 服务器 IP 地址
    - REDIS_PASSWORD = xxxx             # Redis 认证密码
    
    - VOLUME /opt/jumpserver/data       # Core 持久化目录, 存储录像日志
    - VOLUME /opt/koko/data             # Koko 持久化目录
    - VOLUME /opt/lion/data             # Lion 持久化目录
    ```

### 3.2 初始化数据库
!!! tip ""
    ```sh
    docker run --name jms_all --rm \
      -v /opt/jumpserver/core/data:/opt/jumpserver/data \
      -v /opt/jumpserver/koko/data:/opt/koko/data \
      -v /opt/jumpserver/lion/data:/opt/lion/data \
      -e SECRET_KEY=xxxxxx \
      -e BOOTSTRAP_TOKEN=xxxxxx \
      -e LOG_LEVEL=ERROR \
      -e DB_HOST=192.168.x.x \
      -e DB_PORT=3306 \
      -e DB_USER=jumpserver \
      -e DB_PASSWORD=weakPassword \
      -e DB_NAME=jumpserver \
      -e REDIS_HOST=192.168.x.x \
      -e REDIS_PORT=6379 \
      -e REDIS_PASSWORD=weakPassword \
      jumpserver/jms_all:v2.28.6 init_db   # 确定无报错
    ```

### 3.3 启动 JumpServer
!!! tip ""
    ```sh
    docker run --name jms_all -d \
      -v /opt/jumpserver/core/data:/opt/jumpserver/data \
      -v /opt/jumpserver/koko/data:/opt/koko/data \
      -v /opt/jumpserver/lion/data:/opt/lion/data \
      -p 80:80 \
      -p 2222:2222 \
      -p 30000-30100:30000-30100 \
      -e SECRET_KEY=xxxxxx \
      -e BOOTSTRAP_TOKEN=xxxxxx \
      -e LOG_LEVEL=ERROR \
      -e DB_HOST=192.168.x.x \
      -e DB_PORT=3306 \
      -e DB_USER=jumpserver \
      -e DB_PASSWORD=weakPassword \
      -e DB_NAME=jumpserver \
      -e REDIS_HOST=192.168.x.x \
      -e REDIS_PORT=6379 \
      -e REDIS_PASSWORD=weakPassword \
      --privileged=true \
      jumpserver/jms_all:v2.28.6
    ```