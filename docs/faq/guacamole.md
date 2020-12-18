# Guacamole 常见问题

!!! info "请先确认下面选项"
    请在 `web` - `系统设置` - `安全设置` 里面允许 `终端注册`  
    Docker 容器部署的 `JUMPSERVER_SERVER` 不可以使用 `http://127.0.0.1:8080`

### 1. guacamole 启动异常

!!! question "启动异常"
    - ERROR o.a.g.a.j.r.JumpserverRegisterService 121 - 注册终端失败

    在 web - 会话管理 - 终端管理 里面删除 guacamole 的注册 ( 在线显示红色的[gua]xxx )  

    ```sh
    rm -f /opt/jumpserver/guacamole/data/keys/jumpserver.key
    docker restart jms_guacamole
    ```

    Windows 文件上传可以直接把文件拖拽到 Windows 窗口, 上传后文件在 计算机 - G盘, 下载把文件放到 G 盘的 download  目录即可弹出下载窗口, 快捷键上传下载工具栏 ++ctrl+alt+shift++
