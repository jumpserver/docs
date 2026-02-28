# Deploy MinIO Service

!!! tip "Note"
    - This document takes Docker Compose deployment of MinIO as an example. For other installation methods, please refer to https://docs.min.io/docs/minio-quickstart-guide
   
## 1 Preparation
### 1.1 Environment Information
!!! tip ""
    - MinIO server information is as follows: 

    ```sh 
    192.168.100.41
    ```
## 2 Install and Configure MinIO via Docker Compose
### 2.1 Create MinIO Data Persistence Directory
!!! tip ""
    ```sh
    sudo mkdir -p /opt/jumpserver/minio/data /opt/jumpserver/minio/config
    ```
### 2.2 Docker Compose Configuration
!!! tip ""
    ```vim
    # Please modify the account and password yourself and remember them. 
    # After losing them, you can delete the container and recreate it with a new password. Data will not be lost.
    # MINIO_ROOT_USER=minio          # MinIO username
    # MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q  # MinIO password
    ```
    ```vim 
    version: '3.8'
    ```
### 2.3 Start MinIO Service
!!! tip ""
    ```sh
    cd /opt/jumpserver
    docker compose up -d
    ```

## 3 MinIO Configuration
### 3.1 Create Buckets in MinIO
!!! tip ""
    - Visit http://192.168.100.41:9000 and log in with the MinIO credentials you set earlier.
    - Click the Buckets menu on the left side, select Create Bucket, enter jumpserver as the Bucket Name, then click Save.

### 3.2 Configure MinIO in JumpServer
!!! tip ""
    - Visit the JumpServer web page and log in with your administrator account.
    - Click [Terminal Management] in the left menu, select [Storage Configuration] at the top of the page, under [Recording Storage] select [Create] and choose [Ceph]
    - Fill in according to the instructions below, then on the [Terminal Management] page [Update] all components, select [jms-minio] for recording storage, and submit.

    | Option            | Reference Value                | Description                |
    | :-------------  | :------------------------- | :------------------ |
    | Name     | jms-minio                  | Identifier, must be unique       |
    | Type     | Ceph                       | Fixed, cannot be changed       |
    | Bucket | jumpserver                 | Bucket Name         |
    | Access Key (AK)      | minio                      | MINIO_ROOT_USER     |
    | Access Key Secret (SK)     | KXOeyNgDeTdpeu9q           | MINIO_ROOT_PASSWORD |
    | Endpoint | http://192.168.100.41:9000 | MinIO service access address   |
    | Default        |                            | New components will automatically use this storage |
