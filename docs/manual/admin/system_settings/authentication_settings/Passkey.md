## 关于Passkey
!!! tip ""
    - **Passkey** 是一种基于公钥加密的无密码身份验证技术。它取代了传统密码以增强安全性和用户体验。FIDO2 标准（包括 WebAuthn 和 CTAP）支持 Passkey，允许用户使用生物识别技术（指纹或面部识别）、PIN 或安全密钥进行身份验证，而无需输入密码。

    - **Fast Identity Online（FIDO）** 是一种开放标准，旨在提供更安全、无密码的身份验证方法。它由 FIDO 联盟开发，主要包括 FIDO UAF（通用身份验证框架）和 FIDO2（由 WebAuthn 和 CTAP 协议组成）。

## 如何配置
!!! tip ""
    - 在页面右上角，单击设置


    - 导航到 **系统设置>认证设置>Passkey** 。

    - 在 **Passkey** 字段中，选中以启用 Passkey 认证。

    - 在 **Passkey 服务域名** 字段中，输入 JumpServer 的完整域名，例如 "jumpserver.example.com"。如果有多个域，请用逗号分隔它们。

!!! tip "提示"

    - 如果未设置，则默认为请求主机，并匹配 "config.txt" 文件中的域。`DOMAINS`

    - 在 **Passkey 服务名称** 字段中，输入服务名称。

    - 默认值为 "JumpServer" 。

    - 单击 **提交。**

