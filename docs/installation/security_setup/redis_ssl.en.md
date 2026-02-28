# Redis SSL Connection

## 1 Operation Process
### 1.1 Prepare Database CA File
=== "Method 1"
    !!! tip ""
        - Prepare the Redis CA file (cloud providers usually only provide the CA file)

        ```bash
        mkdir -p /opt/jumpserver/config/certs/certs
        cp redis_ca.crt /opt/jumpserver/config/certs/redis_ca.crt
        ```

        - Test the Redis connection without errors.

        ```bash
        # . /opt/jumpserver/config/config.txt
        # redis-cli --tls --cacert /opt/jumpserver/config/certs/redis_ca.crt -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD info
        ```

=== "Method 2"
    !!! tip ""
        - Prepare the Redis CA file, private key, and certificate (self-signed certificate)

        ```bash
        mkdir -p /opt/jumpserver/config/certs
        cp redis_ca.crt /opt/jumpserver/config/certs/redis_ca.crt
        cp redis_client.crt /opt/jumpserver/config/certs/redis_client.crt
        cp redis_client.key /opt/jumpserver/config/certs/redis_client.key
        ```

        - Test the Redis connection without errors.

        ```bash
        # . /opt/jumpserver/config/config.txt
        # redis-cli --tls --cacert /opt/jumpserver/config/certs/redis_ca.crt --cert /opt/jumpserver/config/certs/redis_client.crt --key /opt/jumpserver/config/certs/redis_client.key -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD info
        ```

### 1.2 Edit Configuration File
!!! tip ""
    - Open the configuration file.
    
    ```bash
    vi /opt/jumpserver/config/config.txt

    ```

    - Configure Redis SSL in the configuration file.

    ```vim
    REDIS_USE_SSL=True
    ```

### 1.3 Restart JumpServer Service
!!! tip ""
    ```bash
    cd /opt/jumpserver-installer-{{ jumpserver.tag }}
    ./jmsctl.sh down
    ./jmsctl.sh start
    ```

!!! warning "For other JumpServer deployment methods, place the Redis SSL certificate in the data/certs directory of each component and restart"
    - /opt/jumpserver/data/certs
    - /opt/koko/data/certs
    - /opt/lion/data/certs
