# Migration Guide

!!! warning "Note"
    - Maintain SECRET_KEY consistent with the old version during upgrade and migration, otherwise encrypted data in the database cannot be decrypted.

## 1 Migration Instructions

!!! tip "v2.6 Version Upgrade Instructions"
    - Unified installation method for enterprise and open-source versions; community version can seamlessly switch to enterprise version.
    - Only this installation method will be maintained going forward; other installation methods will no longer provide technical support.
    - After installation, configuration file is in /opt/jumpserver/config/config.txt

## 2 Migration Steps

### 2.1 Database Backup

!!! tip ""
    - Get database information from the jumpserver/config.txt file:

    ```yaml
    DB_HOST: 127.0.0.1       # Database server IP
    DB_PORT: 3306            # Database server port
    DB_USER: jumpserver      # User for database connection
    DB_PASSWORD: ******      # Password for database connection user
    DB_NAME: jumpserver      # Database used by JumpServer
    # mysqldump -h<DB_HOST> -P<DB_PORT> -u<DB_USER> -p<DB_PASSWORD> <DB_NAME> > /opt/<DB_NAME>.sql
    ```

!!! tip ""
    - Select the database backup method corresponding to your environment deployment:

    === "installer deployment"
        ```bash
        jmsctl backup_db
        ```

    === "source code deployment"
        ```bash
        mysqldump -h<DB_HOST> -P<DB_PORT> -u<DB_USER> -p<DB_PASSWORD> <DB_NAME> > /opt/<DB_NAME>.sql
        ```

    === "containerized component deployment"
        ```bash
        docker exec jms_db_1 /usr/bin/mysqldump -uroot -pjumpserver jumpserver > /opt/jumpserver.sql
        ```

### 2.2 Modify Database Character Set

!!! tip ""
    - If you don't need or don't want to handle database character set, skip this step. Just ensure the database character set is the same before and after migration.
    ```bash
    ALTER DATABASE jumpserver CHARACTER SET utf8 COLLATE utf8_general_ci;
    ```

### 2.3 Download jumpserver-install

!!! tip ""
    ```bash
    cd /opt
    wget https://github.com/jumpserver/jumpserver/releases/download/v4.10.9/jumpserver-installer-v4.10.9.tar.gz
    tar xf jumpserver-installer-v4.10.9.tar.gz
    cd jumpserver-installer-v4.10.9
    ```

### 2.4 Edit Temporary Configuration File

!!! tip ""
    ```bash
    vi quick_start.sh
    ```

## 2.5 Start JumpServer Deployment

!!! tip ""
    - Select the deployment method corresponding to your database environment.
