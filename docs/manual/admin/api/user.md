## 1. 查询用户
!!! tip ""
    请求示例
    ``` sh
    curl -X GET 'https://localhost/api/v1/users/users/?offset=0&limit=15' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
     
| 参数名       | 类型    | 描述                                                                 | 是否必选 | 可选值                                                                 |
|--------------|---------|----------------------------------------------------------------------|----------|------------------------------------------------------------------------|
| id           | String  | ID                                                                   | 否       | -                                                                      |
| name         | String  | 名称                                                                 | 否       | -                                                                      |
| username     | String  | 用户名                                                               | 否       | -                                                                      |
| email        | String  | 邮箱                                                                 | 否       | -                                                                      |
| source       | String  | 来源                                                                 | 否       | 数据库：local、ldap、openid、radius、cas、saml2、oauth2、custom、FIT2CLOUD |
| system_roles | String  | 系统角色                                                             | 否       | -                                                                      |
| org_roles    | String  | 组织角色                                                             | 否       | -                                                                      |
| is_active    | Boolean | 是否激活                                                             | 否       | -                                                                      |
| limit        | int     | 每一页显示条数                                                       | 是       | -                                                                      |
| offset       | int     | 分页偏移量                                                           | 是       | -                                                                      |


## 2. 创建用户
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

    
| 参数名                 | 类型           | 描述                                   | 是否必选 | 可选值                                                         |
|------------------------|----------------|----------------------------------------|----------|----------------------------------------------------------------|
| name                   | String         | 名称                                   | 是       | -                                                              |
| username               | String         | 用户名                                 | 是       | -                                                              |
| email                  | String         | 邮箱                                   | 是       | -                                                              |
| wechat                 | String         | 微信                                   | 否       | -                                                              |
| phone                  | String         | 手机                                   | 否       | -                                                              |
| groups                 | String[]       | 用户组id                               | 否       | -                                                              |
| password               | String         | 密码                                   | 是       | -                                                              |
| need_update_password   | Boolean        | 是否下一次登录修改密码                 | 否       | 默认：false；可选值：[true，false]                             |
| public_key             | String         | SSH 公钥                               | 否       | -                                                              |
| system_roles           | String[]       | 系统角色                               | 是       | pk : 系统角色id                                                |
| org_roles              | String[]       | 组织角色                               | 是       | pk : 组织角色id                                                 |
| password_strategy      | String         | 密码策略                               | 否       | 可选值：[ email, custom ]；email : 通过邮件设置密码；custom : 设置密码 |
| source                 | String         | 来源                                   | 否       | 默认值：default；可选值：[ local、ldap、openid、radius、cas、saml2、oauth2、custom ] |
| mfa_level              | Integer        | MFA                                    | 否       | 可选值：[ 0, 1, 2 ]；0 : 禁用；1 : 启用；2 : 强制启用           |
| data_expored           | String(datatime) | 用户失效时间                           | 否       | 格式：2023-02-04T00:54:39.000Z                                 |


## 3. 删除用户
!!! tip ""
    请求示例
    ``` sh
    curl -X DELETE 'https://localhost/api/v1/users/users/cdd61c0e-2012-416a-bde3-f2c642ded82a/' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'
    ```

## 4. 更新用户
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

| 参数名                 | 类型           | 描述                                   | 是否必选 | 可选值                                                         |
|------------------------|----------------|----------------------------------------|----------|----------------------------------------------------------------|
| name                   | String         | 名称                                   | 是       | -                                                              |
| username               | String         | 用户名                                 | 是       | -                                                              |
| email                  | String         | 邮箱                                   | 是       | -                                                              |
| wechat                 | String         | 微信                                   | 否       | -                                                              |
| phone                  | String         | 手机                                   | 否       | -                                                              |
| groups                 | String[]       | 用户组id                               | 否       | -                                                              |
| password               | String         | 密码                                   | 是       | -                                                              |
| need_update_password   | Boolean        | 是否下一次登录修改密码                 | 否       | 可选值：[true，false]                                          |
| password_strategy      | String         | 密码策略                               | 否       | 可选值：[ email, custom ]；email : 通过邮件设置密码；custom : 自定义设置密码 |
| public_key             | String         | SSH 公钥                               | 否       | -                                                              |
| system_roles           | String[]       | 系统角色                               | 是       | pk : 系统角色id                                                |
| org_roles              | String[]       | 组织角色                               | 是       | pk : 组织角色id                                                 |
| source                 | String         | 来源                                   | 否       | 默认值：default；可选值：[ local、ldap、openid、radius、cas、saml2、oauth2、custom ] |
| mfa_level              | Integer        | MFA                                    | 否       | 可选值：[ 0, 1, 2 ]；0 : 禁用；1 : 启用；2 : 强制启用           |
| data_expored           | String(datatime) | 用户失效时间                           | 否       | 格式：2023-02-04T00:54:39.000Z                                 |