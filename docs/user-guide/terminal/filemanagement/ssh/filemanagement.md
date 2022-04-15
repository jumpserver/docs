# 文件管理

## Web 页面

!!! info "连接到 ssh 协议资产"
    在左侧 `资产树` 中选择已连接的资产，鼠标 `右击`，选择 `文件管理`，进入文件管理页面
![登入文件管理](../../../../img/user_terminal_web-terminal_filemanagement_login-filemanagement.jpg)

!!! info "访问有权限的目录"
    默认的目录为 /tmp 目录，如需要指定其他目录请自行联系管理员在 `系统用户` 修改
![访问资产/tmp目录](../../../../img/user_terminal_web-terminal_filemanagement_access-tmpdir.jpg)

!!! info "文件下载"
    选择需要操作的文件 `右键` 点击，即可完成文件 `下载` 等操作
![文件下载](../../../../img/user_terminal_web-terminal_filemanagement_filedownload.jpg)

!!! info "文件上传"
    在页面空白处点击鼠标 `右键` ，选择 `上传文件`，或将文件拖入页面，完成文件上传功能
![文件上传](../../../../img/user_terminal_web-terminal_filemanagement_fileupload.jpg)

## SFTP 客户端

!!! info "除了内置的 Web 方式文件管理外，还支持原生 sftp 方式连接 `sftp -P 2222 用户名@堡垒机 IP` 进行连接。"

!!! warning "如果是手动登陆的资产，请先登陆资产后，再打开文件管理即可跳过密码验证"
