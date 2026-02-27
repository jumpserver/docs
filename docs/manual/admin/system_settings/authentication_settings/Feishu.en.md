# Feishu Authentication

## 1 About Feishu

!!! info "Note: Feishu authentication is an enterprise version feature of JumpServer."
!!! tip ""
    - Click the settings icon in the top right corner of the page to enter the **System Settings** page, then click **Authentication Settings > Feishu** to access the Feishu configuration page.
    - **Feishu Authentication** is an identity authentication method based on the Feishu platform. JumpServer supports QR code login and enterprise identity binding.

## 2 Basic Configuration

!!! tip ""
    Detailed parameter description:

| Parameter | Description | Example |
|-----------|-------------|---------|
| Feishu | Check to enable Feishu identity verification | Enable/Disable |
| App ID | Feishu App ID, which is the unique identifier of the application |  |
| App secret | Feishu application secret key, similar to a password for API access, used to obtain access tokens for calling Feishu APIs |   |
| Attribute Mapping | User attribute mapping. The key represents the JumpServer user attribute name, and the value corresponds to the Feishu user attribute name | See examples below |
| Organization | After authentication and creation, users will be added to the selected organization | Default value: `DEFAULT` |

Feishu User Attribute Example
!!! tip "Attribute Mapping Example"

```json
{
  "name": "nickname",
  "username": "user_id",
  "email": "email"
}
```

## 3 JumpServer Feishu URL Description

| URL Type | Address | Description |
|----------|---------|-------------|
| QR Code Login URL | `https://jumpserver.example.com/core/auth/feishu/qr/login/` | Feishu QR code login entry |
| QR Code Login Callback URL | `https://jumpserver.example.com/core/auth/feishu/qr/login/callback/` | QR code login success callback address |
