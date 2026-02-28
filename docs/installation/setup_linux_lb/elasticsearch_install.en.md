# Deploy Elasticsearch Service

!!! tip "Note"
    - This document takes Docker Compose deployment of Elasticsearch as an example. For other installation methods, please refer to https://www.elastic.co/guide/en/elasticsearch/reference/index.html

## 1 Preparation
### 1.1 Environment Information
!!! tip ""
    - Elasticsearch server information is as follows: 

    ```sh 
    192.168.100.51
    ```

## 2 Install and Configure Elasticsearch via Docker Compose

### 2.1 Create Elasticsearch Data Directory
!!! tip ""
    ```sh
    mkdir -p /opt/jumpserver/elasticsearch/data /opt/jumpserver/elasticsearch/logs
    ```
### 2.2 Docker Compose Configuration
!!! tip ""
    ```vim
    Enter a directory convenient for management (e.g., /home/ubuntu)
    vim docker-compose.yml
    ```
    ```vim
    # Please modify the account and password yourself and remember them. 
    # After losing them, you can delete the container and recreate it with a new password. Data will not be lost.
    # ELASTIC_PASSWORD=KXOeyNgDeTdpeu9q     # Elasticsearch password
    ```
    ```vim
    version: '3.8'
    ```
### 2.3 Start Elasticsearch Service
!!! tip ""
    ```sh
    # Make sure the current directory is where docker-compose.yml is located (e.g., /home/ubuntu)
    docker compose up -d
    ```

## 3 Configure Elasticsearch in JumpServer
!!! tip ""
    - Visit the JumpServer web page and log in with your administrator account.
    - Click [Terminal Management] in the left menu, select [Storage Configuration] at the top of the page, under [Command Storage] select [Create] and choose [Elasticsearch]
    - Fill in according to the instructions below, then on the [Terminal Management] page [Update] all components, select [jms-es] for command storage, and submit.

    | Option            | Reference Value                                               | Description                |
    | :-------------  | :-------------------------------------------------  | :--------------------- |
    | Name     | jms-es                                              | Identifier, must be unique          |
    | Type     | Elasticsearch                                       | Fixed, cannot be changed          |
    | Hosts    | https://elastic:KXOeyNgDeTdpeu9q@192.168.100.51:9200 | Elasticsearch service address |
    | Default       |                                                     | New components will automatically use this storage   |
