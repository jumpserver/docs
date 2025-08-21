# Slack 认证

## 1 关于 Slack

!!! info "注: Slack 认证方式为 JumpServer 企业版功能。"
!!! tip ""
    - 进入 **系统设置**，点击 **认证设置 > Slack**，进入 Slack 配置页面。
    - **Slack** 认证是基于 Slack 平台的身份认证机制，允许用户使用 Slack 账户安全登录企业应用程序。JumpServer 支持标准 Slack 认证。

## 2 配置参数

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| Slack | 勾选启用 Slack 身份验证 | 启用/禁用 |
| Client ID | Slack Client ID，这是 Slack 应用程序的唯一标识符，用于在 OAuth 2.0 授权过程中标识应用程序 |  |
| Client secret | Slack Client secret，这是与 Slack 应用程序关联的机密字符串，用于在 OAuth 2.0 令牌交换过程中对应用程序进行身份认证 |   |
| Client bot token | Slack Client bot token，这是授予 Slack 机器人的访问令牌，允许它与 Slack 工作区交互并执行发送消息或管理频道等任务 |  |
| 映射属性 | 用户属性映射。键表示 JumpServer 用户属性名称，值对应 Slack 用户属性名称 | 示例见下文 |
| 组织 | 经过身份认证和创建后，用户将被添加到所选组织中 | 默认值：`DEFAULT` |

Slack 用户属性示例
!!! tip ""
    -  **映射属性** 字段用于设置用户属性映射。键表示 JumpServer 用户属性名称，值对应 Slack 用户属性名称。

```json
{
  "name": "real_name",
  "username": "name",
  "email": "profile.email"
}
```

## JumpServer Slack URL 说明

| URL 类型 | 地址 | 说明 |
|----------|------|------|
| 二维码登录 URL | `https://jumpserver.example.com/core/auth/slack/qr/login/` | Slack 二维码登录入口 |
| 二维码登录回调 URL | `https://jumpserver.example.com/core/auth/slack/qr/login/callback/` | 二维码登录成功回调地址 |
