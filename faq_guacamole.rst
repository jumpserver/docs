Jms_guacamole 常见问题
-----------------------

- Jms_guacamole 是指 https://github.com/jumpserver/docker-guacamole 项目
- Jms_guacamole 默认的路径为 /opt/docker-guacamole

1. Jms_guacamole 启动异常或者启动失败

.. code-block:: shell

    # 检查 BOOTSTRAP_TOKEN 与 jumpserver 的 BOOTSTRAP_TOKEN 是否一致
    $ cat /opt/jumpserver/config.yml | grep BOOTSTRAP_TOKEN

    # 首先到 web - 会话管理 - 终端管理 里面删除 guacamole 的注册 [gua]xxxxxxx ( 在线显示红色的那个 )

    # 如果是极速安装部署的 guacamole
    $ docker stop jms_guacamole
    $ docker rm jms_guacamole
    $ Server_IP=`ip addr | grep 'state UP' -A2 | grep inet | egrep -v '(127.0.0.1|inet6|docker)' | awk '{print $2}' | tr -d "addr:" | head -n 1 | cut -d / -f1`
    $ docker run --name jms_guacamole -d -p 127.0.0.1:8081:8080 -e JUMPSERVER_SERVER=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN --restart=always jumpserver/jms_guacamole:1.5.5

    # 如果是正常部署的 guacamole
    $ vi ~/.bashrc

    ...

    BOOTSTRAP_TOKEN=xxxxx  # 自行修改这里的 BOOTSTRAP_TOKEN 与 Jumpserver 的一致

    ...

    $ rm -rf /config/guacamole/keys/*
    $ /etc/init.d/guacd start
    $ sh /config/tomcat9/bin/startup.sh

2. VNC 资产连接说明

.. code-block:: shell

    - VNC 目前不支持加密的连接
    # 如: RealVNC Server, 请在 Options-Security 选项里面设置 Encryption 为 Prefer off
