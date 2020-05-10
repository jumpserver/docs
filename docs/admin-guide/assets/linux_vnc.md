# Linux VNC 资产要求

!!! info "资产必须部署 vncserver"

!!! info "防火墙 vncserver 端口必须开放给 jumpserver 所有服务器访问"

!!! tip "Centos 7 示例"
    ```sh
    yum -y groupinstall "GNOME Desktop" "Graphical Administration Tools"
    yum -y install tigervnc-server tigervnc
    cp /lib/systemd/system/vncserver@.service /lib/systemd/system/vncserver@:1.service
    ```
    ```sh
    vi /lib/systemd/system/vncserver\@\:1.service
    ```
    ```vim
    [Service]
    Type=forking
    User=<root>
    ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill :1 > /dev/null 2>&1 || :'
    ExecStart=/sbin/runuser -l root -c "/usr/bin/vncserver :1 -geometry 1280x720 -depth 24"
    PIDFile=/root/.vnc/%H%i.pid
    ExecStop=/bin/sh -c '/usr/bin/vncserver -kill :1 > /dev/null 2>&1 || :'
    [Install]
    WantedBy=multi-user.target
    ```
    ```sh
    systemctl daemon-reload
    ```
    ```sh
    vncpasswd
    ```

    !!! info "安装提示设置密码, 这个密码填在 `jumpserver` `系统用户` 上, `用户名` 为空不需要填写"

    ```sh
    firewall-cmd --permanent --add-service vnc-server
    ```
    ```sh
    vncserver :1
    ```

    !!! info "`:1` 为 `5901` 端口, 同理 `:2` 为 `5902`"

    ```sh
    systemctl enable vncserver@:1
    ```
