# 部署 NFS 服务

## 1 NFS 服务器端安装与配置
### 1.1 环境信息
!!! tip ""
    - NFS 服务器信息如下: 

    ```sh
    192.168.100.11
    ```

### 1.2 安装 NFS 服务器软件
!!! tip ""
    ```sh
    sudo apt update
    sudo apt install nfs-kernel-server -y
    ```


### 1.4 启动 NFS
!!! tip ""
    ```sh
    sudo systemctl enable nfs-kernel-server
    sudo systemctl start nfs-kernel-server
    sudo systemctl status nfs-kernel-server
    ```

### 1.5 配置防火墙
!!! tip ""
    ```sh
    sudo ufw allow nfs
    sudo ufw allow mountd
    sudo ufw allow rpc-bind
    sudo ufw status
    ```

### 1.6 配置 NFS
!!! tip ""
    ```sh
    mkdir /data
    chmod 777 -R /data

    vi /etc/exports
    ```
    ```vim
    # 设置 NFS 访问权限, /data 是刚才创建的将被共享的目录, 192.168.100.* 表示整个 192.168.100.* 的资产都有括号里面的权限
    # 也可以写具体的授权对象 /data 192.168.100.30(rw,sync,no_root_squash) 192.168.100.31(rw,sync,no_root_squash)
    /data 192.168.100.*(rw,sync,all_squash,anonuid=0,anongid=0)
    ```
    
### 1.7 让 exports 配置生效
!!! tip ""
    ```sh
    sudo exportfs -ra
    ```