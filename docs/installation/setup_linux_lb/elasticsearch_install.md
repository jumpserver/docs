# 部署 Elasticsearch 服务

!!! tip "提示"
    - 集群部署请参考 (https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - Elasticsearch 服务器信息如下: 

    ```sh 
    192.168.100.51
    ```

## 2 安装配置 Docker 环境
### 2.1 安装 Docker 和 Docker Compose：
!!! tip ""
    ```sh
    sudo apt update
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce  docker-compose-plugin
    ```

### 2.2 配置 Docker
!!! tip ""
    ```sh
    sudo mkdir -p /etc/docker
    vi /etc/docker/daemon.json
    ```
    ```json
    {
      "live-restore": true,
      "registry-mirrors": ["https://hub-mirror.c.163.com", "https://bmtrgdvx.mirror.aliyuncs.com", "http://f1361db2.m.daocloud.io"],
      "log-driver": "json-file",
      "log-opts": {"max-file": "3", "max-size": "10m"}
    }
    ```

### 2.3 启动 Docker
!!! tip ""
    ```sh
    sudo systemctl enable docker
    sudo systemctl start docker
    ```

## 3 安装配置 Elasticsearch
### 3.1 创建 Elasticsearch 数据目录
!!! tip ""
    ```sh
    mkdir -p /opt/jumpserver/elasticsearch/data /opt/jumpserver/elasticsearch/logs
    ```
### 3.2 docker-compose 配置
!!! tip ""
    ```vim
        进入一个你方便管理的目录（例如/home/ubuntu）
        cd /home/ubuntu
        创建并编辑docker-compose.yml
        vim docker-compose.yml
    ```
    ```vim
        ## 请自行修改账号密码并牢记，丢失后可以删掉容器后重新用新密码创建，数据不会丢失
        # 9200                                  # Web 访问端口
        # 9300                                  # 集群通信
        # discovery.type=single-node            # 单节点
        # bootstrap.memory_lock="true"          # 锁定物理内存, 不使用 swap
        # xpack.security.enabled="true"         # 开启安全模块
        # TAKE_FILE_OWNERSHIP="true"            # 自动修改挂载文件夹的所属用户
        # ES_JAVA_OPTS="-Xms512m -Xmx512m"      # JVM 内存大小, 推荐设置为主机内存的一半
        # elastic                               # Elasticsearch 账号
        # ELASTIC_PASSWORD=KXOeyNgDeTdpeu9q     # Elasticsearch 密码
    ```
    ```vim
        version: '3.8'
        services:
        jms_es:
            image: docker.elastic.co/elasticsearch/elasticsearch:7.17.6
            container_name: jms_es
            restart: always
            ports:
            - "9200:9200"
            - "9300:9300"
            environment:
            - cluster.name=docker-cluster
            - discovery.type=single-node
            - network.host=0.0.0.0
            - bootstrap.memory_lock=true
            - xpack.security.enabled=true
            - TAKE_FILE_OWNERSHIP=true
            - ES_JAVA_OPTS=-Xms512m -Xmx512m
            - ELASTIC_PASSWORD=KXOeyNgDeTdpeu9q
            volumes:
            - /opt/jumpserver/elasticsearch/data:/usr/share/elasticsearch/data
            - /opt/jumpserver/elasticsearch/logs:/usr/share/elasticsearch/logs
            ulimits:
            memlock:
                soft: -1
                hard: -1
    ```
### 3.4 启动 Elasticsearch 服务
!!! tip ""
    ```sh
        # 确保当前目录是docker-compose.yml所在的目录（例如/home/ubuntu）
        cd /home/ubuntu
        docker compose up -d
    ```

### 3.5 在 JumpServer 中配置 Elasticsearch 
!!! tip ""
    - 访问 JumpServer Web 页面并使用管理员账号进行登录。
    - 点击左侧菜单栏的 [终端管理]，在页面的上方选择 [存储配置]，在 [命令存储] 下方选择 [创建] 选择 [Elasticsearch]
    - 根据下方的说明进行填写，保存后在 [终端管理] 页面对所有组件进行 [更新]，命令存储选择 [jms-es]，提交。

    | 选项            | 参考值                                               | 说明                   |
    | :-------------  | :-------------------------------------------------  | :--------------------- |
    | 名称 (Name)     | jms-es                                              | 标识, 不可重复          |
    | 类型 (Type)     | Elasticsearch                                       | 固定, 不可更改          |
    | 主机 (Hosts)    | http://elastic:KXOeyNgDeTdpeu9q@192.168.100.51:9200 | http://es_host:es_port |
    | 按日期建索引    |                                       | 是否根据日期动态建立索引                  |
    | 索引 (Index)    | jumpserver                                          | 索引                   |
    | 忽略证书认证    |                                                     | https 自签 ssl 需要勾选 |
    | 默认       |                                                     | 新组件将自动使用该存储   |
