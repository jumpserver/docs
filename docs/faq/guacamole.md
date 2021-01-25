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

### 2. 频繁断开解决方案

!!! question "Win7/2008 频繁断开解决方案"

    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim hl_lines="14"
    ... 省略
    # Guacamole 配置
    JUMPSERVER_SERVER=http://core:8080
    JUMPSERVER_KEY_DIR=/config/guacamole/data/key/
    JUMPSERVER_RECORD_PATH=/config/guacamole/data/record/
    JUMPSERVER_DRIVE_PATH=/config/guacamole/data/drive/
    JUMPSERVER_ENABLE_DRIVE=true
    JUMPSERVER_CLEAR_DRIVE_SESSION=true
    JUMPSERVER_CLEAR_DRIVE_SCHEDULE=24
    # 添加下面内容
    JUMPSERVER_COLOR_DEPTH=32               # 远程桌面使用 32 位真彩
    JUMPSERVER_DPI=120                      # 远程桌面 DPI
    JUMPSERVER_DISABLE_BITMAP_CACHING=true  # 禁用RDP的内置位图缓存功能
    JUMPSERVER_DISABLE_GLYPH_CACHING=true   # 禁用RDP会话中的字形缓存
    ```
    ```sh
    ./jmsctl.sh restart
    ```

### 3. RDP VNC 显示效果优化

!!! question ""
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim hl_lines="11-14"
    ... 省略
    # Guacamole 配置
    JUMPSERVER_SERVER=http://core:8080
    JUMPSERVER_KEY_DIR=/config/guacamole/data/key/
    JUMPSERVER_RECORD_PATH=/config/guacamole/data/record/
    JUMPSERVER_DRIVE_PATH=/config/guacamole/data/drive/
    JUMPSERVER_ENABLE_DRIVE=true
    JUMPSERVER_CLEAR_DRIVE_SESSION=true
    JUMPSERVER_CLEAR_DRIVE_SCHEDULE=24
    # 添加下面内容
    JUMPSERVER_COLOR_DEPTH=32               # 远程桌面使用 32 位真彩
    JUMPSERVER_DPI=120                      # 远程桌面 DPI
    JUMPSERVER_DISABLE_BITMAP_CACHING=true  # 禁用RDP的内置位图缓存功能
    JUMPSERVER_DISABLE_GLYPH_CACHING=true   # 禁用RDP会话中的字形缓存
    ```
    ```sh
    ./jmsctl.sh restart
    ```
