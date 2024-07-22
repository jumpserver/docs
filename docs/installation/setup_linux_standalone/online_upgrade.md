# 在线升级

!!! warning "升级到 v4 前需要先升级到 v3 最新版本，否则升级将会直接失败"

| OS/Arch       | Architecture | Linux Kernel | Offline Name                                     |
| :------------ | :----------- | :----------- | :----------------------------------------------- |
| linux/amd64   | x86_64       | >= 4.0       | jumpserver-installer-{{ jumpserver.tag }}.tar.gz |
| linux/arm64   | aarch64      | >= 4.0       | jumpserver-installer-{{ jumpserver.tag }}.tar.gz |

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
