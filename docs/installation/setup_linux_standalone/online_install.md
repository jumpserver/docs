# 在线安装
 
!!! tip "[JumpServer 部署环境要求可点击后进行参考](../setup_linux_standalone/requirements.md)"

## 1. 安装部署

=== "中国大陆"
    !!! tip ""
        <div class="termy">
        ```console
        // root@localhost:/opt#
        $ curl -sSL https://resource.fit2cloud.com/jumpserver/jumpserver/releases/latest/download/quick_start.sh | bash

        ---> 100%
        <span style="color: green;">[Success]</span>: download install script to /opt/jumpserver-installer-{{jumpserver.tag}}
        [Info]: Start executing the installation script.
        [Info]: In an automated script deployment, note the message prompts on the screen.
        ---> 100%
        <span style="color: green;">[Success]</span>: The Installation is Complete.

        For more commands, you can enter <span style="color: red;">jmsctl --help</span> to view help information.
        ```
        </div>
=== "其他地区"
    !!! tip ""
        <div class="termy">
        ```console
        // root@localhost:/opt#
        $ curl -sSL https://github.com/jumpserver/jumpserver/releases/latest/download/quick_start.sh | bash

        ---> 100%
        <span style="color: green;">[Success]</span>: download install script to /opt/jumpserver-installer-{{jumpserver.tag}}
        [Info]: Start executing the installation script.
        [Info]: In an automated script deployment, note the message prompts on the screen.
        ---> 100%
        <span style="color: green;">[Success]</span>: The Installation is Complete.

        For more commands, you can enter <span style="color: red;">jmsctl --help</span> to view help information.
        ```
        </div>

!!! info "安装完成后 JumpServer 配置文件路径为： /opt/jumpserver/config/config.txt"

!!! tip ""
    ```sh
    cd /opt/jumpserver-installer-{{ jumpserver.tag }}

    # 启动
    ./jmsctl.sh start

    # 停止
    ./jmsctl.sh down

    # 卸载
    ./jmsctl.sh uninstall

    # 帮助
    ./jmsctl.sh -h
    ```

## 2. 环境访问
!!! info "安装成功后，通过浏览器访问登录 JumpServer"

!!! tip ""
    ```sh
    地址: http://<JumpServer服务器IP地址>:<服务运行端口>
    用户名: admin
    密码: admin
    ```
![登陆页面](../../img/online_install_01.png)
