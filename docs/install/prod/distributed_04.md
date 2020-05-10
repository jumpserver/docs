# Redis 部署

## 环境

-  系统: CentOS 7
-  IP: 192.168.100.20

```
+----------+------------+-----------------+---------------+------------------------+
| Protocol | ServerName |        IP       |      Port     |         Used By        |
+==========+============+=================+===============+========================+
|    TCP   |    Redis   | 192.168.100.20  |      6379     |           Core         |
+----------+------------+-----------------+---------------+------------------------+
```

!!! info "注意: Redis 的数据库 3,4,5 被 Core 使用, 6 被 Koko 使用"

## 安装步骤

### 1. 安装 epel 库

```sh
yum upgrade -y
yum -y install epel-release wget
```

### 2. 配置防火墙

```sh    
firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="6379" accept"
firewall-cmd --reload
```

!!! warning "生产环境应该最小化授权"

### 3. 安装 redis

```sh
yum install -y install epel-release
yum install -y redis
```

### 4. 修改配置文件

```sh
vi /etc/redis.conf
```
```vim
...
# bind 127.0.0.1  # 注释这行, 新增如下内容
bind 0.0.0.0
requirepass weakPassword  # redis 连接密码
maxmemory-policy allkeys-lru  # 清理策略, 优先移除最近未使用的key
...
```

### 5. 启动 redis
```sh
systemctl start redis
systemctl enable redis
```