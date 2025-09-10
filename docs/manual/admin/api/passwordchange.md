## 1. 查询改密计划
!!! tip "请求示例"
    ```sh
    curl -X GET 'https://localhost/api/v1/accounts/change-secret-automations/?offset=0&limit=15' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
## 2. 创建改密计划
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/accounts/change-secret-automations/' \ 
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d '{ 
        "accounts": ["root"], 
        "secret_strategy": "random", 
        "secret_type": "password", 
        "password_rules": { 
            "length": "16" 
            }, 
        "ssh_key_change_strategy": "add", 
        "is_periodic": true,
        "interval": 24, 
        "is_active": true, 
        "name": "test", 
        "assets": ["9266b1f8-f74d-482c-805a-6eed0e099a42"], 
        "nodes": [{ 
        "pk": "90cdb498-9167-4308-8087-cd27b953f5fb" 
        }], 
        "crontab": "0 0 * */1 *", 
        "recipients": [{ 
        "pk": "d1a02c44-e40b-41ac-884a-c44f3c664209" 
        }], 
        "comment": "test" 
        }'
    ```
## 3. 更新改密计划
!!! tip "请求示例"
    ```sh
    curl -X PUT 'https://localhost/api/v1/accounts/change-secret-automations/0a6a2e40-f92b-4aca-94ef-5f6ae5b0966c' \ 
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d '{ 
        "accounts": ["root"], 
        "secret_strategy": "random", 
        "secret_type": "password", 
        "password_rules": { 
            "length": "16" 
            }, 
        "ssh_key_change_strategy": "add", 
        "is_periodic": true,
        "interval": 24, 
        "is_active": true, 
        "name": "test", 
        "assets": ["9266b1f8-f74d-482c-805a-6eed0e099a42"], 
        "nodes": [{ 
            "pk": "90cdb498-9167-4308-8087-cd27b953f5fb" 
        }], 
        "crontab": "0 0 * */1 *", 
        "recipients": [{ 
            "pk": "d1a02c44-e40b-41ac-884a-c44f3c664209" 
        }], 
        "comment": "test" 
        }'
    ```
## 4. 删除改密计划
!!! tip "请求示例"
    ```sh
    curl -X DELETE 'https://localhost/api/v1/accounts/change-secret-automations/0a6a2e40-f92b-4aca-94ef
    5f6ae5b0966c’ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'  
    ```

## 5. 执行改密计划
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/accounts/change-secret-executions/' \ 
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \
        -d '{"automation":"bc778562-630e-4c89-971a-3ec629d4fd3f"}'
    ```