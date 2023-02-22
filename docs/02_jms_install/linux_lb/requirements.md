# 准备工作
## 1 整体部署说明
!!! tip "环境说明"
    - 除 JumpServer 自身组件外，其他组件的高可用请参考对应的官方文档进行部署。
    - 按照此方式部署后，后续只需要根据需要扩容 JumpServer 节点然后添加节点到 HAProxy 即可。
    - 如果已经有 HLB 或者 SLB 可以跳过 HAProxy 部署，第三方 LB 要注意 session 和 websocket 问题。
    - 如果已经有 云存储 (S3/Ceph/Swift/OSS/Azure) 可以跳过 MinIO 部署，MySQL、Redis 也一样。
    - 生产环境中，应该使用 Ceph 等替代 NFS，或者部署高可用的 NFS 防止单点故障。

### 1.1 数据库要求
!!! tip ""

    | 名称    | 版本 | 默认字符集  | 默认字符编码  | TLS/SSL          |
    | :------ | :------ | :--------------- | :----------------- | :--------------- |
    | MySQL   | >= 5.7  | utf8             | utf8_general_ci    | :material-check: |
    | MariaDB | >= 10.2 | utf8mb3          | utf8mb3_general_ci | :material-check: |
    
    | Name    | Version | Sentinel         | Cluster            | TLS/SSL          |
    | :------ | :------ | :--------------- | :----------------- | :--------------- |
    | Redis   | >= 5.0  | :material-check: | :material-close:   | :material-check: |
    
### 1.2 服务器要求
!!! tip ""

    | 服务名称   |      IP 地址        |  端口                   |     使用涉及组件/服务     |   最小化硬件配置    |   标准化硬件配置     |
    | ------------- | ---------------- | ----------------------- | ---------------- | ---------------------- | ----------------------- |
    | NFS           |  192.168.100.11  |  -                      | Core             | 2Core/8GB RAM/100G HDD | 4Core/16GB RAM/1T   SSD |
    | MySQL         |  192.168.100.11  | 3306                    | Core             | 2Core/8GB RAM/90G  HDD | 4Core/16GB RAM/1T   SSD |
    | Redis         |  192.168.100.11  | 6379                    | Core, Koko, Lion | 2Core/8GB RAM/90G  HDD | 4Core/16GB RAM/1T   SSD |
    | HAProxy       |  192.168.100.100 | 80,443,2222,33060,33061 | All              | 2Core/4GB RAM/60G  HDD | 4Core/8GB  RAM/60G  SSD |
    | JumpServer 01 |  192.168.100.21  | 80,2222,33060,33061     | HAProxy          | 2Core/8GB RAM/60G  HDD | 4Core/8GB  RAM/90G  SSD |
    | JumpServer 02 |  192.168.100.22  | 80,2222,33060,33061     | HAProxy          | 2Core/8GB RAM/60G  HDD | 4Core/8GB  RAM/90G  SSD |
    | JumpServer 03 |  192.168.100.23  | 80,2222,33060,33061     | HAProxy          | 2Core/8GB RAM/60G  HDD | 4Core/8GB  RAM/90G  SSD |
    | JumpServer 04 |  192.168.100.24  | 80,2222,33060,33061     | HAProxy          | 2Core/8GB RAM/60G  HDD | 4Core/8GB  RAM/90G  SSD |
    | MinIO         |  192.168.100.41  | 9000,9001               | Core, KoKo, Lion | 2Core/4GB RAM/100G HDD | 4Core/8GB  RAM/1T   SSD |
    | Elasticsearch |  192.168.100.51  | 9200,9300               | Core, KoKo       | 2Core/4GB RAM/100G HDD | 4Core/8GB  RAM/1T   SSD |
    
### 1.3 组件容器健康检查
!!! tip ""

    | 服务名称   | 健康检查                   | 实例                                   |
    | ------------- | ------------------------------ | ----------------------------------------- |
    | Core          | http://core:8080/api/health/   | https://demo.jumpserver.org/api/health/   |
    | KoKo          | http://koko:5000/koko/health/  | https://demo.jumpserver.org/koko/health/  |
    | Lion          | http://lion:8081/lion/health/  | https://demo.jumpserver.org/lion/health/  |

## 2 部署顺序
!!! tip ""
    1.部署 NFS 服务

    2.部署 MySQL 服务

    3.部署 Redis 服务

    4.部署 JumpServer 01 节点 

    5.部署 JumpServer 02 节点 

    6.部署 JumpServer 03 节点 

    7.部署 JumpServer 04 节点 

    8.部署 HAProxy 服务 

    9.部署 MinIO 服务 
    
    10.部署 Elasticsearch 服务 