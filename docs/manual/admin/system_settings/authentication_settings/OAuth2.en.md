# OAuth2 Authentication

## 1 About OAuth2

!!! info "Note: OAuth2 authentication is an enterprise feature of JumpServer."

!!! tip ""
    - Click the gear icon in the top-right corner to enter the **System Settings** page, then click **Authentication Settings > OAuth2** to open the OAuth2 configuration page.
    - **OAuth2** is an open third-party authorization protocol. JumpServer supports standard OAuth2 platform authentication.

## 2 Configuration Parameters

!!! tip ""
    Detailed parameter descriptions:

| Parameter | Description | Example |
| --- | --- | --- |
| OAuth2 | Enable OAuth2 identity authentication | Enable/Disable |
| Service Provider | OAuth2 service provider name | `GitHub`, `Google`, `Facebook`, etc. |
| Icon | Service provider icon displayed on login page; recommended size: 64x64 pixels | |
| Client ID | Client ID provided by OAuth2 service provider | |
| Client Secret | Client Secret provided by OAuth2 service provider | |
| Client Authentication Method | Authentication method for obtaining token; see explanation below | |
| Scope | Scope range for authorization request, space-separated | `user user:email user:login` |
| Authorization Endpoint Address | OAuth2 Authorization Endpoint | `https://github.com/login/oauth/authorize` |
| Token Endpoint Address | OAuth2 Token Endpoint | `https://github.com/login/oauth/access_token` |
| User Info Endpoint Address | OAuth2 UserInfo Endpoint | `https://api.github.com/user` |
| Logout Endpoint Address | OAuth2 Logout Endpoint, called when user logout | `https://github.com/logout` |
| Mapped Attributes | User attribute mapping; correspondence between JumpServer and OAuth2 fields | See JSON example below |
| Organization | After authentication and creation, user will be added to the selected organization | Default: DEFAULT |
| Always Update User Info | When enabled, synchronize user info on every authentication (only name, username, email, phone, comment; groups only on first sync) | Enable/Disable |
| Sync Logout | When enabled, logout is synchronized with OAuth2 service logout | Enable/Disable |

!!! tip ""
    - Client authentication method explanation:

| Request Method | Description |
| --- | --- |
| Client Secret Basic | Use POST method to obtain token; Client ID and Client Secret included in request header |
| Client Secret Post | Use POST method to obtain token; Client ID and Client Secret included in request body as raw data |

JumpServer OAuth2 URL Description

| URL Type | Address | Description |
| --- | --- | --- |
| OAuth2 Login URL | `https://jumpserver.example.com/core/auth/oauth2/login/` | OAuth2 login entry point |
| OAuth2 Login Callback URL | `https://jumpserver.example.com/core/auth/oauth2/login/callback/` | OAuth2 login success callback address |
| Logout URL | `https://jumpserver.example.com/core/auth/oauth2/logout/` | OAuth2 logout address |
