# 1 Panel 部署 JumpServer

!!! warning ""
    - 在安装 JumpServer 之前，需要先在 1Panel 上安装所需的软件 **MySQL** 和 **Redis** 。

!!! tip ""
    - 打开应用商店菜单 在全部栏 右边搜索栏搜索  **JumpServer**  找到后点击 **安装**

![img](/img/V4_1Panel_setup1.png)
!!! tip ""
    - 在安装之前会弹出 各种安装版本的信息 以及数据库选择等信息， 需要输入数据库密码等信息，输入完成后点击 **确认** 即可进行安装

![img](/img/V4_1Panel_setup2.png)

!!! tip ""
    - 详细参数说明:

    | 参数                | 说明                                                         |
    | ------------------- | ------------------------------------------------------------ |
    | 名称                | 创建的 JumpServer 应用名称。                                 |
    | 版本                | 创建的 JumpServer 应用版本。                                 |
    | 加密签名            | JumpServer 的 SECRET_KEY，保持默认即可，迁移环境请保存该 SECRET_KEY。 |
    | 认证令牌            | JumpServer 的 BOOTSTRAP_TOKEN，保持默认即可，迁移环境请保存该 BOOTSTRAP_TOKEN。 |
    | 调试模式            | 支持开启调试模式。                                           |
    | 日志级别            | 日志级别，支持配置 DEBUG、INFO、WARNING、ERROR、CRITICAL 级别。 |
    | 数据库服务          | JumpServer 应用使用的 MySQL 数据库应用，支持下拉选择已安装的 MySQL 数据库应用，1Panel 会自动配置 JumpServer 使用该数据库。 |
    | 数据库名            | JumpServer 应用使用的数据库名称，1Panel 会在选中的数据库中自动创建这个数据库。 |
    | 数据库用户密码      | JumpServer 应用使用的数据库用户密码，1Panel 会在选中的数据库中自动为上一步创建的用户配置该密码。 |
    | 缓存服务服务        | JumpServer 应用使用的 Redis 数据库应用，支持下拉选择已安装的 Redis 数据库应用，1Panel 会自动配置 JumpServer 使用该数据库。 |
    | 缓存服务服务密码    | JumpServer 应用使用的 Redis 数据库密码，1Panel 会在选中的数据库中自动创建配置该密码。 |
    | Web 端口            | 通过 HTTP 协议访问 JumpServer 前端页面。                     |
    | SSH 端口            | SSH Client 方式使用终端工具连接 JumpServer，比如 Xshell、PuTTY、MobaXterm 等终端工具。 |
    | Magnus MySQL 端口   | DB Client 方式连接 MySQL 数据库资产。                        |
    | Magnus Mariadb 端口 | DB Client 方式连接 MariaDB 数据库资产。                      |
    | DOMAINS             | 定义可信任的访问 IP, 请根据实际情况修改，如果是公网 IP 请改成对应的公网 IP。 |
    | 容器名称            | JumpServer 应用的容器名称。                                  |
    | 端口外部访问        | 允许端口外部访问回放开防火墙端口。                           |
    | CPU 限制            | JumpServer 应用可以使用的 CPU 核心数。                       |
    | 内存限制            | JumpServer 应用可以使用的内存大小。                          |
    | 编辑 compose 文件   | 支持自定义 compose 文件启动容器。                            |



!!! tip ""
    - 弹出以下日志记录， 出现 **TASK-END** 表示安装完成

![img](/img/V4_1Panel_setup4.png)

!!! tip ""
    - 安装完成后在应用商店的已安装页，可点击 **参数** 进行相关配置的查看与修改

![img](/img/V4_1Panel_setup5.png)

!!! tip ""
    - 在 **参数** 页面，可以编辑 Web访问地址 ，加密签名 令牌等数据，修改完成后点击 **确认** 即可

![img](/img/V4_1Panel_setup6.png)

  

