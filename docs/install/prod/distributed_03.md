# MariaDB 部署

## 环境

-  系统: CentOS 7
-  服务: MariaDB Server

```
+----------+------------+-----------------+---------------+------------------------+
| Protocol | ServerName |        IP       |      Port     |         Used By        |
+==========+============+=================+===============+========================+
|    TCP   |   Mariadb  | 192.168.100.10  |      3306     |           Core         |
+----------+------------+-----------------+---------------+------------------------+
```

## 安装步骤

### 1. 安装 epel 库

```sh
yum upgrade -y
yum -y install epel-release wget
```

### 2. 配置防火墙

```sh
firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="3306" accept"
firewall-cmd --reload
```

!!! warning "生产环境请勿授权整个网段, 请根据实际情况修改"

### 3. 安装 mariadb

```sh
yum install -y mariadb mariadb-server mariadb-devel
```

### 4. 启动 mariadb

```sh
systemctl enable mariadb
systemctl start mariadb
```

### 5. 创建数据库及授权

```sh
mysql -uroot
```
```mysql
create database jumpserver default charset 'utf8' collate 'utf8_bin';
grant all on jumpserver.* to 'jumpserver'@'192.168.100.%' identified by 'weakPassword';
flush privileges;
```

!!! warning "数据库密码应该采用更安全的密码"