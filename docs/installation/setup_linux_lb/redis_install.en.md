# Deploy Redis Service

## 1 Preparation
### 1.1 Environment Information
!!! tip ""
    - Redis server information is as follows: 
    
    ```sh 
    192.168.100.11
    ```

### 1.2 Update System Package Index
!!! tip ""
    ```sh
    sudo apt update
    ```

## 2 Install and Configure Redis
### 2.1 Install Redis via APT
!!! tip ""
    ```sh
    sudo apt install -y redis-server
    ```

### 2.2 Configure Redis
!!! tip ""
    ```sh
    sudo vim /etc/redis/redis.conf
    ```
    ```vim
    requirepass KXOeyNgDeTdpeu9q  # Set password (already exists, uncomment)
    bind 127.0.0.1                # Comment out this line to enable remote access
    ```

### 2.3 Start Redis
!!! tip ""
    ```sh
    systemctl enable redis
    systemctl start redis
    ```

## 3 Configure Firewall
!!! tip ""
    ```sh
    sudo ufw allow from 192.168.100.0/24 to any port 6379 proto tcp
    sudo ufw reload
    ```
