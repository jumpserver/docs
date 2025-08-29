# 部署 PostgreSQL 16 服务

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - PostgreSQL 服务器信息如下: 
    
    ```sh 
    192.168.100.11
    ```

### 1.2 设置 Repo
!!! tip ""
    ```sh
    sudo apt update
    sudo apt install -y wget gnupg2
    sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
    sudo apt update
    ```

## 2 安装配置 PostgreSQL
### 2.1 Apt 方式安装 PostgreSQL
!!! tip ""
    ```sh
    sudo apt install -y postgresql-16 
    ```

### 2.2 启动 PostgreSQL
!!! tip ""
    ```sh
    sudo systemctl enable postgresql
    sudo systemctl start postgresql
    sudo systemctl status postgresql
    ```

### 2.3 配置数据库授权
!!! tip ""
    ```sh
    sudo -u postgres psql
    ```
    ```sql
    CREATE DATABASE jumpserver;
    CREATE USER jumpserver WITH PASSWORD 'KXOeyNgDeTdpeu9q';
    GRANT ALL PRIVILEGES ON DATABASE jumpserver TO jumpserver;
    \q
    ```

### 2.4 配置远程访问
!!! tip ""
    ```sh
    sudo vim /etc/postgresql/16/main/postgresql.conf
    ```
    找到并修改:
    ```sh
    listen_addresses = '*'
    ```
### 2.5 配置客户端认证
!!! tip ""
    ```sh
    sudo vim /etc/postgresql/16/main/pg_hba.conf
    ```
    在末尾添加:
    ```sh
    host    all             all             0.0.0.0/0               md5
    ```
    重启服务生效:
    ```sh
    sudo systemctl restart postgresql
    sudo systemctl status postgresql
    ```


## 3 配置防火墙
!!! tip ""
    ```sh
    sudo ufw allow from 192.168.100.0/24 to any port 5432
    sudo ufw reload
    ```