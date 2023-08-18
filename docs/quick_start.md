# 快速入门
## 1 一键安装
!!! tip ""
    - 支持主流 Linux 发行版本（基于 Debian / RedHat，包括国产操作系统）
    - Gentoo / Arch Linux 请通过 [源码安装](installation/source_install/requirements.md)
 
!!! tip ""
    === "中国大陆"
        <div class="termy">
        ```console
        // root@localhost:/opt#
        $ curl -sSL https://resource.fit2cloud.com/jumpserver/jumpserver/releases/latest/download/quick_start.sh | bash

        ---> 100%
        <span style="color: green;">[Success]</span>: download install script to /opt/jumpserver-installer-{{jumpserver.tag}}
        [Info]: Start executing the installation script.
        [Info]: In an automated script deployment, note the message prompts on the screen.
        ---> 100%
        <span style="color: green;">[Success]</span>: The Installation is Complete.

        For more commands, you can enter <span style="color: red;">jmsctl --help</span> to view help information.
        ```
        </div>
    === "其他地区"
        <div class="termy">
        ```console
        // root@localhost:/opt#
        $ https://github.com/jumpserver/jumpserver/releases/latest/download/quick_start.sh | bash

        ---> 100%
        <span style="color: green;">[Success]</span>: download install script to /opt/jumpserver-installer-{{jumpserver.tag}}
        [Info]: Start executing the installation script.
        [Info]: In an automated script deployment, note the message prompts on the screen.
        ---> 100%
        <span style="color: green;">[Success]</span>: The Installation is Complete.

        For more commands, you can enter <span style="color: red;">jmsctl --help</span> to view help information.
        ```
        </div>

!!! tip "提示"
    - 首次安装后需要修改配置文件，定义 DOMAINS 字段后即可正常使用。
    - 如果服务器是一键安装并且旧版本就已经使用 JumpServer 开启了 HTTPS，则不需要进行任何更改。
    - 需要使用 IP 地址来访问 JumpServer 的场景，可以根据自己的 IP 类型来填写 config.txt 配置文件中 DOMAINS 字段为公网 IP 还是内网 IP。

    ```
      # 打开config.txt 配置文件，定义 DOMAINS 字段
      vim /opt/jumpserver/config/config.txt 

      # 可信任 DOMAINS 定义,
      # 定义可信任的访问 IP, 请根据实际情况修改, 如果是公网 IP 请改成对应的公网 IP,
      # DOMAINS="demo.jumpserver.org"    # 使用域名访问
      # DOMAINS="172.17.200.191"         # 使用 IP 访问
      # DOMAINS="demo.jumpserver.org,172.17.200.191"    # 使用 IP 和 域名一起访问
      DOMAINS=
    ```

!!! info "安装成功后，通过浏览器访问登录 JumpServer"
    ```sh
    地址: http://<JumpServer服务器IP地址>:<服务运行端口>
    用户名: admin
    密码: admin
    ```

## 2 资产管理
### 2.1 准备工作
!!! tip ""
    - 准备两个测试资产和一个数据库来验证功能。

!!! tip ""

    |   IP 地址     |    主机名       |    端口    | 操作系统         |  管理员用户    |    密码       |
    | ------------ | --------------- | ---------- | ---------------- |--- ---------- |--- ---------- |
    | 172.16.80.11 |    test_ssh01   |     22     |     Centos 7     |      root     |  Test2020.L   |
    | 172.16.80.21 |    test_rdp01   |    3389    |    Windows 10    | administrator |  Test2020.W   |
    | 172.16.80.31 |   test_mysql01  |    3306    |      MySQL 5     |      root     |  Test2020.M   |

!!! warning "注意"
    - Windows 资产如需执行 `更新资产` 信息、`可连接性测试` 等自动化任务，需先进行 [Windows SSH 设置](guide/asset_requirements/windows_ssh.md)，此非登录 Windows 资产的必填项。
    - MySQL 应用需要授权 `Core` 和 `KoKo` 的远程访问的权限 [MySQL 应用要求](guide/asset_requirements/mysql.md)

