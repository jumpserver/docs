# 迁移文档

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致, 否则会导致数据库加密数据无法解密"
    - 请不要跨大版本迁移数据库
    - JumpServer >= v2.6.0

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 6.0  |
| MariaDB | >= 10.2 |    |       |         |

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
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```
    ```sh
    ./jmsctl.sh install
    ```

### 3. 迁移数据

!!! tip "说明"
    - 将旧服务器备份的数据库拷贝到新服务器 /opt
    - 将旧服务器 /opt/jumpserver/config/config.txt 拷贝到新服务器 /opt/jumpserver/config/config.txt

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
