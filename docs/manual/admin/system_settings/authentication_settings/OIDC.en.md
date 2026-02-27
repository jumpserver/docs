# OIDC Authentication

## 1 About OIDC

!!! info "Note: OIDC authentication is an enterprise feature of JumpServer."

!!! tip ""
    - Click the gear icon in the top-right corner to enter the **System Settings** page, then click **Authentication Settings > OIDC** to open the OIDC configuration page.
    - **OpenID Connect (OIDC)** is an identity authentication protocol based on OAuth 2.0. JumpServer authentication supports standard OIDC authentication.

## 2 Basic Configuration

!!! tip ""
    Detailed parameter descriptions:

| Parameter | Description | Example |
| --- | --- | --- |
| OIDC | Check to enable OIDC authentication | Enable/Disable |
| JumpServer Address | Complete domain name of JumpServer, used to construct callback URL | `https://jumpserver.example.com/` |
| Client ID | Client ID provided by OIDC server | |
| Client Secret | Client Secret provided by OIDC server | |
| Client Authentication Method | Authentication method: Client Secret Basic (use POST method to obtain token with Client ID and Client Secret in request header); Client Secret Post (use POST method to obtain token with Client ID and Client Secret in request body) | |
| Use Keycloak | Select to use Keycloak configuration, or uncheck to use native OIDC configuration | |

### 2.1 Using Keycloak

!!! tip ""
    Detailed parameter descriptions:

| Parameter | Description | Example |
| --- | --- | --- |
| Server Address | Keycloak server URI | `https://keycloak.example.com` |
| Domain | Keycloak domain name | `JumpServer` |

### 2.2 Using Native OIDC

!!! tip ""
    Detailed parameter descriptions:

| Parameter | Description | Example |
| --- | --- | --- |
| Endpoint Address | OIDC server base Endpoint for discovering various endpoints | `https://oidc.example.com` |
| Authorization Endpoint Address | OIDC Authorization Endpoint | `https://oidc.example.com/realms/JumpServer/protocol/openid-connect/auth/` |
| Token Endpoint Address | OIDC Token Endpoint | `https://oidc.example.com/realms/JumpServer/protocol/openid-connect/token/` |
