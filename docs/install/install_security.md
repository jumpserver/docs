# 安全建议

Jumpserver 对外需要开放 80 和 2222 端口，如果你配置了 ssl 还需要开放 443 端口, 8080 端口开放给 koko 和 guacamole 组件访问

- JumpServer 所在服务器操作系统应该升级到最新

- JumpServer 依赖的软件升级到最新版本

- 服务器、数据库、redis 等依赖组件请勿使用弱口令密码

- 不推荐关闭 firewalld 和 selinux

- 只开放必要的端口，必要的话请通过 vpn 或者 sslvpn 访问 JumpServer

- 如果必须开放到外网使用，你应该部署 web 应用防火墙做安全过滤

- 请部署 ssl 证书通过 https 协议来访问 JumpServer

- JumpServer 不要使用弱口令密码，应立即改掉默认的 admin 密码

- 推荐开启 MFA 功能，避免因密码泄露导致的安全问题

!!! tip ""
    关注官方更新，及时更新修复漏洞的版本  
    如发现 JumpServer 安全问题，请反馈给我们 ibuler@fit2cloud.com
