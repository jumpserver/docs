# 部署 Redis 服务

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - Redis 服务器信息如下: 
    
    ```sh 
    192.168.100.11
    ```

### 1.2 更新系统包索引
!!! tip ""
    ```sh
    sudo apt update
    ```

## 2 安装配置 Redis
### 2.1 APT 方式安装 Redis
!!! tip ""
    ```sh
    sudo apt install -y redis-server
    ```

### 2.2 配置 Redis
!!! tip ""
    sudo vim /etc/redis/redis.conf
    ```sh
    requirepass KXOeyNgDeTdpeu9q #设置密码（存在，去掉注释）
    bind 127.0.0.1 #注释掉这一行，开启远程访问
    ```

### 2.3 启动 Redis
!!! tip ""
    ```sh
    systemctl enable redis
    systemctl start redis
    ```

## 3 配置防火墙
!!! tip ""
    ```sh
    sudo ufw allow from 192.168.100.0/24 to any port 6379 proto tcp
    sudo ufw reload
    ```