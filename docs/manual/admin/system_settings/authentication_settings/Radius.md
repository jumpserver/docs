# Radius 认证

## 1 关于 RADIUS
!!! info "注: RADIUS 认证方式为 JumpServer 企业版功能。"
!!! tip ""
    - 通过点击页面右上角小齿轮进入 **系统设置** 页面，点击 **认证设置 > Radius** ，进入 RADIUS 配置页面。
    - **RADIUS（远程身份认证拨入用户服务）** 是一种基于 RADIUS 协议的网络访问控制认证机制，提供身份认证、授权和计费（AAA）功能。JumpServer 支持标准 RADIUS 认证。

## 2 配置参数

!!! tip ""
    - 点击页面右上角的设置按钮
    - 导航到 **系统设置 > 认证设置 > Radius**

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| Radius | 勾选启用 Radius 身份验证 | 启用/禁用 |
| 主机 | RADIUS 服务器 IP 地址或域名 | `172.16.10.180` |
| 端口 | RADIUS 服务器端口号 | 默认值：1812  |
| 密文 | JumpServer 和 RADIUS 服务器之间的共享密钥。它的功能类似于密码，对 RADIUS 请求和响应中的敏感信息进行加密，以确保安全通信 |  |
| 使用 radius OTP | 勾选启用 RADIUS 作为 MFA 后端。有关更多信息，请参阅下文启用 RADIUS MFA 后端 | 启用/禁用 |
| 组织 | 经过身份认证和创建后，用户将被添加到所选组织中 | 默认值：`DEFAULT` |

启用 RADIUS MFA 后端

!!! tip ""
    - 按照集成 RADIUS 身份认证指南配置 RADIUS 身份认证。
    - 在 **使用 radius OTP** 字段中，勾选启用 RADIUS 作为 MFA 后端。当用户的 MFA 启用时，他们可以在登录时选择 RADIUS 身份认证类型。
    - 点击 **提交**。