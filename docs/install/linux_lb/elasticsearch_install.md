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
### 2.1 安装 Docker
!!! tip ""
    ```sh
    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
    yum makecache fast
    yum -y install docker-ce
    ```

### 2.2 配置 Docker
!!! tip ""
    ```sh
    mkdir /etc/docker/
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
    systemctl enable docker
    systemctl start docker
    ```

## 3 安装配置 Elasticsearch
### 3.1 下载 Elasticsearch 镜像
!!! tip ""
    ```sh
    docker pull docker.elastic.co/elasticsearch/elasticsearch:7.17.6
    ```
    ```vim
    7a0437f04f83: Pull complete
    7718d2f58c47: Pull complete
    cc5c16bd8bb9: Pull complete
    e3d829b4b297: Pull complete
    1ad944c92c79: Pull complete
    373fb8fbaf74: Pull complete
    5908d3eb2989: Pull complete
    Digest: sha256:81c126e4eddbc5576285670cb3e23d7ef7892ee5e757d6d9ba870b6fe99f1219
    Status: Downloaded newer image for docker.elastic.co/elasticsearch/elasticsearch:7.17.6
    docker.elastic.co/elasticsearch/elasticsearch:7.17.6
    ```

### 3.2 Elasticsearch 持久化数据目录创建
!!! tip ""
    ```sh
    mkdir -p /opt/jumpserver/elasticsearch/data /opt/jumpserver/elasticsearch/logs
    ```

### 3.3 启动 Elasticsearch 服务
!!! tip ""
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
    ```sh
    docker run --name jms_es -d -p 9200:9200 -p 9300:9300 -e cluster.name=docker-cluster -e discovery.type=single-node -e network.host=0.0.0.0 -e bootstrap.memory_lock="true" -e xpack.security.enabled="true" -e TAKE_FILE_OWNERSHIP="true" -e ES_JAVA_OPTS="-Xms512m -Xmx512m" -e ELASTIC_PASSWORD=KXOeyNgDeTdpeu9q -v /opt/jumpserver/elasticsearch/data:/usr/share/elasticsearch/data -v /opt/jumpserver/elasticsearch/logs:/usr/share/elasticsearch/logs --restart=always docker.elastic.co/elasticsearch/elasticsearch:7.17.6
    ```

### 3.4 在 JumpServer 中配置 Elasticsearch 
!!! tip ""
    - 访问 JumpServer Web 页面并使用管理员账号进行登录。
    - 点击左侧菜单栏的 [终端管理]，在页面的上方选择 [存储配置]，在 [命令存储] 下方选择 [创建] 选择 [Elasticsearch]
    - 根据下方的说明进行填写，保存后在 [终端管理] 页面对所有组件进行 [更新]，命令存储选择 [jms-es]，提交。

    | 选项            | 参考值                                               | 说明                   |
    | :-------------  | :-------------------------------------------------  | :--------------------- |
    | 名称 (Name)     | jms-es                                              | 标识, 不可重复          |
    | 类型 (Type)     | Elasticsearch                                       | 固定, 不可更改          |
    | 主机 (Hosts)    | http://elastic:KXOeyNgDeTdpeu9q@192.168.100.51:9200 | http://es_host:es_port |
    | 索引 (Index)    | jumpserver                                          | 索引                   |
    | 忽略证书认证    |                                                     | https 自签 ssl 需要勾选 |
    | 默认存储        |                                                     | 新组件将自动使用该存储   |
