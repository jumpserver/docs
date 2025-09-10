## 1. 创建资产账号
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
| 参数名       | 类型     | 描述                                                                 | 是否必选 | 默认值       |
|--------------|----------|----------------------------------------------------------------------|----------|--------------|
| name         | String   | 名称                                                                 | 否       | -            |
| username     | String   | 用户名                                                               | 是       | -            |
| secret_type  | String   | 密文类型，可选值为 `password`（密码）、`ssh_key`（SSH 密钥）          | 是       | password     |
| secret       | String   | 密钥/密码，仅在 `secret_type` 字段选用 `password` 时启用             | 否       | -            |
| passphrase   | String   | 密钥密码，仅在 `secret_type` 字段选用 `ssh_key` 时启用                | 否       | -            |
| comment      | String   | 备注                                                                 | 否       | -            |
| assets       | String[] | 资产                                                                 | 是       | -            |
| privileged   | Boolean  | 特权账号                                                             | 否       | -            |
| push_now     | String   | 立即推送                                                             | 否       | -            |
| is_active    | Boolean  | 激活                                                                 | 否       | -            |


## 2. 删除资产账号
!!! tip "请求示例"
    ```sh
    curl -X DELETE 'https://localhost//api/v1/perms/accounts/accounts/1b56ff93-18e9-478e-97c2-8b6a3720b95d/' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'
    ```
## 3. 更新资产账号
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

| 参数名       | 类型     | 描述                                                                 | 是否必选 | 默认值       |
|--------------|----------|----------------------------------------------------------------------|----------|--------------|
| name         | String   | 名称                                                                 | 否       | -            |
| username     | String   | 用户名                                                               | 是       | -            |
| secret_type  | String   | 密文类型，可选值为 `password`（密码）、`ssh_key`（SSH 密钥）          | 是       | password     |
| secret       | String   | 密钥/密码，仅在 `secret_type` 字段选用 `password` 时启用             | 否       | -            |
| passphrase   | String   | 密钥密码，仅在 `secret_type` 字段选用 `ssh_key` 时启用                | 否       | -            |
| comment      | String   | 备注                                                                 | 否       | -            |
| assets       | String[] | 资产                                                                 | 是       | -            |
| privileged   | Boolean  | 特权账号                                                             | 否       | -            |
| push_now     | String   | 立即推送                                                             | 否       | -            |
| is_active    | Boolean  | 激活                                                                 | 否       | -            |


## 4. 查询账号
!!! tip "请求示例"
    ```sh
    curl -X GET 'https://localhost/api/v1/accounts/accounts/?node_id=&asset_id=a014d307-7c2b-4788-a3e0
    aebd01ddf761&has_secret=true&offset=0&limit=15' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
| 参数名       | 类型    | 描述               | 是否必选 | 默认值 |
|--------------|---------|--------------------|----------|--------|
| node_id      | String  | 节点ID             | 否       | -      |
| asset_id     | String  | 资产ID             | 否       | -      |
| id           | String  | 账号ID             | 否       | -      |
| username     | String  | 账号用户名         | 否       | -      |
| has_secret   | Boolean | 是否已托管密码     | 否       | -      |
| limit        | int     | 每一页显示条数     | 是       | -      |
| offset       | int     | 分页偏移量         | 是       | -      |



## 5. 查询密码
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

