# 环境升级

## 1 升级须知
!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致，否则会导致数据库加密数据无法解密"
    - 更新前请一定要做好备份工作

### 1.1 备份数据库
!!! tip ""
    ```sh
    docker exec -it jms_core bash
    mysqldump --skip-lock-tables --single-transaction --host=${DB_HOST} --port=${DB_PORT} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} > /opt/jumpserver.sql
    exit
    docker cp jms_core:/opt/jumpserver.sql ~/jumpserver/jumpserver.sql
    ```

## 2 升级过程
### 2.1 修改版本号
!!! tip ""
    ```sh
    cd ~/jumpserver
    vi .env
    ```
    ```vim
    # 修改版本号为你要升级的版本, 其他选项保持默认
    Version={{ jumpserver.tag }}
    ```

### 2.2 数据库升级
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