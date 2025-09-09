**1. 创建工单**
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/tickets/apply-asset-tickets/open/' \ 
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d '{ 
            "title":"test_tickets_1", 
            "apply_accounts":["@ALL"], 
            "apply_actions":["all"], 
            "org_id":"00000000-0000-0000-0000-000000000002", 
            "apply_assets":["b4f205af-4353-49ef-befa-ff9095d52a27"], 
            "apply_date_start":"2023-03-28T02:10:23.245Z", 
            "apply_date_expired":"2023-04-04T02:10:23.245Z" 
         }' 
    ```
**2. 获取工单**
!!! tip "请求示例"
    ```sh
    curl -X GET 'https://localhost/api/v1/tickets/tickets/?state=pending&status=open&type=apply_asset' \ 
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'
    ```
**3. 审批工单**
!!! tip "请求示例"
    ```sh
    curl -X PATCH 'https://localhost/api/v1/tickets/apply-asset-tickets/41b36621-dd4d-492e-a72c-be20b2daeea8/approve/' \ 
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d ' { 
                "org_id": "00000000-0000-0000-0000-000000000002", 
                "apply_assets": ["b4f205af-4353-49ef-befa-ff9095d52a27"], 
                "apply_accounts": ["@ALL"], 
                "apply_actions": ["all"], 
                "apply_date_start": "2023-03-28 10:10:23", 
                "apply_date_expired": "2023-04-04 10:10:23" 
                }'
    ```
**4. 查询流程**
!!! tip "请求示例"
    ```sh
    curl -X GET 'https://localhost/api/v1/tickets/flows/?offset=0&limit=15' \ 
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
**5. 更新流程**
!!! tip "请求示例"
    ```sh
    curl -X GET 'https://localhost/api/v1/tickets/flows/?offset=0&limit=15' \ 
        -H 'Content-Type: application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d ' { 
        "type": "apply_asset", 
        "approval_level": 1, 
        "rules": [{ 
            "level": 1, 
            "strategy": { 
                "value": "super_admin", 
                "label": "超级管理员" 
            }, 
        "assignees_display": ["Administrator(admin)"], 
        "assignees": [] 
        }] 
        }'

    ```