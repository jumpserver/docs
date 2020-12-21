# 迁移文档

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致, 否则会导致数据库加密数据无法解密"
    - 请不要跨大版本迁移数据库
    - jumpserver 版本 >= v2.6.0

### 1. 备份数据

!!! tip ""
    ```sh
    ./jmsctl.sh backup_db
    ```

### 2. 配置新服务器

!!! tip ""
    ```sh
    yum -y install wget
    ```
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/v2.6.1/jumpserver-installer-v2.6.1.tar.gz
    tar -xf jumpserver-installer-v2.6.1.tar.gz
    cd jumpserver-installer-v2.6.1
    ```
    ```sh
    ./jmsctl.sh install
    ```

### 3. 迁移数据

!!! tip "说明"
    - 将旧服务器备份的数据库拷贝到新服务器 /opt
    - 将旧服务器 /opt/jumpserver/config.txt 拷贝到新服务器 /opt/jumpserver/config.txt

!!! tip ""
    ```sh
    ./jmsctl.sh start
    ./jmsctl.sh stop
    ```
    ```sh
    ./jmsctl.sh restore_db /opt/jumpserver.sql
    ```
    ```sh
    ./jmsctl.sh start
    ```
