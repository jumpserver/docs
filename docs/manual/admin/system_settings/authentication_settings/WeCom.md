# 企业微信认证

## 关于企业微信

!!! info ""
    - **企业微信** 认证是基于企业微信的身份认证方法，支持 OAuth 2.0 授权、二维码登录和企业身份绑定，实现安全便捷的企业用户登录和管理。

## 基础配置

!!! tip ""
    - 点击页面右上角的设置按钮
    - 导航至 **系统设置 > 认证设置 > 企业微信**

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| 企业微信 | 勾选启用企业微信身份验证 | 启用/禁用 |
| Corporation ID | 企业微信公司 ID。唯一标识企业微信中的企业，所有 API 请求都必须包含此 ID |  |
| App agent ID | 企业微信应用代理 ID。用于标识企业微信中的特定应用程序，每个应用程序都有一个唯一的代理 ID |  |
| App secret | 企业微信应用程序密钥。用于验证应用程序并获取调用企业微信 API 的访问令牌 |   |
| 映射属性 | 用户属性映射。键表示 JumpServer 用户属性名称，值对应企业微信用户属性名称 | 示例见下文 |
| 组织 | 经过身份认证和创建后，用户将被添加到所选组织中 | 默认值：`DEFAULT` |

企业微信用户属性示例
!!! tip ""
    -  **映射属性** 字段用于设置用户属性映射。键表示 JumpServer 用户属性名称，值对应企业微信用户属性名称。

```json
{
  "name": "alias",
  "username": "userid",
  "email": "extattr.attrs[2].value"
}
```

## 测试企业微信连接
!!! tip ""
    - 点击页面右上角的设置按钮

    - 导航至 **系统设置 > 认证设置 > 企业微信**

    - 滚动至页面底部。

    - 点击 **测试**。

## JumpServer 企业微信 URLs
二维码登录 URL
```bash
https://jumpserver.example.com/core/auth/wecom/qr/login/
```
二维码登录成功回调 URL
```bash
https://jumpserver.example.com/core/auth/wecom/qr/login/callback/
```
OAuth 登录 URL
```bash
https://jumpserver.example.com/core/auth/wecom/oauth/login/
```
OAuth 登录成功回调 URL
```bash
https://jumpserver.example.com/core/auth/wecom/oauth/login/callback/
```
