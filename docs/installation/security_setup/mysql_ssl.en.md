# Database SSL Connection

## 1 Operation Process
### 1.1 Prepare Database CA File
!!! tip ""
    - Prepare the database CA file. Currently, private key authentication is not supported.

    ```bash
    mkdir -p /opt/jumpserver/config/certs
    cp db_ca.pem /opt/jumpserver/config/certs/db_ca.pem
    ```
    
    - Test the MySQL connection without errors.

    ```bash
    # . /opt/jumpserver/config/config.txt
    # mysql --ssl-ca=/opt/jumpserver/config/certs/db_ca.pem -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASSWORD $DB_NAME
    ```

### 1.2 Edit Configuration File
!!! tip ""
    - Open the configuration file.

    ```bash
    vi /opt/jumpserver/config/config.txt
    ```

    - Configure DB SSL in the configuration file.

    ```vim
    DB_USE_SSL=True
    ```
    
### 1.3 Restart JumpServer Service
!!! tip ""
    ```bash
    cd /opt/jumpserver-installer-{{ jumpserver.tag }}
    ./jmsctl.sh down
    ./jmsctl.sh start
    ```

!!! warning "For other JumpServer deployment methods, place the database certificate db_ca.pem in /opt/jumpserver/data/certs and restart"
