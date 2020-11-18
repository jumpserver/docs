# MariaDB 部署

## 环境

!!! tip ""
    - 系统: CentOS 7
    - 服务: MariaDB Server

    ```
    +----------+------------+-----------------+---------------+------------------------+
    | Protocol | ServerName |        IP       |      Port     |         Used By        |
    +==========+============+=================+===============+========================+
    |    TCP   |   Mariadb  | 192.168.100.10  |      3306     |           Core         |
    +----------+------------+-----------------+---------------+------------------------+
    ```

## 安装步骤

### 1. 安装 epel 库

!!! tip ""
    ```sh
    yum upgrade -y
    yum -y install epel-release wget
    ```

### 2. 配置防火墙

!!! tip ""
    ```sh
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="3306" accept"
    firewall-cmd --reload
    ```

!!! warning "生产环境请勿授权整个网段, 请根据实际情况修改"

### 3. 安装 mariadb

!!! tip ""
    ```sh
    vi /etc/yum.repos.d/mariadb.repo
    ```
    ```vi
    # MariaDB 10.5 CentOS repository list - created 2020-11-18 06:35 UTC
    # http://downloads.mariadb.org/mariadb/repositories/
    [mariadb]
    name = MariaDB
    baseurl = http://yum.mariadb.org/10.5/centos7-amd64
    gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
    gpgcheck=1
    ```
    ```sh
    yum install -y MariaDB-server MariaDB-client MariaDB-devel MariaDB-shared
    ```

### 4. 启动 mariadb

!!! tip ""
    ```sh
    systemctl enable mariadb
    systemctl start mariadb
    mysql_secure_installation
    ```

### 5. 创建数据库及授权

!!! tip ""
    ```sh
    mysql -uroot
    ```
    ```mysql
    create database jumpserver default charset 'utf8' collate 'utf8_bin';
    grant all on jumpserver.* to 'jumpserver'@'192.168.100.%' identified by 'weakPassword';
    flush privileges;
    ```

!!! warning "数据库密码应该采用更安全的密码"
