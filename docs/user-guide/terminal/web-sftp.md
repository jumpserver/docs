# 文件管理

!!! info "通过 web 连接管理文件"
    在左侧选择资产后, 可以进入管理员预设的资产目录 ( 默认 /tmp ), 可跨资产复制粘贴文件, 目前仅支持 ssh 协议且 系统用户 要求登陆方式为 自动登陆  
    还可使用命令行登录, 支持 xftp filezilla 等工具
    ```
    sftp -p 2222 用户名@JumpServer IP地址
    ```

![文件管理](../../img/user_terminal_web-sftp_list.jpg)

!!! warning "Windows 文件管理"
    Windows 文件上传可以直接把文件拖拽到 Windows 窗口, 上传后文件在 计算机 - G盘, 下载把文件放到 G 盘的 download  目录即可弹出下载窗口, 快捷键为上传下载工具栏 Ctrl + alt + shift  
