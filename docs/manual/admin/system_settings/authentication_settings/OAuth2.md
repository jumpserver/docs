
## 1 关于 OAuth2

!!! info "注: OAuth2 认证方式为 JumpServer 企业版功能。"
!!! tip ""
    - 通过点击页面右上角小齿轮进入 **系统设置** 页面，点击 **认证设置 > OAuth2** ，进入 OAuth2 配置页面。
    - **OAuth2** 是一种开放三方授权协议，JumpServer 支持标准 OAuth2 平台认证。

## 2 配置参数

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| OAuth2 | 启用 OAuth2 身份认证 | 启用/禁用 |
| 服务提供商 | OAuth2 服务提供商名称 | `GitHub`、`Google`、`Facebook` 等 |
| 图标 | 登录页面显示的服务商图标，建议 64x64 像素 |  |
| 客户端 ID | OAuth2 服务商提供的 Client ID |  |
| 客户端密钥 | OAuth2 服务商提供的 Client Secret |  |
| 客户端认证方式 | 获取令牌的认证方式，详见下方说明 |  |
| 范围(Scope) | 授权请求的 Scope 范围，空格分隔 | `user user:email user:login` |
| 授权端点地址 | OAuth2 授权(Authorization)Endpoint | `https://github.com/login/oauth/authorize` |
| Token 端点地址 | OAuth2 Token(令牌)Endpoint | `https://github.com/login/oauth/access_token` |
| 用户信息端点地址 | OAuth2 用户信息(UserInfo)Endpoint | `https://api.github.com/user` |
| 注销会话端点地址 | OAuth2 注销(Logout)Endpoint，用户注销时调用 | `https://github.com/logout` |
| 映射属性 | 用户属性映射，JumpServer 字段与 OAuth2 字段对应关系 | 见下方 JSON 示例 |
| 组织 | 认证和创建后，用户将被添加到所选组织 | 默认：DEFAULT |
| 总是更新用户信息 | 启用后，每次认证均同步用户信息(仅限姓名、用户名、邮箱、电话、评论，组仅首次同步) | 启用/禁用 |
| 同步注销 | 启用后，注销时同步注销 OAuth2 服务 | 启用/禁用 |

!!! tip ""
    - 客户端认证方式说明:

| 请求方法 | 描述 |
|-----------|------------------------------------------------------------|
| GET       | 使用 GET 方法获取令牌，客户端 ID 和密钥在请求头中传递 |
| POST-DATA | 使用 POST 方法，客户端 ID 和密钥作为表单数据传递 |
| POST-JSON | 使用 POST 方法，客户端 ID 和密钥作为 JSON 数据传递 |


!!! tip ""
    - 属性映射示例:

```json
{
  "name": "user",
  "username": "name",
  "email": "user:email"
}
```

## 3 JumpServer OAuth2 URL 说明

| URL 类型 | 地址 | 说明 |
|----------|------|------|
| Login URL | `https://jumpserver.example.com/core/auth/oauth2/login/` | OAuth2 登录入口地址 |
| Login Success Callback URL | `https://jumpserver.example.com/core/auth/oauth2/callback/` | OAuth2 登录成功后的回调地址 |
| Logout URL | `https://jumpserver.example.com/core/auth/oauth2/logout/` | OAuth2 注销地址 |