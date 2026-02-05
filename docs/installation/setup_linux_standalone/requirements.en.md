# Requirements

## 1. Operating System

!!! tip ""
    - Supports mainstream Linux distributions (based on Debian / RedHat, including domestic operating systems)

| Operating System | Architecture | Linux Kernel | Software Requirements | Minimum Hardware Configuration |
| :------------ | :----------- | :-------- | :------------------------------------ | :-------------------- |
| linux/amd64   | x86_64       | >= 4.0    | wget curl tar gettext iptables python | 4Core / 8GB RAM / 100G HDD |
| linux/arm64   | aarch64      | >= 4.0    | wget curl tar gettext iptables python | 4Core / 8GB RAM / 100G HDD |

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
## 2. Database
!!! tip "JumpServer requires PostgreSQL, MySQL, or MariaDB to store data, and uses Redis for data caching."

| Name        | Version | Default Character Set | Default Collation | TLS/SSL          |
| :--------- | :------ | :--------------- | :----------------- | :--------------- |
| PostgreSQL | >= 16  | UTF8             | en_US.utf8         | :material-check: |
| MySQL      | >= 5.7  | utf8             | utf8_general_ci    | :material-check: |
| MariaDB    | >= 10.6 | utf8mb3          | utf8mb3_general_ci | :material-check: |

| Name    | Version | Sentinel         | Cluster            | TLS/SSL          |
| :------ | :------ | :--------------- | :----------------- | :--------------- |
| Redis   | >= 6.0  | :material-check: | :material-close:   | :material-check: |


!!! tip "Database Creation SQL Reference"

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
