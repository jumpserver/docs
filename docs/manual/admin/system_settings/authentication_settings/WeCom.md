# 企业微信认证

## 1 关于企业微信认证

!!! info "注: 企业微信认证方式为 JumpServer 企业版功能。"
!!! tip ""
    - 进入 **系统设置** 页面，点击 **认证设置 > 企业微信** ，进入 企业微信 配置页面。
    - **企业微信认证** 是基于企业微信的身份认证方法，JumpServer 支持二维码登录和企业身份绑定。

## 2 基础配置

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

!!! tip ""
    -  **映射属性** 字段用于设置用户属性映射。键表示 JumpServer 用户属性名称，值对应企业微信用户属性名称。
    -  企业微信用户属性示例：

```json
{
  "name": "alias",
  "username": "userid",
  "email": "extattr.attrs[2].value"
}
```

## JumpServer 企业微信 URL 说明

| URL 类型 | 地址 | 说明 |
|----------|------|------|
| 二维码登录 URL | `https://jumpserver.example.com/core/auth/wecom/qr/login/` | 企业微信二维码登录入口 |
| 二维码登录回调 URL | `https://jumpserver.example.com/core/auth/wecom/qr/login/callback/` | 二维码登录成功回调地址 |
| OAuth 登录 URL | `https://jumpserver.example.com/core/auth/wecom/oauth/login/` | 企业微信 OAuth 登录入口 |
| OAuth 登录回调 URL | `https://jumpserver.example.com/core/auth/wecom/oauth/login/callback/` | OAuth 登录成功回调地址 |
