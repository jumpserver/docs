# Linux VNC 资产要求

!!! tip "资产要求"
    - 资产必须部署 vncserver
    - 防火墙 vncserver 端口必须开放给 JumpServer 所有服务器访问

!!! tip ""
    - Centos 7 示例
    
    ```sh
    yum -y groupinstall "GNOME Desktop" "Graphical Administration Tools"
    yum -y install tigervnc-server tigervnc
    ```
    ```sh
    vncpasswd
    ```
    ```
    Password: ******
    Verify: ******
    Would you like to enter a view-only password (y/n)? n
    A view-only password is not used
    ```

    - 安装提示设置密码，这个密码填在 `JumpServer` `系统用户` 上，`用户名` 为空不需要填写

    ```sh
    firewall-cmd --permanent --add-service vnc-server
    firewall-cmd --reload
    ```
    ```sh
    vncserver :1
    ```

    - `:1` 为 `5901` 端口，同理 `:2` 为 `5902`
