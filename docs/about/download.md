# 资源下载

## [VideoPlayer](https://github.com/jumpserver/VideoPlayer/releases){:target="_blank"}

Jumpserver 离线录像播放器。

| 版本     | Windows :fontawesome-brands-windows: |  macOS :fontawesome-brands-apple: | Linux :fontawesome-brands-linux: |
| ------- | ------------------------------------ | --------------------------------- | -------------------------------- |
| 开源版本 | :material-check:                     | :material-check:                  | :material-close:                 |
| 企业版本 | :material-check:                     | :material-check:                  | :material-close:                 |

## [Clients](https://github.com/jumpserver/clients/releases){:target="_blank"}

JumpServer 客户端默认已经集成到 jumpserver 镜像，可以从 luna `帮助菜单` - `工具下载` 里下载安装，开源版本支持 SSH 的本地拉起，企业版本还支持 RDP 拉起。

| 版本     | Windows :fontawesome-brands-windows: |  macOS :fontawesome-brands-apple:   | Linux :fontawesome-brands-linux: |
| ------- | ------------------------------------ | ----------------------------------- | -------------------------------- |
| 开源版本 | :material-check:                     | :material-check:                    | :material-check:                 |
| 企业版本 | :material-check:                     | :material-check:                    | :material-check:                 |

## [Jmservisor](https://github.com/jumpserver/Jmservisor/releases){:target="_blank"}

配合 Jumpserver 企业版本使用拉起 Windows Server RemoteApp 功能使用的客户端。

| 版本     | Windows Server 2012/2016/2019 :fontawesome-brands-windows: |
| ------- | ----------------------------------------------------------- |
| 开源版本 | :material-close:                                           |
| 企业版本 | :material-check:                                           |

!!! tip ""
    - [Jmservisor 安装包][jmservisor]

## Installer

无法访问 GitHub 可以使用此地址下载离线安装包

| version                  | linux/amd64                                                                                | linux/arm64                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| {{ jumpserver.version }} | jumpserver-offline-installer-{{ jumpserver.version }}-amd64-{{ installer.version }}.tar.gz | jumpserver-offline-installer-{{ jumpserver.version }}-arm64-{{ installer.version }}.tar.gz | jumpserver-offline-installer-{{ jumpserver.version }}-loong64-{{ installer.version }}.tar.gz |

!!! tip ""
    - 链接: https://community.fit2cloud.com/#/products/jumpserver/downloads

[jmservisor]: https://download.jumpserver.org/public/Jmservisor-{{ jumpserver.jmservisor }}.msi
