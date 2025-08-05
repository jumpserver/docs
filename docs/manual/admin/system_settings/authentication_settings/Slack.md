# Slack 认证

## 关于 Slack

!!! info ""
    - **Slack** 认证是一种基于 Slack 平台的身份认证机制，允许用户使用其 Slack 帐户登录企业应用程序或第三方服务，以进行安全的身份验证和授权。

## 基础配置

!!! tip ""
    - 点击页面右上角的设置按钮
    - 导航到 **系统设置 > 认证设置 > Slack**

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

## 测试 Slack 连接
!!! tip ""
    - 点击页面右上角的设置按钮

    - 导航到 **系统设置 > 认证设置 > Slack**

    - 滚动到页面底部。

    - 点击 **测试**。

## JumpServer Slack URLs
二维码登录 URL
```bash
https://jumpserver.example.com/core/auth/slack/qr/login/
```
二维码登录成功回调 URL
```bash
https://jumpserver.example.com/core/auth/slack/qr/login/callback/
```
