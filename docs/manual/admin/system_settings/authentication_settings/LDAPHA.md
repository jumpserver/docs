# LDAP 认证

## 关于 LDAP HA
!!! info "注: LDAP HA 认证方式为 JumpServer 企业版功能。"
!!! tip ""
    - 进入 **系统设置**，点击 **认证设置 > LDAP HA**，进入 LDAP HA 配置页面。
    - **LDAP High Availability(LDAP)** 是一种开放式协议，用于访问和管理分布式目录信息。主要应用于集中式身份验证和目录服务，如存储用户账户、权限及组织结构信息等。LDAP 被广泛应用于企业身份管理、单点登录(SSO)和访问控制系统中。
    - 在JumpServer中，LDAP HA的集成通常可以确保在主LDAP服务器出现故障时，系统可以自动切换到备份LDAP HA服务器，从而保证认证服务的连续性。这样，即使 LDAP 服务器遇到问题，JumpServer 也可以继续处理用户身份验证请求，而不会导致停机或服务中断。

## 基础配置

!!! tip ""
    - 点击页面右上角的设置按钮
    - 导航至 **系统设置 > 认证设置 > LDAP HA**
    - 在 **LDAP HA** 字段中，选中以启用 LDAP HA 身份验证。
    - 在 **服务端地址** 字段中，键入 LDAP HA 服务器 URI，例如"ldap://example.com:389”和“ldaps://example.com:636"。

!!! info ""
    - 若需配置 LDAP TLS 证书，请将 `ldap_ca.pem、ldap_cert.pem、ldap_cert.key` 文件上传至 JumpServer 服务器 `/data/jumpserver/core/data/certs` 目录，然后通过命令 `jmsctl restart` 重启 JumpServer 服务。

!!! tip ""
    - 在 **绑定 DN** 字段中，输入至少具有查询权限的用户 DN，该权限将用于查询和筛选用户，例如“cn=admin，dc=example，dc=com”。

    - 在 **密码** 字段中，输入 "绑定 DN" 用户的密码。

    - 在 **搜索 OU** 字段中，输入搜索 OU 以指定从何处开始搜索用户，用于分隔多个值，例如“ou=users，dc=example，dc=com |ou=tech，dc=example，dc=com“。`|`

    - 在 **搜索过滤器** 字段中，输入过滤器表达式以搜索 LDAP HA 用户。默认情况下，表达式为“（cn=%（user）s）”，其中“%（user）s”是 Python 中的占位符语法。在过滤过程中，它被替换为 ，生成“（cn=*）”，它搜索所有用户。您还可以将“cn”替换为实际的用户名字段，例如“uid”或“sAMAccountName”。`*`

    - 在 **映射属性** 字段中，输入用户属性映射。该键表示 JumpServer 用户属性名称（可用选项：名称、用户名、电子邮件、is_active、组、电话、评论），而该值对应于 LDAP HA 用户属性名称。


```json 
{  
    "name": "sAMAccountName",
	"username": "cn",  
    "email": "mail",  
	"is_active": "useraccountcontrol",  
    "phone": "telephoneNumber",
	"groups": "memberof"
}
```

## 测试 LDAP HA 连接
!!! tip ""
    - 点击页面右上角的设置按钮

    - 导航至 **系统设置 > 认证设置 > LDAP HA**

    - 滚动至页面底部

    - 点击 **测试连接**

## 测试 LDAP 登录
!!! tip ""
    - 点击页面右上角的设置按钮

    - 导航至 **系统设置 > 认证设置 > LDAP HA**

    - 确保已成功完成并测试 LDAP  HA配置

    - 滚动至页面底部

    - 点击 **测试登录**

    - 在弹出窗口中输入 LDAP 用户的用户名和密码
    - 点击 **确认**。

## 导入 LDAP 用户
!!! tip ""
    - 点击页面右上角的设置按钮

    - 导航至 **系统设置 > 认证设置 > LDAP HA**

    - 确保已成功完成并测试 LDAP HA 配置

    - 滚动至页面底部

    - 点击 **用户导入**

    - 在弹出窗口中，可通过以下方式导入 LDAP HA 用户

    - 点击 **同步用户** 将 LDAP HA 用户同步到列表中

    - 在 **导入组织** 字段中选择要导入的一个或多个组织

    - 选中要导入的用户，点击 **导入** 继续；或者点击 **全部导入** 导入所有用户

![LDAP图1](../../../../img/V4_LDAP1.png)

## 设置 LDAP HA 用户同步
!!! tip ""

    - 点击页面右上角的设置按钮

    - 导航至 **系统设置 > 身份验证 > LDAP HA**

    - 确保已成功完成并测试 LDAP HA 配置

    - 滚动至页面底部

    - 点击 **同步设置**

    - 在弹出窗口中输入以下配置信息

    - 在 **组织** 字段中选择要同步的一个或多个组织

    - 在 **周期执行** 字段中勾选启用周期执行

    - 在 **定时任务** 字段中输入 crontab 表达式。如果为空，则使用 **间隔** 设置

    - 在 **间隔** 字段中输入同步间隔时间(单位：小时)

    - 注意：如果 **定时任务** 有值，则 **定时任务** 优先生效

    - 在 **收件人** 字段中选择一个或多个用户以接收同步结果

    - 点击 **确认**

![LDAP图2](../../../../img/V4_LDAP2.png)

