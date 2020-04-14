Jms_guacamole 常见问题
-----------------------

- Jms_guacamole 是指 https://github.com/jumpserver/docker-guacamole 项目
- Jms_guacamole 默认的路径为 /opt/docker-guacamole

1. Jms_guacamole 启动异常、启动失败或者 Web 连接资产提示无权限访问、黑屏、白屏等

.. code-block:: shell

    # 检查 BOOTSTRAP_TOKEN 与 jumpserver 的 BOOTSTRAP_TOKEN 是否一致
    $ cat /opt/jumpserver/config.yml | grep BOOTSTRAP_TOKEN

    # 首先到 web - 会话管理 - 终端管理 里面删除 guacamole 的注册 [gua]xxxxxxx ( 在线显示红色的那个 )

    # 如果是极速安装部署的 guacamole
    $ docker stop jms_guacamole
    $ docker rm jms_guacamole
    $ Server_IP=`ip addr | grep 'state UP' -A2 | grep inet | egrep -v '(127.0.0.1|inet6|docker)' | awk '{print $2}' | tr -d "addr:" | head -n 1 | cut -d / -f1`
    $ docker run --name jms_guacamole -d -p 127.0.0.1:8081:8080 -e JUMPSERVER_SERVER=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN -e GUACAMOLE_LOG_LEVEL=ERROR --restart=always jumpserver/jms_guacamole:1.5.7

    # 如果是正常部署的 guacamole
    $ vi ~/.bashrc

    ...

    BOOTSTRAP_TOKEN=xxxxx  # 自行修改这里的 BOOTSTRAP_TOKEN 与 JumpServer 的一致

    ...

    $ rm -rf /config/guacamole/keys/*
    $ /etc/init.d/guacd start
    $ sh /config/tomcat9/bin/startup.sh

2. VNC 资产连接说明

.. code-block:: shell

    - VNC 目前不支持加密的连接
    # Windows 正常安装好 RealVNC Server, 注意安装过程中允许放行防火墙
    # 请在 Options-Security 选项里面设置 Encryption 为 Prefer off
    # 然后在 Options-Security 选项里面选择 Authentication 为 VNC password
    # 点击保存, 然后会提示输入 vnc 密码, 这个密码就是用来连接 vnc server
    # 在 web - 资产管理 - 资产列表 里面添加这台 vnc server 资产
    # 协议选择 vnc
    # 端口默认 5900, 不确定的话看下资产的 vnc server 主页上面有
    # 在 web - 资产管理 - 系统用户 里面创建系统用户
    # 协议选择 vnc
    # 用户名不填
    # 密码填刚才在资产设置的 vnc 密码
    # 授权然后到 web 连接即可

    # Centos 7
    $ yum -y groupinstall "GNOME Desktop" "Graphical Administration Tools"
    $ yum -y install tigervnc-server tigervnc
    $ cp /lib/systemd/system/vncserver@.service /lib/systemd/system/vncserver@:1.service
    $ vi /lib/systemd/system/vncserver\@\:1.service

    [Service]
    Type=forking
    User=<root>
    ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill :1 > /dev/null 2>&1 || :'
    ExecStart=/sbin/runuser -l root -c "/usr/bin/vncserver :1 -geometry 1280x720 -depth 24"
    PIDFile=/root/.vnc/%H%i.pid
    ExecStop=/bin/sh -c '/usr/bin/vncserver -kill :1 > /dev/null 2>&1 || :'
    [Install]
    WantedBy=multi-user.target

    $ systemctl daemon-reload
    $ vncpasswd  # 设置密码, 最后有个只读设置记得选 n
    $ firewall-cmd --permanent --add-service vnc-server  # 防火墙放行 vncserver 服务
    $ vncserver :1  # 启动 vncserver 5901 端口
    $ systemctl enable vncserver@:1

    # 在 web - 资产管理 - 资产列表 里面添加这台 vnc server 资产
    # 协议选择 vnc
    # 端口默认 5901 , 不确定的话到资产 ss -tunlp | grep vnc 查下端口
    # 在 web - 资产管理 - 系统用户 里面创建系统用户
    # 协议选择 vnc
    # 用户名不填
    # 密码填刚才在资产设置的 vnc 密码
    # 授权然后到 web 连接即可
