# 资源下载

## [VideoPlayer](https://github.com/jumpserver/VideoPlayer/releases){:target="_blank"}

Jumpserver 离线录像播放器。

| 版本     | Windows :fontawesome-brands-windows: |  macOS :fontawesome-brands-apple: | Linux :fontawesome-brands-linux: |
| ------- | ------------------------------------ | --------------------------------- | -------------------------------- |
| 开源版本 | :material-check:                     | :material-check:                  | :material-close:                 |
| 企业版本 | :material-check:                     | :material-check:                  | :material-close:                 |

## [Clients](https://github.com/jumpserver/clients/releases){:target="_blank"}

JumpServer 客户端，支持 RDP 的本地拉起，后续会支持拉起 ssh。

| 版本     | Windows :fontawesome-brands-windows: |  macOS :fontawesome-brands-apple:   | Linux :fontawesome-brands-linux: |
| ------- | ------------------------------------ | ----------------------------------- | -------------------------------- |
| 开源版本 | :material-close:                     | :material-close:                    | :material-close:                 |
| 企业版本 | :material-check:                     | :material-check:                    | :material-close:                 |

!!! tip ""
    - [Windows 客户端][win-client]
    - [macOS 客户端][mac-client]
    - [macOS Remote_Desktop 客户端][mac-mrd]

## [Jmservisor](https://github.com/jumpserver/Jmservisor/releases){:target="_blank"}

配合 Jumpserver 企业版本使用拉起 Windows Server RemoteApp 功能使用的客户端。

| 版本     | Windows :fontawesome-brands-windows: |  macOS :fontawesome-brands-apple: | Linux :fontawesome-brands-linux: |
| ------- | ------------------------------------ | --------------------------------- | -------------------------------- |
| 开源版本 | :material-close:                     | :material-close:                  | :material-close:                 |
| 企业版本 | :material-check:                     | :material-close:                  | :material-close:                 |

## Installer

无法访问 GitHub 可以使用此地址下载离线安装包

| version                  | linux/amd64                                                                              | linux/arm64                                                                              |
| ------------------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| {{ jumpserver.version }} | jumpserver-offline-installer-{{ jumpserver.version }}-amd64-{{ installer.amd64 }}.tar.gz | jumpserver-offline-installer-{{ jumpserver.version }}-arm64-{{ installer.arm64 }}.tar.gz |

!!! tip ""
    - 链接: https://community.fit2cloud.com/#/products/jumpserver/downloads

[win-client]: https://download.jumpserver.org/public/jumpserver-client.msi.zip
[mac-client]: https://download.jumpserver.org/public/jumpserver-client.dmg
[mac-mrd]: https://download.jumpserver.org/public/Microsoft_Remote_Desktop_10.6.7_installer.pkg
