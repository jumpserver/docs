# OpenID 认证

### 1. 版本 小于等于 1.5.8

!!! info "使用 OpenID 来进行认证设置"
    修改 JumpServer 配置文件启用 OpenID 认证
    ```sh
    vi /opt/jumpserver/config.yml
    ```
    ```yaml
    BASE_SITE_URL: http://localhost:8080
    AUTH_OPENID: True
    AUTH_OPENID_SERVER_URL: https://openid-auth-server.com/
    AUTH_OPENID_REALM_NAME: realm-name
    AUTH_OPENID_CLIENT_ID: client-id
    AUTH_OPENID_CLIENT_SECRET: client-secret
    AUTH_OPENID_IGNORE_SSL_VERIFICATION: True
    AUTH_OPENID_SHARE_SESSION: True
    ```

    !!! question "设置参数说明"
        `BASE_SITE_URL`: JumpServer服务的地址（注意末尾不加  "/"）
        `AUTH_OPENID`: 是否启用 OpenID 认证
        `AUTH_OPENID_SERVER_URL`: OpenID Server 服务的地址（注意末尾要加 "/"）
        `AUTH_OPENID_REALM_NAME`: realm 名称（client 所在的的 realm
        `AUTH_OPENID_CLIENT_ID`: Client ID
        `AUTH_OPENID_CLIENT_SECRET`: Client Secret
        `AUTH_OPENID_IGNORE_SSL_VERIFICATION`: 是否忽略 SSL 验证（在向 OpenID Server 发送请求获取数据时）
        `AUTH_OPENID_SHARE_SESSION`: 是否共享 session（控制用户是否可以单点退出）

### 2. 版本大于等于 1.5.9

