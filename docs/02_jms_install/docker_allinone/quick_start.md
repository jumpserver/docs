# 快速启动
!!! tip "提示"
    - 仅在测试环境中快速部署验证功能使用。

## 1 快速入门
### 1.1 创建 Docker 容器网段
!!! tip ""
    ```sh
    docker network create jms_net --subnet=192.168.250.0/24
    ```

### 1.2 Docker 运行 MySQL 服务
!!! tip ""
    ```sh
    docker run --name jms_mysql --network jms_net -d \
      -e MARIADB_ROOT_PASSWORD=weakPassword \
      -e MARIADB_DATABASE=jumpserver \
      mariadb:10
    ```

### 1.3 Docker 运行 JumpServer 服务
!!! tip ""
    ```sh
    docker run --name jms_all --network jms_net --rm \
      -e DB_HOST=jms_mysql \
      -e DB_USER=root \
      -e DB_PASSWORD=weakPassword \
      --privileged=true \
      jumpserver/jms_all:v2.28.6 init_db
    ```
    ```sh
    docker run --name jms_all --network jms_net -d \
      -p 80:80 \
      -p 2222:2222 \
      -p 30000-30100:30000-30100 \
      -e LOG_LEVEL=ERROR \
      -e DB_HOST=jms_mysql \
      -e DB_USER=root \
      -e DB_PASSWORD=weakPassword \
      -e DB_NAME=jumpserver \
      --privileged=true \
      jumpserver/jms_all:v2.28.6
    ```

## 2 环境清理
### 2.1 测试完毕后清理环境
!!! tip ""
    ```sh
    docker stop jms_all
    docker rm jms_all
    docker stop jms_mysql
    docker rm jms_mysql
    docker volume prune -f
    docker network prune -f
    ```