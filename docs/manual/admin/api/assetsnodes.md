**1. 查询节点**
!!! tip "请求示例"
    ```sh
    curl -X GET 'https://localhost/api/v1/assets/nodes/?search=/Default/xx公司' \ 
        -H 'Content-Type:application/json' \ 
        -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
        -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' 
    ```
**2. 创建节点**
!!! tip "请求示例"
    ```sh
    curl -X POST 'https://localhost/api/v1/assets/nodes/3728f004-99a2-4fca-9577-84d5ffcf9eff/children/' \ 
    -H 'Content-Type:application/json' \ 
    -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
    -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
    -d '{"value":"test_create_node"}'
    ```

**3. 删除节点**
!!! tip "请求示例"
    ```sh
    curl -X DELETE 'https://localhost/api/v1/assets/nodes/89c68ef6-7790-4f20-8f8d-fdd76d229b3d/' \ 
    -H 'Content-Type:application/json' \ 
    -H 'Authorization: Bearer b96810faac725563304dada8c323c4fa061863d4' \ 
    -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002' \ 
    -d '{"value":"test_create_node"}'
    ```