!!! info "使用 OpenID 来进行认证设置"
    修改 JumpServer 配置文件启用 OpenID 认证
    ```sh
    vi /opt/jumpserver/config.yml
    ```
    ```yaml
    AUTH_OPENID: False
    AUTH_OPENID_CLIENT_ID: client-id
    AUTH_OPENID_CLIENT_SECRET: client-secret
    AUTH_OPENID_PROVIDER_ENDPOINT: https://op-example.com/
    AUTH_OPENID_PROVIDER_AUTHORIZATION_ENDPOINT: https://op-example.com/authorize
    AUTH_OPENID_PROVIDER_TOKEN_ENDPOINT: https://op-example.com/token
    AUTH_OPENID_PROVIDER_JWKS_ENDPOINT: https://op-example.com/jwks
    AUTH_OPENID_PROVIDER_USERINFO_ENDPOINT: https://op-example.com/userinfo
    AUTH_OPENID_PROVIDER_END_SESSION_ENDPOINT: https://op-example.com/logout
    AUTH_OPENID_PROVIDER_SIGNATURE_ALG: HS256
    AUTH_OPENID_PROVIDER_SIGNATURE_KEY: None
    AUTH_OPENID_SCOPES: openid profile email
    AUTH_OPENID_ID_TOKEN_MAX_AGE: 60
    AUTH_OPENID_ID_TOKEN_INCLUDE_CLAIM: True
    AUTH_OPENID_USE_STATE: True
    AUTH_OPENID_USE_NONCE: True
    AUTH_OPENID_SHARE_SESSION: True
    AUTH_OPENID_IGNORE_SSL_VERIFICATION: True
    AUTH_OPENID_ALWAYS_UPDATE_USER: True
    ```

    ??? question "设置参数说明"
        `AUTH_OPENID`: Whether to enable OpenID authentication  
        `AUTH_OPENID_CLIENT_ID`: This setting defines the Client ID that should be provided by the considered OIDC provider.  
        `AUTH_OPENID_CLIENT_SECRET`: This setting defines the Client Secret that should be provided by the considered OIDC provider.  
        `AUTH_OPENID_PROVIDER_ENDPOINT`: This setting defines the top-level endpoint under which all OIDC-specific endpoints are available (such as the authotization, token and userinfo endpoints).  
        `AUTH_OPENID_PROVIDER_AUTHORIZATION_ENDPOINT`: This setting defines the authorization endpoint URL of the OIDC provider.  
        `AUTH_OPENID_PROVIDER_TOKEN_ENDPOINT`: This setting defines the token endpoint URL of the OIDC provider.  
        `AUTH_OPENID_PROVIDER_JWKS_ENDPOINT`: This setting defines the JWKs endpoint URL of the OIDC provider.  
        `AUTH_OPENID_PROVIDER_USERINFO_ENDPOINT`: This setting defines the userinfo endpoint URL of the OIDC provider.  
        `AUTH_OPENID_PROVIDER_END_SESSION_ENDPOINT`: This setting defines the end session endpoint URL of the OIDC provider.  
        `AUTH_OPENID_PROVIDER_SIGNATURE_ALG`: This setting defines the signature algorithm used by the OpenID Connect Provider to sign ID tokens. The value of this setting should be  HS256 or RS256.  
        `AUTH_OPENID_PROVIDER_SIGNATURE_KEY`: This setting defines the value of the key used by the OP to the sign ID tokens. It should be used only when the AUTH_OPENID_PROVIDER_SIGNATURE_ALG setting is set to RS256.  
        `AUTH_OPENID_SCOPES`: This setting defines the OpenID Connect scopes to request during authentication.  
        `AUTH_OPENID_ID_TOKEN_MAX_AGE`: This setting defines the amount of time (in seconds) an id_token should be considered valid.  
        `AUTH_OPENID_ID_TOKEN_INCLUDE_CLAIM`: This settings defines whether the id_token content can be used to retrieve userinfo claims and scopes in order to create and update the user being authenticated.  
        `AUTH_OPENID_USE_STATE`: This setting defines whether or not states should be used when forging authorization requests. States are used to maintain state between the authentication request and the callback.  
        `AUTH_OPENID_USE_NONCE`: This setting defines whether or not nonces should be used when forging authorization requests. Nonces are used to mitigate replay attacks.  
        `AUTH_OPENID_SHARE_SESSION`: Whether or not to share session (controls whether or not the user can exit with a single point)  
        `AUTH_OPENID_IGNORE_SSL_VERIFICATION`: Whether to ignore SSL validation (when sending a request to OpenID Server for data)  
        `AUTH_OPENID_ALWAYS_UPDATE_USER`: Whether the user information is always updated (when the user logs in and authenticates successfully every time)  

    !!! tip "例:"
        ```yaml
        AUTH_OPENID: True
        AUTH_OPENID_CLIENT_ID: jumpserver
        AUTH_OPENID_CLIENT_SECRET: 5222e5ed-0234-45f5-b3e7-3133f0d15f99
        AUTH_OPENID_PROVIDER_ENDPOINT: https://op-example.com/
        AUTH_OPENID_PROVIDER_AUTHORIZATION_ENDPOINT: /authorize
        AUTH_OPENID_PROVIDER_TOKEN_ENDPOINT: /token
        AUTH_OPENID_PROVIDER_JWKS_ENDPOINT: /jwks
        AUTH_OPENID_PROVIDER_USERINFO_ENDPOINT: /userinfo
        AUTH_OPENID_PROVIDER_END_SESSION_ENDPOINT: /logout
        AUTH_OPENID_PROVIDER_SIGNATURE_ALG: HS256
        AUTH_OPENID_PROVIDER_SIGNATURE_KEY: None
        AUTH_OPENID_SCOPES: openid profile email
        AUTH_OPENID_ID_TOKEN_MAX_AGE: 60
        AUTH_OPENID_ID_TOKEN_INCLUDE_CLAIM: True
        AUTH_OPENID_USE_STATE: True
        AUTH_OPENID_USE_NONCE: True
        AUTH_OPENID_SHARE_SESSION: True
        AUTH_OPENID_IGNORE_SSL_VERIFICATION: True
        AUTH_OPENID_ALWAYS_UPDATE_USER: True
        ```