### 2.2 编辑资产树
!!! tip ""
    - 点击页面左侧的 `资产管理` - `资产列表`，在根节点 `Default` 右键新建 `SSH Server` 、 `RDP Server` 、`Database` 三个节点。
!!! tip ""
    - 资产树样式如下：

    ```
    Default
    ├─ SSH Server
    └─ RDP Server
    └─ DB
    ```

!!! warning "注意"
    - 根节点 `Default` 不能重命名，右击节点可以 `添加`、`删除` 和 `重命名` 节点，以及进行资产相关的操作。  

### 2.3 创建资产
!!! tip ""
    - 点击页面左侧的 `资产管理` - `资产列表` - `主机` - `创建` 创建一台 Linux 服务器，并在创建资产过程中，创建特权用户，内容就是上面表单的 `管理员用户` 和 `密码`。
    - Windows 资产的创建流程同样如此。

!!! tip ""
    - 创建 Linux 资产样式如下：

!!! tip ""

    | 名称        | IP/主机      | 资产平台 | 节点          | 协议组    | 账号列表   |
    | ---------- | ------------ | ------- | ------------ | -------  | -------- |
    | test_ssh01 | 172.16.80.11 | Linux   | /Default/SSH Server | ssh 22 | 添加 |

!!! tip ""
    - 添加登录资产用户样式如下：

!!! tip ""

    | 名称              | 用户名 | 特权用户 | 密文类型     | 密码          |
    | ----------------- | ---- | ------- | ---------- | ---------------- |
    | 172.16.80.11_root | root  | 是 | 密码 |Test2020.L |

!!! warning "注意"
    - `名称` 不能重名，`密码` 或者 `密钥` 二选一即可，一些资产不允许通过 `密码` 认证可以改用 `私钥` 认证。  
    - `特权用户` 仅支持 `SSH` 协议，用于资产 `可连接性测试`、`推送用户`、`批量改密` 等自动化任务。
    - 资产创建信息填写好保存之后隔几秒钟时间刷新一下网页，`ssh` 协议资产的可连接图标会显示 `绿色`，且 `硬件信息` 会显示出来。  
    - 如果 `可连接` 的图标是 `黄色` 或者 `红色`，可以点击 `资产` 的 `名称`，在右侧 `快速修改` - `测试可连接性` 点击 `测试` 按钮，根据错误提示处理。  
    - 被连接 `Linux` 资产需要 `python` 组件，且版本大于等于 `2.6`，`Ubuntu` 等资产默认不允许 `root` 用户远程 `ssh` 登录，请自行处理，`Windows` 资产需要手动安装 `OpenSSH Server `。
    - 如果资产不能正常连接，请检查 特权用户 的 `用户名` 和 `密码` 是否正确以及该 `特权用户` 是否能使用 `SSH` 从 `JumpServer` 主机正确登录到资产主机上。

### 2.4 创建数据库应用
!!! tip ""
    - 点击页面左侧的 `资产管理` - `资产列表` - `创建` - `数据库下选择 MySQL 数据库`。

!!! tip ""
    - 创建 MySQL 数据库应用样式如下：

!!! tip ""

    | 名称         | 地址   | 节点         | 数据库 | 协议组 | 账号列表  |
    | ------------ | ----- | ------------ | ---- | ----- | ----- |
    | test_mysql01 | 172.16.80.31 | /Default/DB | test | mysql:3306  | 添加 |

!!! tip ""
    - 添加登录数据库用户样式如下：

!!! tip ""

    |        名称       | 用户名 | 特权用户 | 密文类型 | 密码   |
    | ----------------- | ----- | ------ | ------- | -------- |
    | 172.16.80.23_root | root  | root   | 密码    |Test2020.M |

!!! warning "注意"
    - 名称、主机、数据库选项为必填项。

