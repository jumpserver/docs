# Preparation Guide

## 1 Overall Deployment Description
!!! tip "Environment Description"
    - Except for JumpServer's own components, the high availability of other components should be deployed according to the official documentation of the corresponding project.
    - After deployment in this manner, you only need to scale JumpServer nodes as needed and add the nodes to HAProxy.
    - If you already have an HLB or SLB, you can skip the HAProxy deployment. Third-party LB needs to pay attention to session and websocket issues.
    - If you already have cloud storage (S3/Ceph/Swift/OSS/Azure), you can skip MinIO deployment. The same applies to MySQL and Redis.
    - In production environments, you should use Ceph to replace NFS, or deploy high-availability NFS to prevent single point of failure.
    - This document is a reference document. Specific architecture needs to be designed according to your needs.

### 1.1 Database Requirements
!!! tip ""

    | Name    | Version | Default Charset | Default Collation | TLS/SSL          |
    | :------ | :------ | :--------------- | :----------------- | :--------------- |
    | PostgreSQL   | 16  | utf8             | utf8_general_ci    | :material-check: |
    | MariaDB | >= 10.6 | utf8mb3          | utf8mb3_general_ci | :material-check: |
    
    | Name    | Version | Sentinel         | Cluster            | TLS/SSL          |
    | :------ | :------ | :--------------- | :----------------- | :--------------- |
    | Redis   | >= 6.0  | :material-check: | :material-close:   | :material-check: |
    
### 1.2 Server Requirements
!!! tip ""

    | Service Name   |      IP Address        |  Port                   |     Components/Services Used     |   Minimum Hardware Config    |   Standard Hardware Config     |
    | ------------- | ---------------- | ----------------------- | ---------------- | ---------------------- | ----------------------- |
    | NFS           |  192.168.100.11  |  -                      | Core             | 2Core/8GB RAM/100G HDD | 4Core/16GB RAM/1T SSD |
    | PostgreSQL    |  192.168.100.11  | 5432                    | Core             | 2Core/4GB RAM/100G HDD | 4Core/8GB RAM/500G SSD |
    | Redis         |  192.168.100.11  | 6379                    | Core, KoKo, Lion | 2Core/4GB RAM/100G HDD | 4Core/8GB RAM/500G SSD |
    | HAProxy       |  192.168.100.100 | 80,443,2222,3389        | All              | 2Core/4GB RAM/20G HDD  | 2Core/4GB RAM/20G HDD  |
    | JumpServer 01 |  192.168.100.21  | 80,443,2222,3389        | All              | 4Core/8GB RAM/100G HDD | 8Core/16GB RAM/200G SSD |
    | JumpServer 02 |  192.168.100.22  | 80,443,2222,3389        | All              | 4Core/8GB RAM/100G HDD | 8Core/16GB RAM/200G SSD |
    | MinIO         |  192.168.100.41  | 9000,9001               | Core             | 2Core/4GB RAM/100G HDD | 4Core/8GB RAM/1T SSD |
    | Elasticsearch |  192.168.100.51  | 9200,9300               | Core, KoKo       | 2Core/4GB RAM/100G HDD | 4Core/8GB RAM/1T SSD |
    
### 1.3 Component Container Health Check
!!! tip ""

    | Component     | Health Check Endpoint URL            | Demo                                   |
    | ------------- | ----------------------------------- | -------------------------------------- |
    | Core          | http://core:8000/api/health/        | https://demo.jumpserver.org/api/health/ |
    | KoKo          | http://koko:5000/health/            | https://demo.jumpserver.org/koko/health/ |
    | Lion          | http://lion:8081/lion/health/       | https://demo.jumpserver.org/lion/health/ |

## 2 Deployment Order
!!! tip ""
    1. Deploy NFS service
    2. Deploy PostgreSQL service
    3. Deploy Redis service
    4. Deploy HAProxy service
    5. Deploy JumpServer 01 node
    6. Deploy JumpServer 02 node
    7. Deploy MinIO service
    8. Deploy Elasticsearch service
    9. Configure JumpServer components
    10. Deploy Elasticsearch service
