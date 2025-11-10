## 故障恢复

JumpServer 整个环境的故障情况分为三种：JumpServer 程序宕机、数据库宕机、服务器宕机。

### JumpServer 程序故障

**方案一：重启故障容器**
!!! tip ""
    ```bash
    docker restart 容器名
    ```

**方案二：全部重启（彻底恢复）**
!!! tip ""
    ```bash
    # 进入安装包目录
    cd /opt/jumpserver-ee-v4.10.6-x86_64
    # 停止 JumpServer 所有服务
    ./jmsctl.sh down
    # 检查是否有未停止的容器
    docker ps -a
    # 若有未停止的容器，执行强制停止并删除（替换 ID 为实际容器 ID）
    docker kill ID
    docker rm ID
    # 启动 JumpServer 服务（若个别组件启动不成功，可稍等后再次执行启动命令）
    ./jmsctl.sh start
    # 检查 JumpServer 启动状态
    ./jmsctl.sh status
    ```

### 数据库故障

**单机数据库**
1. 优先备份数据库；
2. 登录数据库服务器，停止 JumpServer 服务（避免数据写入冲突）：

!!! tip ""
    ```bash
    jmsctl stop
    ```
3. 检查数据库具体故障原因（如服务未启动、配置错误、磁盘空间不足等），针对性修复；
4. 修复完成后，启动数据库服务，再重启 JumpServer：
!!! tip ""
    ```bash
    jmsctl start
    ```

### 服务器宕机
1. 优先恢复服务器硬件/系统，确保服务器能正常运行；
2. 检查数据库状态（内置/外置），按照 **数据库故障** 的处理方式恢复数据库（主从架构需重新确认主从同步状态）；
3. 启动相关依赖服务：
!!! tip ""
    ```bash
    # 若使用 Keepalived，启动 Keepalived 服务
    systemctl start keepalived
    # 启动 JumpServer 服务
    jmsctl start
    ```
4. 验证服务可用性：
   - 访问 Web 界面确认正常
   - 执行 `jmsctl status` 检查所有组件运行状态
   - 测试资产连接、会话录像等核心功能