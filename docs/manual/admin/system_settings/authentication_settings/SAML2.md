## 关于 SAML2
!!! tip ""
    - **Security Assertion Markup Language 2.0（SAML2）** 是一种开放标准，用于在各方之间交换身份验证和授权数据，尤其是在身份提供者和服务提供商之间。它允许用户使用 IdP 进行一次身份验证并访问多个服务 （SP），而无需重新输入凭据。
    - Identity Provider （IdP） 是一种对用户进行身份验证并将其身份信息提供给服务提供商的系统。

    - Service Provider  （SP） 是一种系统或应用程序，它依赖于 IdP 来验证用户并根据用户身份授予对其服务的访问权限。在这种情况下，JumpServer 仅充当 SP。
## 如何配置
!!! tip ""

    - 在页面右上角，单击 。


    - 导航到 **系统设置>认证设置> SAML2**。

    - 在 **SAML2** 字段中，选中以启用 SAML2 身份验证。

    - 在 **SP 密钥** 字段中，上传 SP 私钥文件。它用于对 SAML 请求进行签名、解密来自 IdP 的加密 SAML 响应并确保数据完整性。

    - 在 **SP 证书** 字段中，上传 SP 证书文件。它由 SP 私钥生成并提供给 IdP 以验证来自 SP 的签名请求。- 此外，它还对 SAML 响应数据进行加密以确保安全传输。

!!! warnning "注意"

    - SP 私钥和 SP 证书协同工作，以确保 SAML2 身份验证中的安全通信和数据保护。简单来说，SP私钥负责签名和解密，而SP证书负责验证和加密。


!!! tip ""

    - 在 **IDP metdata 地址** 字段中，输入IDP metadaa 地址URL，例如“https://saml2.example.com/realms/JumpServer/protocol/saml/descriptor”。

    - 在 **IDP metadata XML** 字段中，您可以手动输入 IdP 元数据 XML。实际上，您只需提供 **IDP metdata 地址** 或 **IDP metadata XML** 。如果两者都存在，则 **IDP 元数据 URL** 优先。
 
    - 在 **高级设置** 字段中，输入要配置的信息。我们将根据此配置生成 SP 元数据以供 IdP 使用。有关更多信息，请参阅[SP 高级设置](https://github.com/SAML-Toolkits/python3-saml/tree/master?tab=readme-ov-file#settings).

SAML2 SP 高级设置示例

```
{  
	"organization": {    
		"en": {      
			"name": "JumpServer",      
			"displayname": "JumpServer",      
			"url": "https://jumpserver.com/"    
		}  
	},
    "strict": true,  
    "security": {}
}
```

!!! warnning ""

    - **SP Metadata** 用于提供有关服务提供商的基本配置信息，包括实体 ID、端点 URL、公共证书和支持的绑定，以促进在 SAML 身份验证中与身份提供商的安全通信。

    - 您可以在 **SP 证书** 字段下方的帮助信息中单击 **查看** 以查看SP Metadata。

![img](../../../../img/V4_SAML2.png)





在 **映射属性** 字段中，输入用户属性映射。键表示 SAML2 用户属性名称，而值对应于 JumpServer 用户属性名称（可用选项：名称、用户名、电子邮件、组、电话、评论）。

SAML2 用户属性示例

``` json
{  
	"uid": "username",  
	"email": "email",  
	"member": "groups"
}
```

在 **组织** 字段中，在身份验证和创建后，用户将被添加到所选组织中。

在 **总是更新用户信息** 字段中，勾选后，SAML2 用户认证后，每次都会更新用户信息（仅包括：姓名、用户名、电子邮件、电话、评论），"群组"仅在创建用户时同步。

在 **同步注销** 字段中，选中后，注销也会将用户从 SAML2 服务注销。

单击 **提交。**

## JumpServer SAML2 网址

登录网址

```
https://jumpserver.example.com/core/auth/saml2/login/
```



登录成功回传 URL

```
https://jumpserver.example.com/core/auth/saml2/callback/
```



注销 URL

```
https://jumpserver.example.com/core/auth/saml2/logout/
```



SP 元数据 URL
```
https://jumpserver.example.com/core/auth/saml2/metadata/
```