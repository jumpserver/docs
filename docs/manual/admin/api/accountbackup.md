## 1. 查询账号备份策略
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/accounts/account-backup-plans/?offset=0&limit=15' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
## 2. 创建账号备份策略
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/accounts/account-backup-plans/' \ 
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d’{ 
        "types": ["linux", "windows", "unix", "other", "general", "switch", "router", "firewall", "mysql", "mariadb", 
        "postgresql", "oracle", "sqlserver", "clickhouse", "mongodb", "redis", "public", "private", "k8s", "website"], 
        "is_periodic": true, 
        "interval": 24, 
        "name": "test", 
        "recipients": [{ 
            "pk": "d1a02c44-e40b-41ac-884a-c44f3c664209" 
            }], 
        "crontab": "0 0 * * *", 
        "comment": "abcs" 
        }’
    ```
## 3. 删除账号备份策略
!!! tip "请求示例"  
    ```sh
    curl -X DELETE 'https://localhost/api/v1/accounts/account-backup-plans/37e4c30a-71ea-4b58-91f3-a692715dcf99/' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'  
    ```
## 4. 执行账号备份策略
!!! tip "请求示例"  
    ```sh
    curl -X POST 'https://localhost/api/v1/accounts/account-backup-plan-executions/' \
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'\ -d'{plan: "37e4c30a-71ea-4b58-91f3-a692715dcf99"}' 
    ```