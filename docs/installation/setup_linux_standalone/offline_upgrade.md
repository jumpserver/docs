# 离线升级

!!! warning "注意"
    - [JumpServer 在做升级或迁移操作前，请先阅读升级须知](../upgrade_notice.md)
    - 升级前做好数据库的备份工作是一个良好的习惯。

=== "离线升级(linux/amd64)"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录。

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-amd64-{{ jumpserver.installer }}.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-amd64-{{ jumpserver.installer }}
        ```
        ```sh
        ./jmsctl.sh upgrade
        ./jmsctl.sh start
        ```

=== "离线升级(linux/arm64)"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/arm64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录。

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-arm64-{{ jumpserver.installer }}.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-arm64-{{ jumpserver.installer }}
        ```
        ```sh
        ./jmsctl.sh upgrade
        ./jmsctl.sh start
        ```

=== "离线升级(linux/loong64)"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/loong64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录。

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-loong64-{{ jumpserver.installer }}.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-loong64-{{ jumpserver.installer }}
        ```
        ```sh
        ./jmsctl.sh upgrade
        ./jmsctl.sh start
        ```


