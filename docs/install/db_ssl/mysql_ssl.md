# 数据库 SSL 连接

## 1 操作过程
### 1.1 准备数据库 CA 文件
!!! tip ""
    - 准备好数据库 CA 文件, 当前不支持私钥认证。

    ```bash
    mkdir -p /opt/jumpserver/config/certs
    cp db_ca.pem /opt/jumpserver/config/certs/db_ca.pem
    ```
    
    - 测试 MySQL 连接无误。

    ```bash
    # . /opt/jumpserver/config/config.txt
    # mysql --ssl-ca=/opt/jumpserver/config/certs/db_ca.pem -h$DB_HOST -P$DB_PORT -U$DB_USER -p$DB_PASSWORD $DB_NAME
    ```

### 1.2 编辑配置文件
!!! tip ""
    - 打开配置文件。

    ```bash
    vi /opt/jumpserver/config/config.txt
    ```

    - 在配置文件配置使用 DB SSL。

    ```vim
    DB_USE_SSL=True
    ```
    
### 1.3 重启 JumpServer 服务
!!! tip ""
    ```bash
    cd /opt/jumpserver-installer-{{ jumpserver.tag }}
    ./jmsctl.sh down
    ./jmsctl.sh start
    ```

!!! warning "其他方式部署的 JumpServer 请将数据库证书 db_ca.pem 放到 /opt/jumpserver/data/certs 后重启即可"