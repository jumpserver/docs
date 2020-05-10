# 分布式部署

!!! warning "本文档不应该直接使用在生产环境"

!!! info "说明"
    本文档需要非常专业的能力来解决一些集群问题，如集群崩溃 集群分离 集群扩展 lvs 负载均衡策略 故障排查 以及 集群组件存活检测机制等。在这些问题上你可能无法获得 JumpServer 额外的技术支持。

## 环境说明

- 系统: CentOS 7
- NFS IP: 192.168.100.99
- Mariadb IP: 192.168.100.10
- Redis ip: 192.168.100.20
- Core IP: 192.168.100.30 192.168.100.31
- koko IP: 192.168.100.40 192.168.100.41
- Guacamole IP: 192.168.100.50 192.168.100.51
- Tengine IP: 192.168.100.100

## 安全说明

- ssh、telnet 协议资产的防火墙设置允许 koko 与 core 访问
- rdp、vnc 协议资产的防火墙设置允许 guacamole 与 core 访问

## 其他

- 最终用户都是通过 Tengine 反向代理访问
- 负载均衡模式, 七层使用 session_sticky, 四层用 least_conn
- jumpserver/data 目录需要同步
- koko 需要使用同一个 redis

!!! tip "生产建议"
    你也可以使用如 NetScaler 类似的硬件或者软件来进行负载均衡策略，请处理好 session 问题  
    在生产环境中，你应该替换 nfs 为更强大的分布式文件系统，如： Ceph  
    如果你的设备很多使用人数也很多，你应该部署分布式关系型数据库  
    你应该部署多个独立的 Redis 负载均衡进行容错（当前版本的 JumpServer 还不支持 Redis Cluster）  
    Tengine RPM 使用 [wojiushixiaobai][wojiushixiaobai] 维护的一个 rpm 包，在生产环境中你应该自行编译

[wojiushixiaobai]: https://github.com/wojiushixiaobai/tengine-rpm