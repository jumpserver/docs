# Deploy PostgreSQL 16 Service

## 1 Preparation
### 1.1 Environment Information
!!! tip ""
    - PostgreSQL server information is as follows: 
    
    ```sh 
    192.168.100.11
    ```

### 1.2 Set Up Repository
!!! tip ""
    ```sh
    sudo apt update
    sudo apt install -y wget gnupg2
    sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
    sudo apt update
    ```

## 2 Install and Configure PostgreSQL
### 2.1 Install PostgreSQL via APT
!!! tip ""
    ```sh
    sudo apt install -y postgresql-16 
    ```

### 2.2 Start PostgreSQL
!!! tip ""
    ```sh
    sudo systemctl enable postgresql
    sudo systemctl start postgresql
    sudo systemctl status postgresql
    ```

### 2.3 Configure Database Authorization
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

### 2.4 Configure Remote Access
!!! tip ""
    ```sh
    sudo vim /etc/postgresql/16/main/postgresql.conf
    ```
    Find and modify:
    ```vim
    listen_addresses = '*'
    ```
### 2.5 Configure Client Authentication
!!! tip ""
    ```sh
    sudo vim /etc/postgresql/16/main/pg_hba.conf
    ```
    Add at the end:
    ```vim
    host    all             all             0.0.0.0/0               md5
    ```
    Restart the service to take effect:
    ```sh
    sudo systemctl restart postgresql
    sudo systemctl status postgresql
    ```


## 3 Configure Firewall
!!! tip ""
    ```sh
    sudo ufw allow from 192.168.100.0/24 to any port 5432
    sudo ufw reload
    ```
