# Windows RDP 资产要求

!!! info "提示"
    - 部分安装了安全软件的资产无法正常连接。
    - 创建资产的 "资产平台" 默认情况下使用 Windows 即可。

!!! tip "资产要求"
    - 打开 Windows 远程设置
    - 防火墙放行 rdp 端口
    - 创建资产时 "资产平台" 选择 Windows
    - 正常创建 RDP 账号
    - 授权后即可

!!! warning "如果资产设置了 远程(RDP)连接要求使用指定的连接层 SSL"
    - 在 JumpServer 资产管理 - 平台列表 创建一个新的平台模板。
    - 名称: Windows-SSL
    - 基础: Windows
    - 编码: UTF-8  如果复制粘贴乱码可以改成 GBK
    - RDP security: TLS
    - RDP console: 默认
    - 提交后, 修改资产的资产平台为 Windows-SSL。

!!! warning "如果资产设置了 远程(RDP)连接要求使用指定的连接层 RDP"
    - 在 JumpServer 资产管理 - 平台列表 创建一个新的平台模板
    - 名称: Windows-RDP
    - 基础: Windows  
    - 编码: UTF-8  如果复制粘贴乱码可以改成 GBK  
    - RDP security: RDP  
    - RDP console: 默认  
    - 提交后, 修改资产的资产平台为 Windows-RDP

!!! warning "域账号注意事项"
    - 如果`域账号`配置了特定的登录工作站, 则需要在 DC 域控制器的 `域用户`属性登录工作站，在里面添加 lion 的 Container ID。
    - 如不确定, 请配置为此用户可以登录到: 所有计算机(C)
