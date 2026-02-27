# Passkey Authentication

## 1 About Passkey

!!! tip ""
    - Click the gear icon in the top-right corner to enter the **System Settings** page, then click **Authentication Settings > Passkey** to open the Passkey configuration page.
    - **Passkey** is a passwordless identity authentication technology based on public key encryption that complies with FIDO2 standards (including WebAuthn and CTAP). It supports identity verification through biometrics (such as fingerprint, face), PIN, or security keys, improving security and user experience.
    - Some authenticators require JumpServer to enable HTTPS access, otherwise the authentication process may not proceed normally.

## 2 Configuration Parameters

!!! tip ""
    Detailed parameter descriptions:

| Parameter | Description | Example |
| --- | --- | --- |
| Passkey | Enable Passkey passwordless authentication | Enable/Disable |
| Service Domain | Complete domain name where Passkey service is available; multiple domains separated by commas | `jumpserver.example.com` |
| Service Name | Passkey service name | `JumpServer` |

!!! tip ""
    - If service domain is not set, it defaults to the request host and matches `DOMAINS` in the `config.txt` file.

## 3 Operation Instructions

!!! tip ""
    - After configuration is complete, click **Submit** to save settings.
