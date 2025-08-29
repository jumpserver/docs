# 部署 MinIO 服务

!!! tip "提示"
    - 此文档以docker方式部署MinIO为例，其他安装方式请参考 (https://docs.min.io/docs/minio-quickstart-guide)
   
## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - MinIO 服务器信息如下: 

    ```sh 
    192.168.100.41
    ```
## 2 通过 Docker Compose 安装配置 MinIO
### 2.1 MinIO 持久化数据目录创建
!!! tip ""
    ```sh
    sudo mkdir -p /opt/jumpserver/minio/data /opt/jumpserver/minio/config
    ```
### 2.2 docker-compose.yml 配置
!!! tip ""
    ```vim
        ## 请自行修改账号密码并牢记，丢失后可以删掉容器后重新用新密码创建，数据不会丢失
        # 9000                                   # api     访问端口
        # 9001                                   # console 访问端口
        # MINIO_ROOT_USER=minio                 # minio 账号
        # MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q  # minio 密码
    ```
    ```vim 
        version: '3.8'
        services:
        jms_minio:
            image: minio/minio:latest
            container_name: jms_minio
            restart: always
            ports:
            - "9000:9000"   # MinIO API端口
            - "9001:9001"   # MinIO控制台端口
            environment:
            - MINIO_ROOT_USER=minio
            - MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q
            volumes:
            - /opt/jumpserver/minio/data:/data
            - /opt/jumpserver/minio/config:/root/.minio
            command: server /data --console-address ":9001"
    ```
### 2.4 启动 MinIO 服务
!!! tip ""
    ```sh
        cd /opt/jumpserver
        docker compose up -d
    ```

## 3 MinIO 配置
### 3.1 在 MinIO 中创建 Buckets
!!! tip ""
    - 访问 http://192.168.100.41:9000，输入刚才设置的 MinIO 账号密码登录。
    - 点击左侧菜单的 Buckets，选择 Create Bucket 创建桶，Bucket Name 输入 jumpserver，然后点击 Save 保存。

### 3.2 在 JumpServer 中配置 MinIO
!!! tip ""
    - 访问 JumpServer Web 页面并使用管理员账号进行登录。
    - 点击左侧菜单栏的 [终端管理]，在页面的上方选择 [存储配置]，在 [录像存储] 下方选择 [创建] 选择 [Ceph]
    - 根据下方的说明进行填写，保存后在 [终端管理] 页面对所有组件进行 [更新]，录像存储选择 [jms-mino]，提交。

    | 选项            | 参考值                      | 说明                |
    | :-------------  | :------------------------- | :------------------ |
    | 名称 (Name)     | jms-minio                  | 标识, 不可重复       |
    | 类型 (Type)     | Ceph                       | 固定, 不可更改       |
    | 桶名称 (Bucket) | jumpserver                 | Bucket Name         |
    | Access key(AK)      | minio                      | MINIO_ROOT_USER     |
    | Access key secret(SK)     | KXOeyNgDeTdpeu9q           | MINIO_ROOT_PASSWORD |
    | 端点 (Endpoint) | http://192.168.100.41:9000 | minio 服务访问地址   |
    | 默认        |                            | 新组件将自动使用该存储 |

