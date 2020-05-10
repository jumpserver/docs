# NFS 部署

## 环境

-  系统: CentOS 7
-  IP: 192.168.100.99

```
+----------+------------+-----------------+------------------------+
| Protocol | ServerName |        IP       |         Used By        |
+==========+============+=================+========================+
|    TCP   |     NFS    |  192.168.100.99 |       Core, Tengine    |
+----------+------------+-----------------+------------------------+
```

## 安装步骤

### 1. 安装 epel 库

```sh
yum upgrade -y  
yum -y install epel-release
```

### 2. 配置防火墙

```sh
firewall-cmd --add-service=nfs --permanent --zone=public
firewall-cmd --add-service=mountd --permanent --zone=public
firewall-cmd --add-service=rpc-bind --permanent --zone=public
firewall-cmd --reload
```

!!! warning "生产环境应该使用更严格的方式"

### 3. 安装 nfs-server

```sh
yum -y install nfs-utils rpcbind
systemctl enable rpcbind nfs-server nfs-lock nfs-idmap
systemctl start rpcbind nfs-server nfs-lock nfs-idmap
```

### 4. 创建 NFS 共享目录

```sh
mkdir /data
```

!!! info "此共享目录存放 jumpserver 的录像及任务结果"

### 5. 设置 NFS 访问权限

```sh
vi /etc/exports
```
```vim
/data 192.168.100.*(rw,sync,no_root_squash)
```

!!! info ""
    /data 是刚才创建的将被共享的目录, 192.168.100.* 表示整个 192.168.100.* 的资产都有括号里面的权限  
    也可以写具体的授权对象 /data 192.168.100.30(rw,sync,no_root_squash) 192.168.100.31(rw,sync,no_root_squash)


### 6. 使 exports 生效

```sh
exportfs -a
```