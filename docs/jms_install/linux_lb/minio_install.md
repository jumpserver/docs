# 部署 MinIO 服务

!!! tip "提示"
    - 集群部署请参考 (http://docs.minio.org.cn/docs/master/minio-erasure-code-quickstart-guide)

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - MinIO 服务器信息如下: 

    ```sh 
    192.168.100.41
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

## 3 安装配置 MinIO
### 3.1 下载 MinIO 镜像
!!! tip ""
    ```sh
    docker pull minio/minio:latest
    ```
    ```vim
    latest: Pulling from minio/minio
    a591faa84ab0: Pull complete
    76b9354adec6: Pull complete
    f9d8746550a4: Pull complete
    890b1dd95baa: Pull complete
    3a8518c890dc: Pull complete
    8053f0501aed: Pull complete
    506c41cb8532: Pull complete
    Digest: sha256:e7a725edb521dd2af07879dad88ee1dfebd359e57ad8d98104359ccfbdb92024
    Status: Downloaded newer image for minio/minio:latest
    docker.io/minio/minio:latest
    ```

### 3.2 MinIO 持久化数据目录创建
!!! tip ""
    ```sh
    mkdir -p /opt/jumpserver/minio/data /opt/jumpserver/minio/config
    ```

### 3.3 启动 MinIO 服务
!!! tip ""
    ```vim
    ## 请自行修改账号密码并牢记，丢失后可以删掉容器后重新用新密码创建，数据不会丢失
    # 9000                                  # api     访问端口
    # 9001                                  # console 访问端口
    # MINIO_ROOT_USER=minio                 # minio 账号
    # MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q  # minio 密码
    ```
    ```sh
    docker run --name jms_minio -d -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q -v /opt/jumpserver/minio/data:/data -v /opt/jumpserver/minio/config:/root/.minio --restart=always minio/minio:latest server /data --console-address ":9001"
    ```

### 3.5 在 MinIO 中创建 Buckets
!!! tip ""
    - 访问 http://192.168.100.41:9000，输入刚才设置的 MinIO 账号密码登录。
    - 点击左侧菜单的 Buckets，选择 Create Bucket 创建桶，Bucket Name 输入 jumpserver，然后点击 Save 保存。

### 3.6 在 JumpServer 中配置 MinIO
!!! tip ""
    - 访问 JumpServer Web 页面并使用管理员账号进行登录。
    - 点击左侧菜单栏的 [终端管理]，在页面的上方选择 [存储配置]，在 [录像存储] 下方选择 [创建] 选择 [Ceph]
    - 根据下方的说明进行填写，保存后在 [终端管理] 页面对所有组件进行 [更新]，录像存储选择 [jms-mino]，提交。

    | 选项            | 参考值                      | 说明                |
    | :-------------  | :------------------------- | :------------------ |
    | 名称 (Name)     | jms-minio                  | 标识, 不可重复       |
    | 类型 (Type)     | Ceph                       | 固定, 不可更改       |
    | 桶名称 (Bucket) | jumpserver                 | Bucket Name         |
    | Access key      | minio                      | MINIO_ROOT_USER     |
    | Secret key      | KXOeyNgDeTdpeu9q           | MINIO_ROOT_PASSWORD |
    | 端点 (Endpoint) | http://192.168.100.41:9000 | minio 服务访问地址   |
    | 默认存储        |                            | 新组件将自动使用该存储 |

