# 升级操作

## 1 准备工作
### 1.1 查询定义的 JumpServer 配置
!!! tip ""
    ```sh
    docker exec -it jms_all env
    ```

### 1.2 停止 JumpServer
!!! tip ""
    ```sh
    docker stop jms_all
    ```

### 1.3 数据库备份
!!! tip "提示"
    - 下面用到的 DB-xxx 从上面的 docker exec -it jms_all env 结果获取。
    - 例: mysqldump -h192.168.100.11 -p3306 -ujumpserver -pnu4x599Wq7u0Bn8EABh3J91G jumpserver > /opt/jumpserver-v2.12.0.sql
    
!!! tip ""
    ```sh
    mysqldump -h$DB_HOST -p$DB_PORT -u$DB_USER -p$DB_PASSWORD $DB_NAME > /opt/jumpserver-<版本号>.sql
    ```

## 2 环境升级
### 2.1 拉取新版本镜像
!!! tip ""
    ```sh
    docker pull jumpserver/jms_all:v2.28.6
    ```

### 2.2 删掉旧版本容器
!!! tip ""
    ```sh
    docker rm jms_all
    ```

### 2.3 处理数据库合并
!!! tip ""
    ```sh
    docker run --name jms_all --rm \
      -v /opt/jumpserver/core/data:/opt/jumpserver/data \
      -v /opt/jumpserver/koko/data:/opt/koko/data \
      -v /opt/jumpserver/lion/data:/opt/lion/data \
      -e SECRET_KEY=****** \                 # 自行修改成你的旧版本 SECRET_KEY, 丢失此 key 会导致数据无法解密
      -e BOOTSTRAP_TOKEN=****** \            # 自行修改成你的旧版本 BOOTSTRAP_TOKEN
      -e LOG_LEVEL=ERROR \
      -e DB_HOST=192.168.x.x \               # 自行修改成你的旧版本 MySQL 服务器, 设置不对数据丢失
      -e DB_PORT=3306 \
      -e DB_USER=jumpserver \
      -e DB_PASSWORD=****** \
      -e DB_NAME=jumpserver \
      -e REDIS_HOST=192.168.x.x \            # 自行修改成你的旧版本 Redis 服务器
      -e REDIS_PORT=6379 \
      -e REDIS_PASSWORD=****** \
      jumpserver/jms_all:v2.28.6 upgrade     # 确定无报错
    ```

### 2.4 启动新版本
!!! tip ""
    ```sh
    docker run --name jms_all -d \
      -v /opt/jumpserver/core/data:/opt/jumpserver/data \
      -v /opt/jumpserver/koko/data:/opt/koko/data \
      -v /opt/jumpserver/lion/data:/opt/lion/data \
      -p 80:80 \
      -p 2222:2222 \
      -p 30000-30100:30000-30100 \
      -e SECRET_KEY=****** \                 # 自行修改成你的旧版本 SECRET_KEY, 丢失此 key 会导致数据无法解密
      -e BOOTSTRAP_TOKEN=****** \            # 自行修改成你的旧版本 BOOTSTRAP_TOKEN
      -e LOG_LEVEL=ERROR \
      -e DB_HOST=192.168.x.x \               # 自行修改成你的旧版本 MySQL 服务器, 设置不对数据丢失
      -e DB_PORT=3306 \
      -e DB_USER=jumpserver \
      -e DB_PASSWORD=****** \
      -e DB_NAME=jumpserver \
      -e REDIS_HOST=192.168.x.x \            # 自行修改成你的旧版本 Redis 服务器
      -e REDIS_PORT=6379 \
      -e REDIS_PASSWORD=****** \
      --privileged=true \
      jumpserver/jms_all:v2.28.6
    ```