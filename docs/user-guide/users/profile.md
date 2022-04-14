# 个人信息

!!! info "登录堡垒机后，来到个人信息页面，用户可对本人账号信息进行相应的认证配置和消息订阅配置："
    - 设置企业微信认证：需管理员配置并开启该功能，其他如钉钉等外部身份认证与此类似；
    - 设置多因子认证：普通用户可自行选择是否开启，以增加账号安全性；
    ![个人信息](../../img/user_login_account-info.jpg)
!!! info "更新密码："
	- 用户可以自行更新当前账号密码；
	![更新密码](../../img/user_login_password-update.jpg)
!!! info "更新SSH公钥："
	- 用户可以自行设定SSH公钥，在使用SSH终端登录时使用；
	- 重置并下载SSH公钥：重新生成默认的SSH密钥，下载后，在SSH终端链接时使用；
	![更新SSH公钥](../../img/user_login_ssh-pub-key.jpg)
!!! tip "消息订阅（站内信外的通知方式需开启配置）"
	- 默认支持站内信通知，当开启邮件和企业微信等其他设置时，可以选择将消息通过相应方式通知到用户；
!!! info "个人信息设置的文件密码设置："
	- 该密码，当开启账号管理功能[企业版功能](https://www.jumpserver.org/enterprise.html){:target="_blank"}  ，导出用户时，可以对导出的文件进行加密；
	![文件加密](../../img/user_login_file-encryption-password.jpg)