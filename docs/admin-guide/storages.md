# 存储说明

## 命令存储

!!! info "`终端管理` - `存储配置` - `命令存储` - `新建` - `Elasticsearch`"

| 名称     | 示例                    | 说明            |
| :------- | :--------------------- | :-------------- |
| 名称     | jms_es                  | 标识用, 不可重复 |
| 类型     | Elasticsearch           | 必填, 无法更改   |
| 主机     | http://172.16.11.3:9200 | http://es_user:es_password@es_host:es_port |
| 索引     | jumpserver              | 索引             |
| 文档类型 | command                 | 必填, 无法更改   |
| 备注     | es 测试服务器            | 仅标识, 可不填   |     

!!! info "在 `终端管理` 页面选择 `更新` 组件, 把命令存储修改成刚才创建的 es 服务器即可"
    - 修改完成后, 大概需要 1 分钟的时间完成同步, 也可以通过重启 jms_koko 来立即生效

    ```sh
    docker restart jms_koko
    ```


## 录像存储

!!! info "`终端管理` - `存储配置` - `录像存储` - `新建`"

!!! info "在 `终端管理` 页面选择 `更新` 组件"
    - 选择你需要的存储方式即可, 大概需要 1 分钟的时间完成同步
    - 之前已经存储在本地的录像需要自己手动上传到你新的存储环境


## 日志存储

!!! info "对接 syslog"
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim
    # 加入 syslog 相关设置
    SYSLOG_ENABLE=true
    SYSLOG_ADDR=192.168.100.215:514
    ```
    ```sh
    ./jmsctl.sh restart
    ```
