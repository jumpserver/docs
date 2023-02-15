# 在线升级

!!! warning "注意"
    - [JumpServer 在做升级或迁移操作前，请先阅读升级须知](../linux_stand-alone/upgrade_notice.md)
    - 升级前做好数据库的备份工作是一个良好的习惯。
!!! tip ""
    - 如果您的服务器可以访问互联网，可以通过以下命令直接升级 JumpServer 至最新版本。

    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```
    ```sh
    # 升级至最新版本
    ./jmsctl.sh upgrade
    # 启动 JumpServer 服务
    ./jmsctl.sh start
    # 查看 JumpServer 服务状态
    ./jmsctl.sh status
    ```