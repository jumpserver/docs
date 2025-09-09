**1. 查询用户**
!!! tip ""
    请求示例
    ``` sh
    curl -X GET 'https://localhost/api/v1/users/users/?offset=0&limit=15' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
**2. 创建用户**
!!! tip ""
    请求示例
    ``` sh
    curl -X POST 'https://localhost/api/v1/users/users/' \ 
     -H 'Content-Type:application/json' \ 
     -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
     -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
     -d '{ 
             "name":"test_create_user_1", 
             "username":"test_create_user_1", 
             "password_strategy":"email", 
             "email":"test_create_user_1@fit2cloud.com", 
             "mfa_level":0, 
             "source":"local", 
             "date_expired":"2093-02-05T08:28:41.726694Z", 
             "system_roles": 
             [ 
                 { 
                     "pk":"00000000-0000-0000-0000-000000000003" 
                 } 
             ], 
             "org_roles": 
             [ 
                 { 
                     "pk":"00000000-0000-0000-0000-000000000007"
                      } 
             ] 
        }'
    
    ```

**3. 删除用户**
!!! tip ""
    请求示例
    ``` sh
    curl -X DELETE 'https://localhost/api/v1/users/users/cdd61c0e-2012-416a-bde3-f2c642ded82a/' \ 
     -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
     -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'
    ```

**4. 更新用户**
!!! tip ""
    请求示例
    ``` sh
    curl -X PUT 'https://localhost/api/v1/users/users/cdd61c0e-2012-416a-bde3-f2c642ded82a/' \ 
     -H 'Content-Type:application/json' \ 
     -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
     -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
     -d '{ 
             "name":"test_create_user_1", 
             "username":"test_create_user_1", 
             "password": "Password@123", 
             "email":"test_create_user_1@fit2cloud.com", 
             "mfa_level":0, 
             "source":"local", 
             "date_expired":"2093-02-05T08:28:41.726694Z", 
             "system_roles": 
             [ 
                 { 
                     "pk":"00000000-0000-0000-0000-000000000001" 
                 } 
             ], 
             "org_roles": 
             [ 
                 { 
                     "pk":"00000000-0000-0000-0000-000000000005" 
                 } 
             ] 
        }' 
    ```
