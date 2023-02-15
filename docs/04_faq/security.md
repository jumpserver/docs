# 安全建议

## 1 基本安全要求
!!! tip ""
    - JumpServer 对外最低需要开放 80 443 2222 端口。
    - JumpServer 所在服务器操作系统应该升级到最新。
    - JumpServer 依赖的软件应该升级到最新版本。
    - 服务器、数据库、Redis 等依赖组件请勿使用弱口令密码。 
    - 不推荐关闭 Firewalld 和 Selinux。
    - 只开放必要的端口，必要的话请通过 VPN 或者 SSLVPN 访问 JumpServer。
    - 如果必须开放到外网使用，你应该部署 Web 应用防火墙做安全过滤。
    - 请部署 SSL 证书通过 HTTPS 协议来访问 JumpServer。
    - JumpServer 应该在安全设置强密码规则，禁用用户使用弱口令密码。
    - 应该开启 JumpServer MFA 认证功能，避免因密码泄露导致的安全问题。

!!! warning "注意"
    - 如发现 JumpServer 安全问题，请反馈给我们 ibuler@fit2cloud.com

## 2 安全配置建议
!!! tip ""
    - [Linux 常见高危命令汇总](https://kb.fit2cloud.com/?p=173){:target="_blank"}
    - [设置某个资产只允许通过某个 IP 登录 JumpServer 之后进行连接](https://kb.fit2cloud.com/?p=199){:target="_blank"}
    - [JumpServer 使用用户自己的 SSL 证书进行访问](https://kb.fit2cloud.com/?p=152){:target="_blank"}
    - [JumpServer 增强用户登录的安全性](https://kb.fit2cloud.com/?p=71){:target="_blank"}
    - [JumpServer 登录资产用户切换](https://kb.fit2cloud.com/?p=65){:target="_blank"}
    - [JumpServer 高危命令限制](https://kb.fit2cloud.com/?p=63){:target="_blank"}
    - [限制来源 IP 登录 JumpServer 堡垒机](https://kb.fit2cloud.com/?p=43){:target="_blank"}
    - [JumpServer 常用的 MFA 工具](https://kb.fit2cloud.com/?p=6){:target="_blank"}
    - [JumpServer 设置会话过期时间](https://kb.fit2cloud.com/?p=5){:target="_blank"}
