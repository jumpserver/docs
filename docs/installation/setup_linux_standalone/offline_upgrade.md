# 离线升级

!!! warning "v3 版本与 v2 版本存在一定的差异，如需 v2 版本升级至 v3 版本 [请先阅读此文档](https://kb.fit2cloud.com/?p=06638d69-f109-4333-b5bf-65b17b297ed9){:target="_blank"}"

!!! info "升级前请先参考 [升级或迁移须知](../upgrade_notice.md)"

=== "离线升级(linux/amd64)"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录。

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-amd64.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-amd64
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
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-arm64.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-arm64
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
        tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-loong64.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.tag }}-loong64
        ```
        ```sh
        ./jmsctl.sh upgrade
        ./jmsctl.sh start
        ```
