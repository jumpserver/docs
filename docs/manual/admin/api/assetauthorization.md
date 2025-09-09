**1. 创建资产授权**
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/perms/asset-permissions/' \ 
     -H 'Content-Type:application/json' \ 
     -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
     -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
     -d '{ 
            "name":"create_asset_permission", 
            "user_groups":[{"pk":"745980b1-54be-4c5e-b6ab-89826c2e2054"}], 
            "nodes":["3728f004-99a2-4fca-9577-84d5ffcf9eff"], 
            "accounts":["@ALL"], 
            "actions":["connect","upload","download","copy","paste"],
             "is_active":true, 
            "date_start":"2023-02-23T10:53:23.879Z", 
            "date_expired":"2123-01-30T10:53:23.879Z" 
        }'
    ```
**2. 删除资产授权**
!!! tip "请求示例"
    ```sh
    curl -X DELETE 'https://localhost/api/v1/perms/asset-permissions/b2c45ce6-6b9c-4270-a073-567ff0e0ade8/' \ 
    -H 'Content-Type:application/json' \ 
    -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
    -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
**3. 更新资产授权**
!!! tip "请求示例"
    ```sh
    curl -X PUT 'https://localhost/api/v1/perms/asset-permissions/ca90421b-bc45-48c0-bd49-4a213ff61b7c/' \ 
    -H 'Content-Type:application/json' \ 
    -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
    -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
    -d '{ 
            "name":"create_asset_permission", 
            "user_groups":[{"pk":"745980b1-54be-4c5e-b6ab-89826c2e2054"}], 
            "nodes":["3728f004-99a2-4fca-9577-84d5ffcf9eff"], 
            "accounts":["@ALL"], 
            "actions":["connect","upload","download","copy","paste"], 
            "is_active":true, 
            "date_start":"2023-02-23T10:53:23.879Z", 
            "date_expired":"2123-01-30T10:53:23.879Z" 
        }'
    ```
