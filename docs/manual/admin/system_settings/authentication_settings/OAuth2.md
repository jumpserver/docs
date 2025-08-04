# OAuth2 认证

## 关于 OAuth2

!!! info ""
    - **开放授权2.0(OAuth2)** 是一种开放授权协议，允许第三方应用程序访问存储在其他服务提供商(如 Google、Facebook、GitHub 等)上的用户资源，而无需暴露用户的密码。OAuth2 允许用户在不共享登录凭据的情况下授予第三方应用程序特定的资源权限。

## 基础配置

!!! tip ""
    - 点击页面右上角的设置按钮
    - 导航至 **系统设置 > 认证设置 > OAuth2**

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| OAuth2 | 勾选启用 OAuth2 身份验证 | 启用/禁用 |
| 服务提供商 |  OAuth2 服务提供商名称 | 如 `Github、Google、Facebook` 等 |
| 图标 | OAuth2 服务提供商图标，推荐使用 64px * 64px 的大小。服务提供商和图标将显示在登录页面上 | 示例见下文 |
| 客户端 ID | OAuth2 服务提供商提供的客户端 ID |   |
| 客户端密钥 | OAuth2 服务提供商提供的客户端密钥 |  |
| 客户端认证方式 | 获取令牌的一种方法 | 示例见下文 |
| 范围 | 定义客户端在授权请求中请求访问的用户信息的范围 | 多条信息用空格分隔，例如 `user user:email user:login` |
| 授权端点地址 | OAuth2 授权端点地址 | `https://github.com/login/oauth/authenticate` |
| Token 端点地址 | OAuth2 Token 端点地址 | `https://github.com/login/oauth/access_token` |
| 用户信息端点地址 | OAuth2 用户信息端点地址 | `https://api.github.com/user` |
| 注销会话端点地址 | 用 OAuth2 注销会话端点地址，当用户注销时，将调用此端点 | `https://github.com/logout` |
| 映射属性 | 用户属性映射。键表示 JumpServer 用户属性名称，值对应 OAuth2 用户属性名称 | 示例见下文 |
| 组织 | 经过身份认证和创建后，用户将被添加到所选组织中 | 默认值：DEFAULT |
| 总是更新用户信息 | 勾选后，在 OAuth2 用户身份认证后，每次都会更新用户信息(仅包括：姓名、用户名、电子邮件、电话、评论)，“组”仅在创建用户时同步 | 启用/禁用 |
| 同步注销 | 勾选后，用户将在注销时通过调用“结束会话端点地址”从 OAuth2 服务中注销 | 启用/禁用 |

OAuth2 图标配置成功后的登录页面示例
![OAuth2图1](../../../../img/V4_OAuth2_1.png)

OAuth2 客户端认证方式示例
!!! tip "客户端认证的三种方式"

    | 请求方法      | 描述                                                         |
    | ------------- | ------------------------------------------------------------ |
    | GET       | 使用 GET 方法获取令牌，请求标头中包含客户端 ID 和客户端密钥。  |
    | POST-DATA | 使用 POST 方法获取令牌，其中客户端 ID 和客户端密钥作为“原始数据”包含在请求体中。 |
    | POST-JSON | 使用 POST 方法获取令牌，其中客户端 ID 和客户端密钥作为“JSON 数据”包含在请求体中。 |

OAuth2 用户属性示例
!!! tip ""
    -  **映射属性** 字段用于设置用户属性映射。键表示 JumpServer 用户属性名称，值对应 OAuth2 用户属性名称。

```json
{
  "name": "user",
  "username": "name",
  "email": "user:email"
}
```

## JumpServer OAuth2 URLs
登录 URL
```bash
https://jumpserver.example.com/core/auth/oauth2/login/
```
登录成功回调 URL
```bash
https://jumpserver.example.com/core/auth/oauth2/callback/
```
登出 URL
```bash
https://jumpserver.example.com/core/auth/oauth2/logout/
```