## 3 创建授权规则
!!! tip ""
    - 点击页面左侧的 `权限管理` - `资产授权` - `创建` 创建一个授权。
    - Windows 资产、MySQL 数据库 的授权流程和下述内容相同。

!!! tip ""
    - 创建登录授权规则（例如 Linux 资产），样式如下：

!!! tip ""

    | 名称             | 用户                 | 用户组 | 资产                     | 节点 | 账号                                  | 动作                  |
    | ---------------- | -------------------- | ----- | ------------------------ | --- | ----------------------------------------- | -------------------- |
    | admin_ssh01 | Administrator(admin) |   -    | test_ssh01(172.16.80.11) |  -   | 所有账号                  | :material-check: 全部 |

!!! warning "注意"
    - `名称`，授权的名称，不能重复。  
    - `用户` 和 `用户组` 二选一，不推荐即选择 `用户` 又选择 `用户组`。  
    - `资产` 和 `节点` 二选一，选择 `节点` 会包含 `节点` 下面的所有 `资产`。  
    - `账号`，`账号` 为连接资产的 `认证凭据`。  
    - `用户(组)`，`资产(节点)` 是一对一的关系，所以当拥有 `Linux`、`Windows` 不同类型资产时，应该分别给 `Linux` 资产和 `Windows` 资产创建 `授权规则`。  

## 4 用户登录
!!! tip ""
    - 点击页面右上角的 `Web 终端` 进行资产连接。

!!! warning "注意"
    - 用户只能看到自己被管理员授权了的 `资产`，如果登录后无资产，请联系管理员进行确认。

## 5 系统设置
!!! tip ""
    - 点击页面右上角的 `系统设置` 进行配置。

### 5.1 基本设置
!!! tip ""

    | 名称          | 示例                        | 备注                                         |
    | ------------ | --------------------------- | -------------------------------------------- |
    | 当前站点URL   | https://demo.jumpserver.org | 不设置的话，邮件收到的地址为 `http://localhost` |
    | 用户向导URL   |                             | 用户首次登录可以看到此 `超链接`，可以不设置      |
    | 忘记密码URL   |                             | 使用了 LDAP, OPENID 等外部认证系统，可以自定义  |

### 5.2 邮件设置
!!! tip ""

    | 名称 | 示例 | 备注 |
    | ---------- | ---------------- | ---------------------------------- |
    | SMTP主机   | smtp.qq.com      | 服务商提供的 smtp 服务器             |
    | SMTP端口   | 25               | 通常是 `25`                         |
    | SMTP账号   | **********@qq.com | 通常是 `user@domain.com`            |
    | SMTP密码   | **************** | 每次 `测试连接` 都需要重新输入密码    |
    | 使用SSL    | [ ]              | 如果端口使用 `465`，必须勾选此项      |
    | 使用TLS    | [ ]              | 如果端口使用 `587`，必须勾选此项      |
    | 发件人     | **********@qq.com | `测试连接` 必须要输入                |
    | 主题前缀   | [JMS]            | 邮件的标题，收到的邮件是 `[JMS]` 开头 |
    | 测试收件人 | **********@qq.com | 测试连接必填                         |

!!! warning "注意"
    - 不可以同时勾选 `使用 SSL` 和 `使用 TLS`。

## 6 常用功能操作
!!! tip ""
    - **[通过 SFTP 上传下载][通过 SFTP 上传下载]**
    - **[Windows 上传下载][Windows 上传下载]**
    - **[限制 IP 登录][限制 IP 登录]**
    - **[纳管数据库应用][纳管数据库应用]**
    - **[Redis 数据库纳管][Redis 数据库纳管]**


[通过 SFTP 上传下载]: https://kb.fit2cloud.com/?p=115
[Windows 上传下载]: https://kb.fit2cloud.com/?p=87
[限制 IP 登录]: https://kb.fit2cloud.com/?p=199
[Redis 数据库纳管]: https://kb.fit2cloud.com/?p=91
[纳管数据库应用]: https://kb.fit2cloud.com/?p=79
