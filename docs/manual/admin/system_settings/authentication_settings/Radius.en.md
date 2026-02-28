# RADIUS Authentication

## 1 About RADIUS

!!! info "Note: RADIUS authentication is an enterprise feature of JumpServer."

!!! tip ""
    - Click the gear icon in the top-right corner to enter the **System Settings** page, then click **Authentication Settings > Radius** to open the RADIUS configuration page.
    - **RADIUS (Remote Authentication Dial In User Service)** is a network access control authentication mechanism based on the RADIUS protocol, providing authentication, authorization, and accounting (AAA) functions. JumpServer supports standard RADIUS authentication.

## 2 Configuration Parameters

!!! tip ""
    - Click the settings button in the top-right corner
    - Navigate to **System Settings > Authentication Settings > Radius**

!!! tip ""
    Detailed parameter descriptions:

| Parameter | Description | Example |
| --- | --- | --- |
| Radius | Check to enable RADIUS authentication | Enable/Disable |
| Host | RADIUS server IP address or domain name | `172.16.10.180` |
| Port | RADIUS server port number | Default: 1812 |
| Secret | Shared key between JumpServer and RADIUS server. It functions like a password, encrypting sensitive information in RADIUS requests and responses to ensure secure communication | |
| Use radius OTP | Check to enable RADIUS as MFA backend. For more information, see Enable RADIUS MFA Backend below | Enable/Disable |
| Organization | After authentication and creation, user will be added to the selected organization | Default: `DEFAULT` |

Enable RADIUS MFA Backend

!!! tip ""
    - Configure RADIUS authentication following the RADIUS authentication integration guide.
    - In the **Use radius OTP** field, check to enable RADIUS as MFA backend. When user's MFA is enabled, they can select RADIUS authentication type during login.
    - Click **Submit**.
