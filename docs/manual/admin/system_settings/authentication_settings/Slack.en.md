# Slack Authentication

## 1 About Slack

!!! info "Note: Slack authentication is an enterprise feature of JumpServer."

!!! tip ""
    - Click the gear icon in the top-right corner to enter the **System Settings** page, then click **Authentication Settings > Slack** to open the Slack configuration page.
    - **Slack** authentication is an identity authentication mechanism based on the Slack platform, allowing users to securely login to enterprise applications using Slack accounts. JumpServer supports standard Slack authentication.

## 2 Configuration Parameters

!!! tip ""
    Detailed parameter descriptions:

| Parameter | Description | Example |
| --- | --- | --- |
| Slack | Check to enable Slack authentication | Enable/Disable |
| Client ID | Slack Client ID, which is the unique identifier of the Slack application used to identify the application during OAuth 2.0 authorization | |
| Client secret | Slack Client secret, which is a secret string associated with the Slack application used to authenticate the application during OAuth 2.0 token exchange | |
| Client bot token | Slack Client bot token, which is an access token granted to the Slack bot, allowing it to interact with the Slack workspace and perform tasks such as sending messages or managing channels | |
| Mapped Attributes | User attribute mapping; key represents JumpServer user attribute name, value corresponds to Slack user attribute name | See example below |
| Organization | After authentication and creation, user will be added to the selected organization | Default: `DEFAULT` |

Slack User Attribute Example

!!! tip ""
    - The **Mapped Attributes** field is used to set user attribute mapping. The key represents JumpServer user attribute name, and the value corresponds to Slack user attribute name.

```json
{
  "name": "real_name",
  "username": "name",
  "email": "profile.email"
}
```

## JumpServer Slack URL Description

| URL Type | Address | Description |
| --- | --- | --- |
| QR Code Login URL | `https://jumpserver.example.com/core/auth/slack/qr/login/` | Slack QR code login entry point |
| QR Code Login Callback URL | `https://jumpserver.example.com/core/auth/slack/qr/login/callback/` | QR code login success callback address |
