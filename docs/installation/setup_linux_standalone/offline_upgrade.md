# 离线升级

!!! warning "JumpServer V3 如果要升级到 V4 版本，需要先升级到 V3 的最新版本，否则升级会失败！"

| OS/Arch       | Architecture | Linux Kernel | Offline Name                                     |
| :------------ | :----------- | :----------- | :----------------------------------------------- |
| linux/amd64   | x86_64       | >= 4.0       | jumpserver-ce-{{ jumpserver.tag }}-x86_64.tar.gz |

## 1. 升级部署

=== "linux/amd64"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录。

    !!! tip ""
        ```sh
        cd /opt
        tar -xf jumpserver-ce-{{ jumpserver.tag }}-x86_64.tar.gz
        cd jumpserver-ce-{{ jumpserver.tag }}-x86_64
        ```
        ```sh
        ./jmsctl.sh upgrade
        ./jmsctl.sh start
        ```