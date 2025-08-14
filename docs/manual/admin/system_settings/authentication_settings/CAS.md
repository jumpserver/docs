## 关于CAS
!!! tip ""
	- **Central Authentication Service （CAS）** 是一种单点登录 （SSO） 协议，旨在为多个应用程序提供集中式身份验证。CAS 由耶鲁大学开发，允许用户通过一次登录访问多个受保护的服务，无需重新输入凭据。它通过“ticket”机制实现身份验证，并支持各种身份提供者，例如数据库、LDAP 和 OAuth。

## 如何配置
!!! tip ""
	- 在页面右上角，单击设置图标


	- 导航到 **系统设置>认证设置> CAS**。

	- 在 **CAS** 字段中，选中以启用 CAS 身份验证。

	- 在 **服务端地址**字段中，输入 CAS 服务器 URI，例如“https://example.com/cas”。

	- 在 **回调地址** 字段中，输入 CAS 代理服务器 URI（如果位于代理后面）。例如，如果主机侦听“http://foo.bar:8080”，但请求使用“https://foo.bar:8443”，请输入“https://foo.bar:8443”，有关详细信息，请参阅[Django CAS 配置](https://djangocas.dev/docs/latest/configuration.html#cas-root-proxied-as-optional).

	- 在 **版本** 字段中，输入 CAS 协议版本：1、2、3 或 CAS_2_SAML_1_0。

	- 默认值为“3”。

	- 在 **映射属性** 字段中，输入用户属性映射。键表示 CAS 用户属性名称，而值对应于 JumpServer 用户属性名称（可用选项：名称、用户名、电子邮件、组、电话、评论）。

	- CAS 用户属性示例

	``` json
	{  
		"cas:user": "username",  
		"cas:fullname": "name",  
		"cas:mail": "email",
	}
	```



	- 在 **组织** 字段中，在身份验证和创建后，用户将被添加到所选组织中。

	- 在 **创建用户** 字段中，选中后，将在成功身份验证后创建用户。

	!!! warning "警告"
		- 如果未选中且用户不存在，则身份验证将失败。


	- 在 **同步注销** 字段中，选中注销后，注销也会使用户从 CAS 服务注销。

	- 单击 **提交。**



## JumpServer CAS URL

登录网址

```
https://jumpserver.example.com/core/auth/cas/login/
```



登录成功回传 URL

```
https://jumpserver.example.com/core/auth/cas/callback/
```



注销 URL

```
https://jumpserver.example.com/core/auth/cas/logout/
```

