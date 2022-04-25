# 安全建议

!!! tip ""
    - Jumpserver 对外需要开放 80 443 2222 33060 33061 端口
    - JumpServer 所在服务器操作系统应该升级到最新  
    - JumpServer 依赖的软件升级到最新版本  
    - 服务器、数据库、redis 等依赖组件请勿使用弱口令密码  
    - 不推荐关闭 firewalld 和 selinux  
    - 只开放必要的端口，必要的话请通过 vpn 或者 sslvpn 访问 JumpServer  
    - 如果必须开放到外网使用，你应该部署 web 应用防火墙做安全过滤  
    - 请部署 ssl 证书通过 https 协议来访问 JumpServer  
    - JumpServer 不要使用弱口令密码，应立即改掉默认的 admin 密码  
    - 推荐开启 MFA 功能，避免因密码泄露导致的安全问题

!!! tip ""
    关注官方更新，及时更新修复漏洞的版本  
    如发现 JumpServer 安全问题，请反馈给我们 ibuler@fit2cloud.com

## 数据库 SSL 连接

!!! tip ""
    ```bash
    # 准备好数据库 ca 文件, 当前不支持私钥认证
    . /opt/jumpserver/config.txt
    mkdir $VOLUME_DIR/core/data/certs -p
    cp db_ca.pem $VOLUME_DIR/core/certs/db_ca.pem
    ```
    ```bash
    # 测试 mysql 连接无误
    # mysql --ssl-ca=$VOLUME_DIR/core/certs/db_ca.pem -h$DB_HOST -P$DB_PORT -U$DB_USER -p$DB_PASSWORD $DB_NAME
    ```
    ```bash
    # 然后重启 jumpserver 即可
    cd /opt/jumpserver-installer-{{ jumpserver.version }}
    ./jmsctl.sh down
    ./jmsctl.sh start
    ```

!!! warning "其他方式部署的 jumpserver 请将数据库证书 db_ca.pem 放到 /opt/jumpserver/data/certs 重启即可"

## Redis SSL 连接

=== "公钥认证"
    !!! tip ""
        ```bash
        准备好 Redis ca 文件 (云服务商一般只提供 ca 文件)
        . /opt/jumpserver/config.txt
        mkdir $VOLUME_DIR/core/data/certs -p
        cp redis_ca.crt $VOLUME_DIR/core/data/certs/redis_ca.crt
        ```
        ```bash
        # 测试 redis 连接无误
        # redis-cli --tls --cacert $VOLUME_DIR/core/data/certs/redis_ca.crt -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD info
        ```

=== "私钥认证"
    !!! tip ""
        ```bash
        # 准备好 Redis ca 文件、私钥和证书 (自签证书)
        . /opt/jumpserver/config.txt
        mkdir $VOLUME_DIR/core/data/certs -p
        cp redis_ca.crt $VOLUME_DIR/core/data/certs/redis_ca.crt
        cp redis_client.crt $VOLUME_DIR/core/data/certs/redis_client.crt
        cp redis_client.key $VOLUME_DIR/core/data/certs/redis_client.key
        ```
        ```bash
        # 测试 redis 连接无误
        # redis-cli --tls --cacert $VOLUME_DIR/core/data/certs/redis_ca.crt --cert $VOLUME_DIR/core/data/certs/redis_client.crt --key $VOLUME_DIR/core/data/certs/redis_client.key -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD info
        ```

!!! tip ""
    ```bash
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim
    # 在配置文件配置使用 Redis SSL
    REDIS_USE_SSL=True
    ```
    ```bash
    # 然后重启 jumpserver 即可
    cd /opt/jumpserver-installer-{{ jumpserver.version }}
    ./jmsctl.sh down
    ./jmsctl.sh start
    ```

!!! warning "其他方式部署的 jumpserver 请将 Redis SSL 证书放到 /opt/jumpserver/data/certs 重启即可"

## [Web SSL 访问](../../admin-guide/proxy/)
