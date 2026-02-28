# Lark Authentication

## About Lark
!!! info "Note: Lark authentication is an enterprise version feature of JumpServer."
!!! tip ""
    - Click the settings icon in the top right corner of the page to enter the **System Settings** page, then click **Authentication Settings > Lark** to access the Lark configuration page.
    - **Lark** Authentication is an identity authentication mechanism provided by Lark (international version of Feishu) that enables enterprises and third-party applications to authenticate and authorize users through Lark.

## Basic Configuration

!!! tip ""
    - Click the settings icon in the top right corner of the page
    - Navigate to **System Settings > Authentication Settings > Lark**

!!! tip ""
    Detailed parameter description:

| Parameter | Description | Example |
|-----------|-------------|---------|
| Lark | Check to enable Lark identity verification | Enable/Disable |
| App ID | Lark App ID, which is the unique identifier of the application |  |
| App secret | Lark application secret key, used to obtain access tokens for calling Lark APIs |   |
| Attribute Mapping | User attribute mapping. The key represents the JumpServer user attribute name, and the value corresponds to the Lark user attribute name | See examples below |
| Organization | After authentication and creation, users will be added to the selected organization | Default value: `DEFAULT` |

Lark User Attribute Example
!!! tip ""
    - The **Attribute Mapping** field is used to set user attribute mapping. The key represents the JumpServer user attribute name, and the value corresponds to the Lark user attribute name.

```json
{
  "name": "nickname",
  "username": "user_id",
  "email": "email"
}
```

## JumpServer Lark URL Description

| URL Type | Address | Description |
|----------|---------|-------------|
| QR Code Login URL | `https://jumpserver.example.com/core/auth/lark/qr/login/` | Lark QR code login entry |
| QR Code Login Callback URL | `https://jumpserver.example.com/core/auth/lark/qr/login/callback/` | QR code login success callback address |
