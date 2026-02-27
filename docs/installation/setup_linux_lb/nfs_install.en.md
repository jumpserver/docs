# Deploy NFS Service

## 1 NFS Server Installation and Configuration
### 1.1 Environment Information
!!! tip ""
    - NFS server information is as follows: 

    ```sh
    192.168.100.11
    ```

### 1.2 Install NFS Server Software
!!! tip ""
    ```sh
    sudo apt update
    sudo apt install nfs-kernel-server -y
    ```


### 1.3 Start NFS
!!! tip ""
    ```sh
    sudo systemctl enable nfs-kernel-server
    sudo systemctl start nfs-kernel-server
    sudo systemctl status nfs-kernel-server
    ```

### 1.4 Configure Firewall
!!! tip ""
    ```sh
    sudo ufw allow nfs
    sudo ufw allow mountd
    sudo ufw allow rpc-bind
    sudo ufw status
    ```

### 1.5 Configure NFS
!!! tip ""
    ```sh
    mkdir /data
    chmod 777 -R /data

    vi /etc/exports
    ```
    ```vim
    # Set NFS access permissions. /data is the directory to be shared. 192.168.100.* means all assets in the 192.168.100.* segment have the permissions in parentheses.
    # You can also write specific authorization targets: /data 192.168.100.30(rw,sync,no_root_squash) 192.168.100.31(rw,sync,no_root_squash)
    /data 192.168.100.*(rw,sync,all_squash,anonuid=0,anongid=0)
    ```
    
### 1.6 Make the exports Configuration Effective
!!! tip ""
    ```sh
    sudo exportfs -ra
    ```
