# 部署 Redis 服务

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - Redis 服务器信息如下: 
    
    ```sh 
    192.168.100.11
    ```

### 1.2 设置 Repo
!!! tip ""
    ```sh
    yum -y install epel-release https://repo.ius.io/ius-release-el7.rpm
    ```

## 2 安装配置 Redis
### 2.1 Yum 方式安装 Redis
!!! tip ""
    ```sh
    yum install -y redis5
    ```

### 2.2 配置 Redis
!!! tip ""
    ```sh
    sed -i "s/bind 127.0.0.1/bind 0.0.0.0/g" /etc/redis.conf
    sed -i "561i maxmemory-policy allkeys-lru" /etc/redis.conf
    sed -i "481i requirepass KXOeyNgDeTdpeu9q" /etc/redis.conf
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
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="6379" accept"
    firewall-cmd --reload
    ```