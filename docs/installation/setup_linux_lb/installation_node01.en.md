# Deploy JumpServer Node 01

## 1 Preparation
### 1.1 Environment Information
!!! tip ""
    - JumpServer_Node_01 server information is as follows: 
    
    ```sh 
    192.168.100.21
    ```

## 2 Configure NFS
### 2.1 Install NFS Dependency Packages
!!! tip ""
    ```sh
    yum -y install nfs-utils
    showmount -e 192.168.100.11
    ```

### 2.2 Mount NFS Directory
!!! tip ""
    ```sh
    # Mount the Core persistence directory to NFS. The default is /data/jumpserver/core/data. Modify according to actual situation.
    # JumpServer persistence directory definition is related to parameter VOLUME_DIR. You will be prompted during JumpServer installation.
    mkdir /data/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /data/jumpserver/core/data
    ```

### 2.3 Configure Automatic NFS Mount on Boot
!!! tip ""
    ```sh
    # Write to /etc/fstab for automatic mounting on reboot. Note: After setting this, if NFS is corrupted or cannot be connected, the server will fail to start.
    echo "192.168.100.11:/data /data/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

## 3 Install JumpServer 

### 3.1 Download Installation Package
!!! tip ""
    - Download the latest linux/amd64 offline package from the Fei Zhi Yun community [downloads page](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, and upload it to the /opt directory of the deployment server.

### 3.2 Install JumpServer Service
!!! tip ""
    ```sh
    ./jmsctl.sh install
    ```

!!! warning "Note: The bootstrap_token and SECRET_KEY in the configuration file must be consistent with other JumpServer nodes in the cluster, otherwise database data and component registration will be affected. During the first installation, random values will be automatically generated. After Node 01 completes installation, these values need to be recorded and used in other nodes."

### 3.3 Start JumpServer Service
!!! tip ""
    ```sh
    ./jmsctl.sh start
    ```

## 4 Extend More Nodes
!!! tip ""
    - To extend more nodes, follow the same installation and configuration as above.
    - Ensure that the BOOTSTRAP_TOKEN and SECRET_KEY in the configuration files remain consistent across all nodes.
