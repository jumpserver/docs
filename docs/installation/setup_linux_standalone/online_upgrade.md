# 在线升级

!!! warning "v3 版本与 v2 版本存在一定的差异，如需 v2 版本升级至 v3 版本 [请先阅读此文档](https://kb.fit2cloud.com/?p=06638d69-f109-4333-b5bf-65b17b297ed9){:target="_blank"}"

!!! info "升级前请先参考 [升级或迁移须知](../upgrade_notice.md)"

=== "中国大陆"
    !!! tip ""
        ```sh
        cd /opt
        wget https://resource.fit2cloud.com/jumpserver/installer/releases/download/{{ jumpserver.tag }}/jumpserver-installer-{{ jumpserver.tag }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.tag }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.tag }}
        ```
=== "其他地区"
    !!! tip ""
        ```sh
        cd /opt
        wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.tag }}/jumpserver-installer-{{ jumpserver.tag }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.tag }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.tag }}
        ```

!!! tip ""
    ```sh
    ./jmsctl.sh upgrade

    # 启动 JumpServer 服务
    ./jmsctl.sh start
    ```
