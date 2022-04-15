# Web GUI 上传下载

!!! info "选择 Web GUI 方式，连接到资产"
![登陆资产](../../../../img/user_terminal_web-terminal_webgui_login.jpg)

!!! info "以上图方式登录资产后，在我的电脑界面会看到共享盘 Guacamole"
![gua盘](../../../../img/user_terminal_web-terminal_webgui_gua_filemanagement.jpg)

!!! info "打开文件管理，点击上传文件，上传完成后可在共享盘中看到这个文件，从共享盘中拖拽到服务器，完成上传"
![文件上传](../../../../img/user_terminal_web-terminal_webgui_gua_filemanagement_upload.jpg)
![文件上传2gua](../../../../img/user_terminal_web-terminal_webgui_gua_filemanagement_upload2gua.jpg)
![文件上传gua2server](../../../../img/user_terminal_web-terminal_webgui_gua_filemanagement_upload_gua2server.jpg)

!!! info "打开 Download 文件夹，可以将资产上的文件拖入 Download 文件夹，浏览器会自动拉起下载，下载到本地"
![文件下载](../../../../img/user_terminal_web-terminal_webgui_gua_filemanagement_dowanload.jpg)

??? warning "如果 Guacamole 盘不存在可以参考以下内容进行配置。"
    !!! info "点击 `此电脑` 右键，选择 `映射网络驱动器`"
    ![映射网络驱动器](../../../../img/user_terminal_web-terminal_webgui_gua_netdrive.jpg)

    !!! info "点击 `浏览`，选择 JumpServer"
    ![选择 Guacamole Filessystem](../../../../img/user_terminal_web-terminal_webgui_gua_netdrive_choose.jpg)

    !!! info "若发现目录中没有 Guacamole Filessystem ，请参考 [设置开启网络发现功能](https://jingyan.baidu.com/article/4853e1e5a1e3b41908f7266b.html)，并重新登入
