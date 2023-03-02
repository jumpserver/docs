# 部署 MySQL 服务

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - MySQL 服务器信息如下: 
    
    ```sh 
    192.168.100.11
    ```

### 1.2 设置 Repo
!!! tip ""
    ```sh
    yum -y localinstall http://mirrors.ustc.edu.cn/mysql-repo/mysql57-community-release-el7.rpm
    ```

## 2 安装配置 MySQL
### 2.1 Yum 方式安装 MySQL
!!! tip ""
    ```sh
    yum install -y mysql-community-server
    ```

### 2.1 配置 MySQL
!!! tip ""
    ```sh
    if [ ! "$(cat /usr/bin/mysqld_pre_systemd | grep -v ^\# | grep initialize-insecure )" ]; then
        sed -i "s@--initialize @--initialize-insecure @g" /usr/bin/mysqld_pre_systemd
    fi
    ```

### 2.2 启动 MySQL
!!! tip ""
    ```sh
    systemctl enable mysqld
    systemctl start mysqld
    ```

### 2.3 配置数据库授权
!!! tip ""
    ```sh
    mysql -uroot
    ```
    ```mysql hl_lines="13 16 19 22 25 28"
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 2
    Server version: 5.7.32 MySQL Community Server (GPL)

    Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> create database jumpserver default charset 'utf8';
    Query OK, 1 row affected (0.00 sec)

    mysql> set global validate_password_policy=LOW;
    Query OK, 0 rows affected (0.00 sec)

    mysql> create user 'jumpserver'@'%' identified by 'KXOeyNgDeTdpeu9q';
    Query OK, 0 rows affected (0.00 sec)

    mysql> grant all on jumpserver.* to 'jumpserver'@'%';
    Query OK, 0 rows affected, 1 warning (0.00 sec)

    mysql> flush privileges;
    Query OK, 0 rows affected (0.00 sec)

    mysql> exit
    Bye
    ```

## 3 配置防火墙
!!! tip ""
    ```sh
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="3306" accept"
    firewall-cmd --reload
    ```