# 离线升级

!!! warning "升级到 v4 前需要先升级到 v3 最新版本，否则升级将会直接失败"

| OS/Arch       | Architecture | Linux Kernel | Offline Name                                     |
| :------------ | :----------- | :----------- | :----------------------------------------------- |
| linux/amd64   | x86_64       | >= 4.0       | jumpserver-ce-{{ jumpserver.tag }}-x86_64.tar.gz |

## 1. 升级部署

!!! warning ""
    - 离线升级目前只支持 linux/amd64 架构，其他架构升级请参考 [在线升级](./online_upgrade.md)

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