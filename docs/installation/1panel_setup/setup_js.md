# 1Panel 部署 JumpServer

## 1. 安装 1panel
!!! tip ""
    - 关于 1Panel 的安装部署与基础功能介绍，请参考 [1Panel 官方文档](https://1panel.cn/docs/installation/online_installation/) 。
    - 在完成了 1Panel 的安装部署后，根据提示网址打开浏览器进入 1Panel。
    

## 2. 安装数据库以及 Redis 服务
!!! warning ""
    - 在安装 JumpServer 之前，需要先在 1Panel 上安装所需的软件 **PostgreSQL**（或者 **MySQL**）以及 **Redis** 应用 。

## 3. 安装 JumpServer
!!! tip ""
    - 打开应用商店菜单 在全部栏 右边搜索栏搜索 **JumpServer** 找到后点击 **安装**。

![img](img/V4_1Panel_setup1.png)
!!! tip ""
    - 在安装之前会弹出各种安装版本的信息以及数据库选择等信息，需要输入数据库密码等信息，输入完成后点击 **确认** 即可进行安装。

![img](img/V4_1Panel_setup2.png)

!!! tip "详细参数说明:"

    | 参数                | 说明                                                         |
    | ------------------- | ------------------------------------------------------------ |
    | 名称                | 创建的 JumpServer 应用名称。                                 |
    | 版本                | 创建的 JumpServer 应用版本。                                 |
    | 加密签名            | JumpServer 的 SECRET_KEY，保持默认即可，迁移环境请保存该 SECRET_KEY。 |
    | 认证令牌            | JumpServer 的 BOOTSTRAP_TOKEN，保持默认即可，迁移环境请保存该 BOOTSTRAP_TOKEN。 |
    | 调试模式            | 支持开启调试模式。                                           |
    | 日志级别            | 日志级别，支持配置 DEBUG、INFO、WARNING、ERROR、CRITICAL 级别。 |
    | 数据库服务          | JumpServer 应用使用的 PostgreSQL 数据库应用，支持下拉选择已安装的 PostgreSQL 数据库应用，1Panel 会自动配置 JumpServer 使用该数据库。 |
    | 数据库名            | JumpServer 应用使用的数据库名称，1Panel 会在选中的数据库中自动创建这个数据库。 |
    | 数据库用户密码      | JumpServer 应用使用的数据库用户密码，1Panel 会在选中的数据库中自动为上一步创建的用户配置该密码。 |
    | 缓存服务服务        | JumpServer 应用使用的 Redis 数据库应用，支持下拉选择已安装的 Redis 数据库应用，1Panel 会自动配置 JumpServer 使用该数据库。 |
    | 缓存服务服务密码    | JumpServer 应用使用的 Redis 数据库密码，1Panel 会在选中的数据库中自动创建配置该密码。 |
    | Web 端口            | 通过 HTTP 协议访问 JumpServer 前端页面。                     |
    | SSH 端口            | SSH Client 方式使用终端工具连接 JumpServer，比如 Xshell、PuTTY、MobaXterm 等终端工具。 |
    | DOMAINS             | 定义可信任的访问 IP, 请根据实际情况修改，如果是公网 IP 请改成对应的公网 IP。 |
    | 容器名称            | JumpServer 应用的容器名称。                                  |
    | 端口外部访问        | 允许端口外部访问回放开防火墙端口。                           |
    | CPU 限制            | JumpServer 应用可以使用的 CPU 核心数。                       |
    | 内存限制            | JumpServer 应用可以使用的内存大小。                          |
    | 编辑 compose 文件   | 支持自定义 compose 文件启动容器。                            |



!!! info "弹出以下日志记录，出现 **TASK-END** 表示安装完成。"

![img](img/V4_1Panel_setup4.png)

## 4. 访问 JumpServer
!!! info "安装成功后，通过浏览器访问登录 JumpServer。"
    ```sh
    地址: http://<1Panel 服务器 IP 地址>:<JumpServer 服务运行端口>
    用户名: admin
    密码: ChangeMe
    ```
  

