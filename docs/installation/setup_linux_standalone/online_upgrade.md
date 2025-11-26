# 在线升级

!!! warning "JumpServer V3 如果要升级到 V4 版本，需要先升级到 V3 的最新版本，否则升级会失败！"

| OS/Arch       | Architecture | Linux Kernel | Offline Name                                     |
| :------------ | :----------- | :----------- | :----------------------------------------------- |
| linux/amd64   | x86_64       | >= 4.0       | jumpserver-installer-{{ jumpserver.tag }}.tar.gz |

## 1. 升级部署

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
