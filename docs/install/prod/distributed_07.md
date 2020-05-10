# guacamole 部署

## 环境

-  系统: CentOS 7
-  IP: 192.168.100.50

```
+----------+------------+-----------------+---------------+------------------------+
| Protocol | ServerName |        IP       |      Port     |         Used By        |
+==========+============+=================+===============+========================+
|    TCP   | Guacamole  | 192.168.100.50  |      8081     |         Tengine        |
+----------+------------+-----------------+---------------+------------------------+
|    TCP   | Guacamole  | 192.168.100.51  |      8081     |         Tengine        |
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
firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="8081" accept"
firewall-cmd --reload
```

!!! tip "192.168.100.100 为 tengine 服务器 ip, 请根据实际情况修改"

### 3. 配置 docker 源

```sh
yum install -y yum-utils device-mapper-persistent-data lvm2 wget
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum makecache fast
```

### 4. 安装 docker

```sh
yum -y install docker-ce
```

### 5. 配置 docker 加速

```sh
mkdir /etc/docker
wget -O /etc/docker/daemon.json http://demo.jumpserver.org/download/docker/daemon.json
```

### 6. 启动 docker

```sh
systemctl enable docker
systemctl start docker
```

### 7. 启动 guacamole

```sh
docker run --name jms_guacamole -d \
  -p 8081:8080 \
  -e JUMPSERVER_KEY_DIR=/config/guacamole/key \
  -e JUMPSERVER_SERVER=http://192.168.100.100 \
  -e BOOTSTRAP_TOKEN=zxffNymGjP79j6BN \
  -e GUACAMOLE_LOG_LEVEL=ERROR \
  jumpserver/jms_guacamole:1.5.8
```

!!! warning "BOOTSTRAP_TOKEN 的值从 jumpserver/config.yml 里面获取"
    访问 http://192.168.100.100/terminal/terminal/ 检查 guacamole 注册

## 多节点部署

- 登录到新的节点服务器, 前面安装 docker 都是一样的

```sh
yum upgrade -y
yum -y install epel-release wget
firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="8081" accept"
firewall-cmd --reload
yum -y install docker-ce
mkdir /etc/docker
wget -O /etc/docker/daemon.json http://demo.jumpserver.org/download/docker/daemon.json
systemctl enable docker
systemctl start docker
```

- 启动 guacamole

```sh
docker run --name jms_guacamole -d \
  -p 8081:8080 \
  -e JUMPSERVER_KEY_DIR=/config/guacamole/key \
  -e JUMPSERVER_SERVER=http://192.168.100.100 \
  -e BOOTSTRAP_TOKEN=zxffNymGjP79j6BN \
  -e GUACAMOLE_LOG_LEVEL=ERROR \
  jumpserver/jms_guacamole:1.5.8
```

!!! warning "BOOTSTRAP_TOKEN 的值从 jumpserver/config.yml 里面获取"
    访问 http://192.168.100.100/terminal/terminal/ 检查 guacamole 注册