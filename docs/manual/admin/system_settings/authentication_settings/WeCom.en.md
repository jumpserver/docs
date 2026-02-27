# WeCom Authentication

## 1 About WeCom Authentication

!!! info "Note: WeCom authentication is an enterprise feature of JumpServer."

!!! tip ""
    - Click the gear icon in the top-right corner to enter the **System Settings** page, then click **Authentication Settings > WeCom** to open the WeCom configuration page.
    - **WeCom Authentication** is an identity authentication method based on WeCom, and JumpServer supports QR code login and enterprise identity binding.

## 2 Basic Configuration

!!! tip ""
    Detailed parameter descriptions:

| Parameter | Description | Example |
| --- | --- | --- |
| WeCom | Check to enable WeCom authentication | Enable/Disable |
| Corporation ID | WeCom company ID. Uniquely identifies the enterprise in WeCom; all API requests must include this ID | |
| App agent ID | WeCom application agent ID. Used to identify specific applications in WeCom; each application has a unique agent ID | |
| App secret | WeCom application secret. Used to authenticate the application and obtain access tokens for calling WeCom API | |
| Mapped Attributes | User attribute mapping; key represents JumpServer user attribute name, value corresponds to WeCom user attribute name | See example below |
| Organization | After authentication and creation, user will be added to the selected organization | Default: `DEFAULT` |

!!! tip ""
    - The **Mapped Attributes** field is used to set user attribute mapping. The key represents JumpServer user attribute name, and the value corresponds to WeCom user attribute name.
    - WeCom user attribute example:

```json
{
  "name": "alias",
  "username": "userid",
  "email": "extattr.attrs[2].value"
}
```

## JumpServer WeCom URL Description

| URL Type | Address | Description |
| --- | --- | --- |
| QR Code Login URL | `https://jumpserver.example.com/core/auth/wecom/qr/login/` | WeCom QR code login entry point |
| QR Code Login Callback URL | `https://jumpserver.example.com/core/auth/wecom/qr/login/callback/` | QR code login success callback address |
| OAuth Login URL | `https://jumpserver.example.com/core/auth/wecom/oauth/login/` | WeCom OAuth login entry point |
| OAuth Login Callback URL | `https://jumpserver.example.com/core/auth/wecom/oauth/login/callback/` | OAuth login success callback address |
