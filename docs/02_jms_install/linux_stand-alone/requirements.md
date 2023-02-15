# 环境要求
## 1 操作系统
!!! tip ""
    **JumpServer 的操作系统环境要求如下：**
!!! tip ""
    | OS/Arch       | Architecture | Linux Kernel  | Soft Requirement                      | Minimize Hardware     |
    | :------------ | :----------- | :------------ | :------------------------------------ | :-------------------- |
    | linux/amd64   | x86_64       | >= 4.0        | wget curl tar gettext iptables python | 2Core/8GB RAM/60G HDD |
    | linux/arm64   | aarch64      | >= 4.0        | wget curl tar gettext iptables python | 2Core/8GB RAM/60G HDD |
    | linux/loong64 | loongarch64  | == 4.19       | wget curl tar gettext iptables python | 2Core/8GB RAM/60G HDD |

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
!!! tip ""
    **JumpServer 需要使用 MySQL 或 MariaDB 存储数据，使用 Redis 缓存数据，如果有自建数据库或云数据库的使用需求请参考下列的数据库环境要求：**
!!! tip "我们支持[数据库 SSL 连接](../db_ssl/mysql_ssl.md) 和 [Redis SSL 连接](../db_ssl/redis_ssl.md)"

!!! tip ""
    | Name    | Version | Default Charset  | Default collation  | TLS/SSL          |
    | :------ | :------ | :--------------- | :----------------- | :--------------- |
    | MySQL   | >= 5.7  | utf8             | utf8_general_ci    | :material-check: |
    | MariaDB | >= 10.2 | utf8mb3          | utf8mb3_general_ci | :material-check: |

    | Name    | Version | Sentinel         | Cluster            | TLS/SSL          |
    | :------ | :------ | :--------------- | :----------------- | :--------------- |
    | Redis   | >= 5.0  | :material-check: | :material-close:   | :material-check: |


!!! tip "数据库建库语句参考"
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