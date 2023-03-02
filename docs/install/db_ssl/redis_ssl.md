# Redis SSL 连接

## 1 操作过程
### 1.1 准备数据库 CA 文件
=== "方式一"
    !!! tip ""
        - 准备好 Redis ca 文件 (云服务商一般只提供 ca 文件)

        ```bash
        mkdir -p /opt/jumpserver/config/certs/certs
        cp redis_ca.crt /opt/jumpserver/config/certs/redis_ca.crt
        ```

        - 测试 redis 连接无误。

        ```bash
        # . /opt/jumpserver/config/config.txt
        # redis-cli --tls --cacert /opt/jumpserver/config/certs/redis_ca.crt -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD info
        ```

=== "方式二"
    !!! tip ""
        - 准备好 Redis ca 文件、私钥和证书 (自签证书)

        ```bash
        mkdir -p /opt/jumpserver/config/certs
        cp redis_ca.crt /opt/jumpserver/config/certs/redis_ca.crt
        cp redis_client.crt /opt/jumpserver/config/certs/redis_client.crt
        cp redis_client.key /opt/jumpserver/config/certs/redis_client.key
        ```

        - 测试 redis 连接无误。

        ```bash
        # . /opt/jumpserver/config/config.txt
        # redis-cli --tls --cacert /opt/jumpserver/config/certs/redis_ca.crt --cert /opt/jumpserver/config/certs/redis_client.crt --key /opt/jumpserver/config/certs/redis_client.key -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD info
        ```

### 1.2 编辑配置文件
!!! tip ""
    - 打开配置文件。
    
    ```bash
    vi /opt/jumpserver/config/config.txt

    ```

    - 在配置文件配置使用 Redis SSL。

    ```vim
    REDIS_USE_SSL=True
    ```

### 1.3 重启 JumpServer 服务
!!! tip ""
    ```bash
    cd /opt/jumpserver-installer-{{ jumpserver.tag }}
    ./jmsctl.sh down
    ./jmsctl.sh start
    ```

!!! warning "其他方式部署的 JumpServer 请将 Redis SSL 证书放到各组件 data/certs 目录重启即可"
    - /opt/jumpserver/data/certs
    - /opt/koko/data/certs
    - /opt/lion/data/certs