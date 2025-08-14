## 关于OIDC
!!! tip ""

    - **OpenID Connect（OIDC）** 是一种基于 "OAuth 2.0" 的身份认证协议。它允许应用程序通过 "授权服务器 "验证用户身份并获取基本用户信息，例如 "用户名" 和 "电子邮件" 。它在OAuth 2.0之上增加了一个身份层，使用 "ID Token" 来传输用户身份信息，并广泛用于单点登录（SSO）和身份认证系统。

    - **Relying Party （RP）** 是使用认证服务并依赖于 OpenID 提供程序来认证用户和提供身份信息的应用程序或客户机。

    - **OpenID Provider （OP）** 是负责验证用户身份并向 RP 提供身份信息的服务器。

## 如何配置
!!! tip ""

    - 在页面右上角，单击系统设置


    - 导航到 **系统设置>认证设置> OIDC** 。

    - 在 **OIDC** 字段中，选中以启用 OIDC 身份验证。

    - 在 **jumpserver 地址** 字段中，输入 JumpServer 的完整域名，例如“https://jumsperver.example.com/”，用于构造回调 URL。

    - 在 **客户端 ID** 字段中，输入 OIDC 服务器提供的客户端 ID。

    - 在 **客户端密钥** 字段中，输入 OIDC 服务器提供的客户端密钥。

    - 在 **客户端认证方式** 字段中，选择认证的方式。

    - Client Secret Basic：使用 POST 方法获取令牌，请求标头中包含客户端 ID 和客户端密码。

    - Client Secret Post：使用 POST 方法获取令牌，其中客户端 ID 和客户端密码作为原始数据包含在请求正文中。


在 **使用 keycloak** 字段中，选中以使用 Keycloak 配置，或取消选中以使用本机 OIDC 配置。

=== "使用 Keycloak"
    !!! tip ""

        -  在 **服务端地址** 字段中，输入 Keycloak 服务器 URI，例如 "https://keycloak.example.com"。

        -  在 **域**  字段中，输入 Keycloak 域名称，例如 "JumpServer"。


=== "使用本机 OIDC"
    !!! tip ""
        - 在 **端点地址** 字段中，输入 OIDC 提供的端点地址，例如“https://oidc.example.com”。

        - 在 **授权端点地址** 字段中，输入 OIDC 授权端点地址，例如“https://oidc.example.com/realms/JumpServer/protocol/openid-connect/auth/”。

        - 在 **Token端点地址** 字段中，输入 OIDC 令牌Token，例如“https://oidc.example.com/realms/JumpServer/protocol/openid-connect/token/”。

        - 在 **Jwks端点地址** 字段中，输入 OIDC JSON Web 密钥集 （JWKS） Token，例如“https://oidc.example.com/realms/JumpServer/protocol/openid-connect/certs/。

        - 在 **用户信息端点** 字段中，输入 OIDC 用户信息端点，例如“https://oidc.example.com/realms/JumpServer/protocol/openid-connect/userinfo/”。
        - 在 **注销会话端点地址** 字段中，输入 OIDC 注销会话端点地址，当用户注销时，将调用此地址，例如“https://oidc.example.com/realms/JumpServer/protocol/openid-connect/logout/”。

        - 在 **签名算法** 字段中，输入 OIDC 签名算法，有效选项为 "HS256"和 "RS256"。默认值为 "HS256"。

            - HS256：使用“客户端 ID”作为共享密钥。
            - RS256：使用“签名密钥”作为共享密钥。
            - 注意, 在 OIDC 身份验证流中验证 ID 令牌时，此函数中的共享密钥用于基于哈希的消息身份验证代码 （HMAC） 签名。

        - 在 **签名key** 字段中，当“签名key”字段值为“RS256”时，签名密钥将用于HMAC签名验证或JSON Web Token（JWK）解密，以确保OIDC认证的安全性。

        - 在 **启用 PKCE 字段** 中，建议使用。代码交换证明密钥 （PKCE） 保护授权码流并防止授权码拦截攻击。

        - 在 **验证校验码方式** 字段中，用于在PKCE进程中从代码验证器生成代码质询的方法。选中 "启用 PKCE" 时，会出现此选项。默认值为“S256”。

            - S256：推荐使用，将 SHA-256 哈希算法应用于代码验证器，然后 Base64 URL 对结果进行编码（删除填充“=”）以生成code challenge。
            - Plain：直接使用代码验证器本身作为code challenge，无需任何处理
        - 在 **连接范围** 字段中，定义客户端在授权请求中请求从 OP 访问的用户信息范围。多条信息用空格分隔，例如 "openid profile email"。

        - 在 **令牌有效时间(秒)** 字段中，ID 令牌的最大期限（以秒为单位）。过期后，将使用刷新令牌自动获取新的。

        - 在 **声明** 字段中，选中后，ID 令牌将包括 userinfo 范围和声明。如果未选中，将从 OP 提供的 userinfo 终结点检索声明。有关更多信息，请参阅标准索赔.

        - 在 **使用状态** 字段中，建议使用，有助于防止跨站点请求伪造 （CSRF） 攻击并确保请求和回调之间的一致性。

        - 在 **临时使用** 字段中，建议使用，有助于防止重放攻击。

!!! tip ""

    - 在 **总是更新用户信息** 字段中，勾选后，OIDC 用户认证后，每次都会更新用户信息（仅包括：姓名、用户名、邮箱、电话、评论），“群组”仅在创建用户时同步。

    - 在 **忽略 SSL 证书验证** 字段中，选中后，在向 OP 发送请求时将忽略 SSL 证书验证。

    - 在 **共享会话** 字段中，选中后，当用户从其他应用程序注销时，会话将同时注销。

    - 在 **映射属性** 字段中，输入用户属性映射。键表示 JumpServer 用户属性名称（可用选项：名称、用户名、电子邮件、组、电话、评论），而该值对应于 OIDC 用户属性名称。

OIDC 用户属性示例

``` json
{  
	"name": "name",  
	"username": "preferred_username",  
	"email": "email",  
	"groups": "groups"
}
```


!!! tip ""
    - 在 **组织** 字段中，在身份验证和创建后，用户将被添加到所选组织中。

    - 单击 **提交。**

## JumpServer OIDC URL

登录网址

```
https://jumpserver.example.com/core/auth/openid/login/
```



登录成功回传 URL

```
https://jumpserver.example.com/core/auth/openid/callback/
```



注销 URL

```
https://jumpserver.example.com/core/auth/openid/logout/
```

# 