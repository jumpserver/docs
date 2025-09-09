**1. 创建资产账号**
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/accounts/accounts/' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d '{ 
                "privileged":true, 
                "secret_type":"password", 
                "push_now":false, 
                "is_active":true, 
                "name":"root", 
                "username":"root", 
                "secret":"ThisIsPassword", 
                "asset":"09e1e072-1498-42f7-a6b1-567c2db56f59" 
            }'
    ```

**2. 删除资产账号**
!!! tip "请求示例"
    ```sh
    curl -X DELETE 'https://localhost//api/v1/perms/accounts/accounts/1b56ff93-18e9-478e-97c2-8b6a3720b95d/' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'
    ```
**3. 更新资产账号**
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/accounts/accounts/f3280232-113a-4135-a908-eddd1d9f27b6' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d '{ 
                "privileged":true, 
                "secret_type":"password", 
                "push_now":false, 
                "is_active":true, 
                "name":"root", 
                "username":"root", 
                "secret":"ThisIsPassword", 
                "asset":"09e1e072-1498-42f7-a6b1-567c2db56f59" 
            }'
    ```
**4. 查询账号**
!!! tip "请求示例"
    ```sh
    curl -X GET 'https://localhost/api/v1/accounts/accounts/?node_id=&asset_id=a014d307-7c2b-4788-a3e0
    aebd01ddf761&has_secret=true&offset=0&limit=15' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
**5. 查询密码**
!!! warning "前提条件"
    默认查询密码需要MFA，直接调用该接口需要在配置文件中设置参数：
    ```sh
    SECURITY_VIEW_AUTH_NEED_MFA=False
    ```
    修改参数后需要重启 JMS 服务: jmsctl restart
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/accounts/account-secrets/1e28b088-c86c-41b7-a85b-29e15c7cc8cb/' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'  
    ```

