
## 1 关于 Passkey

!!! tip ""
    - 进入 **系统设置** 页面，点击 **认证设置 > Passkey**，进入 Passkey 配置页面。
    - **Passkey** 是一种基于公钥加密的无密码身份认证技术，符合 FIDO2 标准（包括 WebAuthn 和 CTAP），支持通过生物识别（如指纹、面部）、PIN 或安全密钥进行身份验证，提升安全性和用户体验。
    - 部分认证器需要 JumpServer 启用 HTTPS 访问，否则认证流程可能无法正常进行。

## 2 配置参数

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| Passkey | 启用 Passkey 无密码认证 | 启用/禁用 |
| 服务域名 | Passkey 服务可用的完整域名，多个域名用逗号分隔 | `jumpserver.example.com` |
| 服务名称 | Passkey 服务名称 | `JumpServer` |

!!! tip ""
    - 服务域名如未设置，默认取请求主机，并匹配 `config.txt` 文件中的 `DOMAINS`。

## 3 操作说明

!!! tip ""
    - 配置完成后，点击 **提交** 保存设置。

