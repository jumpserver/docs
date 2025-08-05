# 钉钉认证

## 关于钉钉

!!! info ""
    - **钉钉** 认证是基于钉钉的身份认证方法，支持 OAuth 2.0 授权、二维码登录和企业身份绑定，实现安全便捷的企业用户登录和管理。

## 基础配置

!!! tip ""
    - 点击页面右上角的设置按钮
    - 导航至 **系统设置 > 认证设置 > 企业微信**

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| 启用钉钉认证 | 勾选启用钉钉身份验证 | 启用/禁用 |
| Agent ID | 钉钉 Agent ID，该 ID 唯一标识企业内的微型应用程序，主要用于发送工作通知 |  |
| App key | 钉钉应用程序密钥，这是应用程序的唯一标识符，类似于 API 访问的用户名 |  |
| App secret | 钉钉应用程序密钥，类似于 API 访问的密码，用于获取调用钉钉 API 的 访问令牌 |   |
| 映射属性 | 用户属性映射。键表示 JumpServer 用户属性名称，值对应钉钉用户属性名称 | 示例见下文 |
| 组织 | 经过身份认证和创建后，用户将被添加到所选组织中 | 默认值：`DEFAULT` |

钉钉用户属性示例
!!! tip ""
    -  **映射属性** 字段用于设置用户属性映射。键表示 JumpServer 用户属性名称，值对应钉钉用户属性名称。

```json
{
  "name": "name",
  "username": "name",
  "email": "email"
}
```

## 测试钉钉连接
!!! tip ""
    - 点击页面右上角的设置按钮

    - 导航到 **系统设置 > 认证设置 > 钉钉**

    - 滚动到页面底部。

    - 点击 **测试**。

## JumpServer 钉钉 URLs
二维码登录 URL
```bash
https://jumpserver.example.com/core/auth/dingtalk/qr/login/
```
二维码登录成功回调 URL
```bash
https://jumpserver.example.com/core/auth/dingtalk/qr/login/callback/
```
OAuth 登录 URL
```bash
https://jumpserver.example.com/core/auth/dingtalk/oauth/login/
```
OAuth 登录成功回调 URL
```bash
https://jumpserver.example.com/core/auth/dingtalk/oauth/login/callback/
```
