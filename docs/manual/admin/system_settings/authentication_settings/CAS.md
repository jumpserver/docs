## 1 关于CAS

!!! tip ""
    - 通过点击页面右上角小齿轮进入 **系统设置** 页面，点击 **认证设置 > CAS** ，进入 CAS 配置页面。
	- **Central Authentication Service （CAS）** 是一种单点登录 （SSO） 协议，旨在为多个应用程序提供集中式身份验证。JumpServer 支持标准 CAS 平台认证。

## 2 基础配置

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| CAS | 勾选启用 CAS 身份验证 | 启用/禁用 |
| 服务端地址 | CAS 服务器 URI | `https://example.com/cas` |
| 回调地址 | CAS 代理服务器 URI | `https://foo.bar:8443` |
| 版本 | CAS 协议版本：1、2、3 或 CAS_2_SAML_1_0 | 默认值：3 |
| 映射属性 | 用户属性映射。键表示 CAS 用户属性名称，值对应 JumpServer 用户属性名称 | 示例见下文 |
| 组织 | 身份验证和创建后，用户将被添加到所选组织中 |  |
| 创建用户 | 选中后，将在成功身份验证后创建 JumpServer 不存在的用户 |  |
| 同步注销 | 选中注销后，注销也会使用户从 CAS 服务注销 |  |

!!! tip ""
    CAS 用户属性示例：
    
``` bash
{  
	"cas:user": "username",  
	"cas:fullname": "name",  
	"cas:mail": "email"
}
```


## 3 JumpServer CAS URL 说明

!!! tip ""
    详细 URL 说明：

| URL 类型 | 地址 | 说明 |
|----------|------|------|
| 登录网址 | `https://jumpserver.example.com/core/auth/cas/login/` | CAS 登录入口地址 |
| 登录成功回传 URL | `https://jumpserver.example.com/core/auth/cas/callback/` | CAS 登录成功后的回调地址 |
| 注销 URL | `https://jumpserver.example.com/core/auth/cas/logout/` | CAS 注销地址 |

