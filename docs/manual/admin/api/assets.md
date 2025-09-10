## 1. 创建主机资产
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/assets/hosts/'\ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d '{ 
             "name":"test_create_asset", 
             "address":"192.168.1.1", 
             "platform": 
             { 
                 "pk":1 
             }, 
             "nodes": 
             [ 
                 { 
                     "pk":"1ecb988f-ded3-4b57-bc8f-808467abbe2f" 
                 } 
             ], 
             "protocols": 
             [ 
                 { 
                     "name":"ssh", 
                     "port": 22 
                 } 
             ], 
             "labels":[], 
             "is_active":true, 
             "accounts":[] 
            }'
    ```
| 参数名     | 类型       | 描述                                                                 | 是否必选 | 默认值  |
|------------|------------|----------------------------------------------------------------------|----------|---------|
| name       | String     | 名称                                                                 | 是       | -       |
| addrs      | String     | IP地址                                                               | 是       | -       |
| platform   | String     | 系统平台，示例值：1（代表Linux）、5（代表Windows）                    | 是       | -       |
| nodes      | String[]   | 节点                                                                 | 是       | -       |
| protocols  | String[]   | 协议/端口，参数格式示例：`{"name": "ssh", "port": 22}`                | 否       | -       |
| labels     | String[]   | 标签                                                                 | 否       | -       |
| is_active  | Boolean    | 激活状态                                                             | 否       | true    |
| accounts   | String[]   | 账号信息                                                             | 否       | -       |

## 2. 删除资产
!!! tip "请求示例"
    ```sh
    curl -X DELETE 'https://localhost/api/v1/assets/hosts/1b56ff93-18e9-478e-97c2-8b6a3720b95d/' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer 
        b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```