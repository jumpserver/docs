# 环境要求

## 1. 操作系统

!!! tip ""
    - 支持主流 Linux 发行版本（基于 Debian / RedHat，包括国产操作系统）
    - Gentoo / Arch Linux 请通过源码安装

| 操作系统   | 架构 | Linux 内核  | 软件要求       | 最小化硬件配置     |
| :------------ | :----------- | :-------- | :------------------------------------ | :-------------------- |
| linux/amd64   | x86_64       | >= 4.0    | wget curl tar gettext iptables python | 2Core/8GB RAM/60G HDD |
| linux/arm64   | aarch64      | >= 4.0    | wget curl tar gettext iptables python | 2Core/8GB RAM/60G HDD |

=== "Debian / Ubuntu"
    !!! tip ""
        ```sh
        apt-get update
        apt-get install -y wget curl tar gettext iptables
        ```

=== "RedHat / CentOS"
    !!! tip ""
        ```sh
        yum update
        yum install -y wget curl tar gettext iptables
        ```
## 2 数据库
!!! tip "JumpServer 需要使用 PostgreSQL、MySQL 或 MariaDB 存储数据，使用 Redis 缓存数据"

| 名称        | 版本    | 默认字符集        | 默认字符编码        | TLS/SSL          |
| :--------- | :------ | :--------------- | :----------------- | :--------------- |
| PostgreSQL | >= 9.6  | UTF8             | en_US.utf8         | :material-check: |
| MySQL      | >= 5.7  | utf8             | utf8_general_ci    | :material-check: |
| MariaDB    | >= 10.6 | utf8mb3          | utf8mb3_general_ci | :material-check: |

| 名称    | 版本 | Sentinel         | Cluster            | TLS/SSL          |
| :------ | :------ | :--------------- | :----------------- | :--------------- |
| Redis   | >= 6.0  | :material-check: | :material-close:   | :material-check: |


!!! tip "创建数据库 SQL 参考"

=== "PostgreSQL"
    !!! tip ""
        ```pgsql
        create database jumpserver with encoding='UTF8';
        ```
        ```pgsql
        postgres=# \l
                                                                 List of databases
            Name      |   Owner    | Encoding | Locale Provider |  Collate   |   Ctype    | ICU Locale | ICU Rules |   Access privileges   
        --------------+------------+----------+-----------------+------------+------------+------------+-----------+-----------------------
        jumpserver    | postgres   | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
        (1 rows)
        ```

=== "MySQL"
    !!! tip ""
        ```mysql
        create database jumpserver default charset 'utf8';
        ```
        ```mysql
        mysql> show create database jumpserver;
        +------------+---------------------------------------------------------------------+
        | Database   | Create Database                                                     |
        +------------+---------------------------------------------------------------------+
        | jumpserver | CREATE DATABASE `jumpserver` /*!40100 DEFAULT CHARACTER SET utf8 */ |
        +------------+---------------------------------------------------------------------+
        1 row in set (0.00 sec)
        ```

=== "MariaDB"
    !!! tip ""
        ```mysql
        create database jumpserver default charset 'utf8';
        ```
        ```mysql
        MariaDB> show create database jumpserver;
        +------------+-----------------------------------------------------------------------+
        | Database   | Create Database                                                       |
        +------------+-----------------------------------------------------------------------+
        | jumpserver | CREATE DATABASE `jumpserver` /*!40100 DEFAULT CHARACTER SET utf8mb3*/ |
        +------------+-----------------------------------------------------------------------+
        1 row in set (0.001 sec)
        ```
