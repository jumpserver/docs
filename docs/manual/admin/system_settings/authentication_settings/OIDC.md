## 1 关于OIDC

!!! info "注: OIDC 认证方式为 JumpServer 企业版功能。"
!!! tip ""
    - 通过点击页面右上角小齿轮进入 **系统设置** 页面，点击 **认证设置 > OIDC** ，进入 OIDC 配置页面。
    - **OpenID Connect(OIDC)** 是一种基于 OAuth 2.0 的身份认证协议。JumpServer 认证支持标准的 OIDC 认证。

## 2 基础配置
!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| OIDC | 勾选启用 OIDC 身份验证 | 启用/禁用 |
| JumpServer 地址 | JumpServer 的完整域名，用于构造回调 URL | `https://jumpserver.example.com/` |
| 客户端 ID | OIDC 服务器提供的客户端 ID |  |
| 客户端密钥 | OIDC 服务器提供的客户端密钥 |  |
| 客户端认证方式 | 认证方式：Client Secret Basic(使用 POST 方法获取令牌，请求标头中包含客户端 ID 和客户端密码)；Client Secret Post(使用 POST 方法获取令牌，客户端 ID 和客户端密码作为原始数据包含在请求正文中) |  |
| 使用 Keycloak | 选中使用 Keycloak 配置，或取消选中使用本机 OIDC 配置 |  |

### 2.1 使用 Keycloak

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| 服务端地址 | Keycloak 服务器 URI | `https://keycloak.example.com` |
| 域 | Keycloak 域名称 | `JumpServer` |

### 2.2 使用本机 OIDC

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| 端点地址 | OIDC 服务端基础 Endpoint，用于发现各类端点 | `https://oidc.example.com` |
| 授权端点地址 | OIDC 授权(Authorization)Endpoint | `https://oidc.example.com/realms/JumpServer/protocol/openid-connect/auth/` |
| Token 端点地址 | OIDC Token(令牌)Endpoint | `https://oidc.example.com/realms/JumpServer/protocol/openid-connect/token/` |
| JWKS 端点地址 | OIDC 公钥(JWKS)Endpoint | `https://oidc.example.com/realms/JumpServer/protocol/openid-connect/certs/` |
| 用户信息端点 | OIDC 用户信息(UserInfo)Endpoint | `https://oidc.example.com/realms/JumpServer/protocol/openid-connect/userinfo/` |
| 注销端点地址 | OIDC 注销(Logout)Endpoint，用户注销时调用 | `https://oidc.example.com/realms/JumpServer/protocol/openid-connect/logout/` |
| 签名算法 | ID Token 签名算法，支持 HS256(对称密钥)和 RS256(非对称密钥) | 默认：HS256 |
| 签名密钥 | RS256 时用于验证签名的公钥或密钥 |  |
| 启用 PKCE | 是否启用 PKCE(Proof Key for Code Exchange)增强安全性 | 建议启用 |
| 校验码方式 | PKCE 校验码生成方式：S256(推荐，SHA-256)或 Plain | 默认：S256 |
| Scope | 授权请求的 Scope 范围，空格分隔 | `openid profile email` |
| 令牌有效期(秒) | ID Token 有效期，过期后自动刷新 |  |
| 声明(Claims) | 是否在 ID Token 中包含 userinfo 范围声明 |  |
| 状态校验 | 启用后可防止 CSRF 攻击，确保请求一致性 | 建议启用 |
| 临时码校验 | 启用后可防止重放攻击 | 建议启用 |
| 总是更新用户信息 | 启用后，每次认证均同步用户信息(仅限姓名、用户名、邮箱、电话、评论，群组仅首次同步) |  |
| 忽略 SSL 证书验证 | 启用后，跳过对 OP 服务器 SSL 证书的校验 |  |
| 共享会话 | 启用后，用户在其他应用注销时会同步注销 |  |
| 属性映射 | 用户属性映射，JumpServer 字段与 OIDC 字段对应关系 | 见下方 JSON 示例 |


### 2.3 OIDC 用户属性示例

``` json
{  
	"name": "name",  
	"username": "preferred_username",  
	"email": "email",  
	"groups": "groups"
}
```

## 3 JumpServer OIDC URL 说明

!!! tip ""
    详细 URL 说明：

| URL 类型 | 地址 | 说明 |
|----------|------|------|
| 登录网址 | `https://jumpserver.example.com/core/auth/openid/login/` | OIDC 登录入口地址 |
| 登录成功回传 URL | `https://jumpserver.example.com/core/auth/openid/callback/` | OIDC 登录成功后的回调地址 |
| 注销 URL | `https://jumpserver.example.com/core/auth/openid/logout/` | OIDC 注销地址 |
