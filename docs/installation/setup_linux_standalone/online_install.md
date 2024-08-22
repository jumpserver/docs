# 在线安装
 
!!! tip "[JumpServer 部署环境要求可点击后进行参考](../setup_linux_standalone/requirements.md)"

## 1. 安装部署

=== "中国大陆"
    !!! tip ""
        <div class="termy">
        ```console
        // root@localhost:/opt#
        $ curl -sSL https://resource.fit2cloud.com/jumpserver/jumpserver/releases/download/{{ jumpserver.tag }}/quick_start.sh | bash

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
        $ curl -sSL https://github.com/jumpserver/jumpserver/releases/download/{{ jumpserver.tag }}/quick_start.sh | bash

        ---> 100%
        <span style="color: green;">[Success]</span>: download install script to /opt/jumpserver-installer-{{jumpserver.tag}}
        [Info]: Start executing the installation script.
        [Info]: In an automated script deployment, note the message prompts on the screen.
        ---> 100%
        <span style="color: green;">[Success]</span>: The Installation is Complete.

        For more commands, you can enter <span style="color: red;">jmsctl --help</span> to view help information.
        ```
        </div>

!!! tip "提示"
    - 首次安装后需要修改配置文件，定义 DOMAINS 字段后即可正常使用
    - 如果服务器是一键安装并且旧版本就已经使用 JumpServer 开启了 HTTPS，则不需要进行任何更改。
    - 需要使用 IP 地址来访问 JumpServer 的场景，可以根据自己的 IP 类型来填写 config.txt 配置文件中 DOMAINS 字段为公网 IP 还是内网 IP。

    ```
      # 打开config.txt 配置文件，定义 DOMAINS 字段
      vim /opt/jumpserver/config/config.txt 

      # 可信任 DOMAINS 定义,
      # 定义可信任的访问 IP, 请根据实际情况修改, 如果是公网 IP 请改成对应的公网 IP,
      # DOMAINS="demo.jumpserver.org"    # 使用域名访问
      # DOMAINS="172.17.200.191"         # 使用 IP 访问
      # DOMAINS="demo.jumpserver.org,172.17.200.191"    # 使用 IP 和 域名一起访问
      DOMAINS=
    ```

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
    ```sh
    地址: http://<JumpServer服务器IP地址>:<服务运行端口>
    用户名: admin
    密码: admin
    ```
![登录页面](../../img/online_install_01.png)
