# Deploy JumpServer Node 02

## 1 Preparation
### 1.1 Environment Information
!!! tip ""
    - JumpServer_Node_02 server information is as follows: 
    ```sh
    192.168.100.22
    ```


## 2 Configure NFS
### 2.1 Install NFS Dependency Packages
!!! tip ""
    ```sh
    apt -y install nfs-utils
    showmount -e 192.168.100.11
    ```

### 2.2 Mount NFS Directory
!!! tip ""
    ```sh
    # Mount the Core persistence directory to NFS. The default is /opt/jumpserver/core/data. Modify according to actual situation.
    # JumpServer persistence directory definition is related to parameter VOLUME_DIR. You will be prompted during JumpServer installation.
    mkdir /opt/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /opt/jumpserver/core/data
    ```

### 2.3 Configure Automatic NFS Mount on Boot
!!! tip ""
    ```sh
    # Write to /etc/fstab for automatic mounting on reboot. Note: After setting this, if NFS is corrupted or cannot be connected, the server will fail to start.
    echo "192.168.100.11:/data /opt/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

## 3 Install JumpServer 
### 3.1 Download Installation Package
!!! tip ""
    - Download the latest linux/amd64 offline package from the Fei Zhi Yun community [downloads page](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, and upload it to the /opt directory of the deployment server.
### 3.2 Modify Temporary Configuration File
!!! tip ""
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="9 10"

    # Modify the options below. Keep others default. Do not directly copy content from here.
    # The bootstrap_token and SECRET_KEY in the configuration file must be consistent with other JumpServer nodes in the cluster, otherwise database data and component registration will be affected.

    # Installation Configuration
    ### Note the persistence directory VOLUME_DIR. If you mounted NFS to another directory above, modify it here as well.
    # For example, if NFS is mounted to /data/jumpserver/core/data, then VOLUME_DIR=/data/jumpserver
    VOLUME_DIR=/data/jumpserver

    # Core Configuration
    ### Cannot be modified after startup, otherwise passwords and other information cannot be decrypted. Do not directly copy the following string.
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW    # Must be consistent with other JumpServer nodes (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                                # Must be consistent with other JumpServer nodes (*)
    ```

### 3.3 Execute Script to Install JumpServer Service
!!! tip ""
    ```sh
    ./jmsctl.sh install
    ```

### 3.4 Start JumpServer Service
!!! tip ""
    ```sh
    ./jmsctl.sh start
    ```

## 4 Extend More Nodes
!!! tip ""
    - For additional node expansion, the installation and configuration are the same as above.
    - Ensure that the BOOTSTRAP_TOKEN and SECRET_KEY in the configuration files remain consistent across all nodes.
