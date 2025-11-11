
!!! info "企业版客户出现服务故障建议在企业客户支持群中联系客户成功团队获取及时帮助。"

## 1 JumpServer 程序故障

当出现组件容器异常高负载或者当容器健康为 unhealthy 时可以通过以下方案临时恢复。

**方案一：重启故障容器**

```bash
# 重启故障容器 或者通过 `jmsctl restart [core/celery/koko/chen/lion]` 重建容器。
docker restart <容器名>
# 检查所有组件运行状态
jmsctl status 

```

**方案二：全部重启**

```bash
# 进入安装包目录
cd /opt/jumpserver-ee-{{ jumpserver.tag }}-x86_64
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

## 2 数据库故障

1. 备份数据库：

 ```bash
 jmsctl backup_db
 ```

2. 登录数据库服务器，停止 JumpServer 服务（避免数据写入冲突）：

 ```bash
 jmsctl stop
 ```

3. 检查数据库具体故障原因（如服务未启动、配置错误、磁盘空间不足等），针对性修复；
4. 修复完成后，启动数据库服务，再重启 JumpServer：

 ```bash
 jmsctl start
 ```

## 3 服务器宕机

1. 优先恢复服务器硬件/系统，确保服务器能正常运行；
2. 检查数据库状态（内置/外置），按照 [数据库故障](./crash_recovery.md) 的处理方式恢复数据库；
3. 启动相关依赖服务：
 ```bash
 # 若使用 Keepalived，启动 Keepalived 服务
 systemctl start keepalived
 # 启动 JumpServer 服务
 jmsctl start
 ```
1. 通过 `jmsctl status` 检查服务状态。

## 4 安全建议

> 1. 定期备份 JumpServer 数据库，避免数据丢失导致业务中断，建议结合业务场景设置每日/每周备份频率。
> 2. 定期备份 JumpServer 核心配置文件（如 `config.txt` 及各类组件配置文件），便于故障时快速恢复环境。
> 3. 全局开启 MFA（多因素认证）功能，通过二次验证提升账户安全性，降低因密码泄露引发的安全风险。
> 4. 开启账户备份计划，定期将关键账户信息备份至指定邮箱，作为账户异常时的应急逃生方案。
