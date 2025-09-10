## 1. 查询节点
!!! tip "请求示例"
    ```sh
    curl -X GET 'https://localhost/api/v1/assets/nodes/?search=/Default/xx公司' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
| 参数名 | 类型   | 描述               | 是否必选 | 可选值 |
|--------|--------|--------------------|----------|--------|
| search | String | 搜索词             | 否       | -      |
| limit  | int    | 每一页显示条数，支持节点名搜索 | 是       | -      |
| offset | int    | 分页偏移量         | 是       | -      |

## 2. 创建节点
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/assets/nodes/3728f004-99a2-4fca-9577-84d5ffcf9eff/children/' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d '{"value":"test_create_node"}'
    ```
| 参数名 | 类型   | 描述     | 是否必选 | 可选值 |
|--------|--------|----------|----------|--------|
| value  | String | 节点名称 | 是       | -      |


## 3. 删除节点
!!! tip "请求示例"
    ```sh
    curl -X DELETE 'https://localhost/api/v1/assets/nodes/89c68ef6-7790-4f20-8f8d-fdd76d229b3d/' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
        -d '{"value":"test_create_node"}'
    ```
