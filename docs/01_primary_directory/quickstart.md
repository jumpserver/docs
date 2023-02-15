# 快速入门
## 1 一键安装
!!! tip ""
    - 支持主流 Linux 发行版本（基于 Debian / RedHat，包括国产操作系统）
    - Gentoo / Arch Linux 请通过 [源码安装](../build.md)
<div class="termy">
```console
// root@localhost:/opt#
$ curl -sSL https://github.com/jumpserver/jumpserver/releases/download/{{ jumpserver.version }}/quick_start.sh | bash

---> 100%
<span style="color: green;">[Success]</span>: download install script to /opt/jumpserver-installer-{{ jumpserver.version }}
[Info]: Start executing the installation script.
[Info]: In an automated script deployment, note the message prompts on the screen.
---> 100%
<span style="color: green;">[Success]</span>: The Installation is Complete.

For more commands, you can enter <span style="color: red;">jmsctl --help</span> to view help information.
```
</div>


!!! info "提示"
    - 以下操作均在 Web 页面完成，请使用 admin 用户登陆，默认密码 admin

## 2 系统设置

!!! note "点击页面右上角的 `系统设置` 进行配置"

### 2.1 基本设置

| 名称          | 示例                        | 备注                                         |
| ------------ | --------------------------- | -------------------------------------------- |
| 当前站点URL   | https://demo.jumpserver.org | 不设置的话，邮件收到的地址为 `http://localhost` |
| 用户向导URL   |                             | 用户首次登陆可以看到此 `超链接`，可以不设置      |
| 忘记密码URL   |                             | 使用了 LDAP, OPENID 等外部认证系统，可以自定义  |

### 2.2 邮件设置

| 名称 | 示例 | 备注 |
| ---------- | ---------------- | ---------------------------------- |
| SMTP主机   | smtp.qq.com      | 服务商提供的 smtp 服务器             |
| SMTP端口   | 25               | 通常是 `25`                         |
| SMTP账号   | 296015668@qq.com | 通常是 `user@domain.com`            |
| SMTP密码   | **************** | 每次 `测试连接` 都需要重新输入密码    |
| 使用SSL    | [ ]              | 如果端口使用 `465`，必须勾选此项      |
| 使用TLS    | [ ]              | 如果端口使用 `587`，必须勾选此项      |
| 发件人     | 296015668@qq.com | `测试连接` 必须要输入                |
| 主题前缀   | [JMS]            | 邮件的标题，收到的邮件是 `[JMS]` 开头 |
| 测试收件人 | 296015668@qq.com | 测试连接必填                         |

!!! warning "注意"
    - 不可以同时勾选 `使用SSL` 和 `使用TLS`


## 3 资产管理

!!! note "准备两个测试资产和一个数据库来验证功能"

|      IP      |    Host name    |    Port    | Operating System |  Admin User   |    Password   |
| ------------ | --------------- | ---------- | ---------------- |--- ---------- |--- ---------- |
| 172.16.80.11 |    test_ssh01   |     22     |     Centos 7     |      root     |  Test2020.L   |
| 172.16.80.21 |    test_rdp01   |    3389    |    Windows 10    | administrator |  Test2020.W   |
| 172.16.80.31 |   test_mysql01  |    3306    |      MySQL 5     |      root     |  Test2020.M   |

!!! warning "注意"
    - Windows 资产如需执行 `更新资产` 信息、`可连接性测试` 等自动化任务，需先进行 [Windows SSH 设置](assets/windows_ssh.md)，此非登录 Windows 资产的必填项
    - MySQL 应用需要授权 `Core` 和 `KoKo` 的远程访问的权限 [MySQL 应用要求](app/mysql.md)

### 3.1 编辑资产树###

!!! note "点击页面左侧的 `资产管理` - `资产列表`，在根节点 `Default` 右键新建 `SSH Server` 和 `RDP Server` 两个节点"

```
Defaule
├─ SSH Server
└─ RDP Server
```

!!! warning "注意"
    根节点 `Default` 不能重名，右击节点可以 `添加`、`删除` 和 `重命名` 节点，以及进行资产相关的操作  

### 3.2 创建特权用户

!!! note "点击页面左侧的 `资产管理` - `系统用户` - `创建特权用户` 创建两个特权用户，特权用户的内容就是上面表单的 `Admin User` 和 `Password`"

| 名称                        | 协议 | 用户名        | 密码       | SSH密钥          | 密钥密码          |
| -------------------------- | ---- | ------------- | ---------- | ---------------- | ---------------- |
| 172.16.80.11_root          | SSH  | root          | Test2020.L |                  |                  |
| 172.16.80.21_administrator | SSH  | administrator | Test2020.W |                  |                  |

!!! warning ""
    - `名称` 不能重名，`密码` 或者 `密钥` 二选一即可，一些资产不允许通过 `密码` 认证可以改用 `私钥` 认证  
    - `特权用户` 仅支持 `SSH` 协议，用于资产 `可连接性测试`、`推送用户`、`批量改密` 等自动化任务

### 3.3 创建资产

!!! note "点击页面左侧的 `资产管理` - `资产列表` - `创建资产` 把两个资产导入"

| 主机名      | IP(域名)     | 系统平台 | 协议组            | 特权用户                    | 节点                 |
| ---------- | ------------ | ------- | ----------------- | -------------------------- | -------------------- |
| test_ssh01 | 172.16.80.11 | Linux   | ssh 22            | 172.16.80.11_root          | Default / SSH Server |
| test_rdp01 | 172.16.80.21 | Windows | rdp 3389 / ssh 22 | 172.16.80.21_administrator | Default / RDP Server |

!!! warning "注意"
    - 资产创建信息填写好保存之后隔几秒钟时间刷新一下网页，`ssh` 协议资产的可连接图标会显示 `绿色`，且 `硬件信息` 会显示出来  
    - 如果 `可连接` 的图标是 `黄色` 或者 `红色`，可以点击 `资产` 的 `名称`，在右侧 `快速修改` - `测试可连接性` 点击 `测试` 按钮，根据错误提示处理  
    - 被连接 `Linux` 资产需要 `python` 组件，且版本大于等于 `2.6`，`Ubuntu` 等资产默认不允许 `root` 用户远程 `ssh` 登录，请自行处理，`Windows` 资产需要手动安装 `OpenSSH Server `
    - 如果资产不能正常连接，请检查 特权用户 的 `用户名` 和 `密码` 是否正确以及该 `特权用户` 是否能使用 `SSH` 从 `JumpServer` 主机正确登录到资产主机上

### 3.4 创建数据库应用

!!! note "击页面左侧的 `应用管理` - `数据库应用` - `创建数据库应用` 创建 mysql 数据库"

| 名称         | 类型   | 主机         | 端口 | 数据库 | 备注  |
| ------------ | ----- | ------------ | ---- | ----- | ----- |
| test_mysql01 | MySQL | 172.16.80.31 | 3306 | test  | MySQL |

!!! warning ""
    - 名称、主机、数据库选项为必填项

### 3.5 创建系统用户

|      IP      |   System   | Type  | System User  |    Password   |     Group    |     Sudo     |  Sftp Root  |
| ------------ | ---------- | ----- | ------------ | ------------- | ------------ | ------------ | ----------- |
| 172.16.80.11 |  Centos 7  |  SSH  |  testssh01   |  random pass  |              |      ALL     |      /      |
| 172.16.80.21 | Windows 10 |  RDP  |  testrdp01   |  random pass  |     Users    |              |             |
| 172.16.80.23 |   MySQL 5  | MySQL |     root     |  Test2020.M   |              |              |             |

!!! note "点击页面左侧的 `资产管理` - `系统用户` - `创建普通用户` 创建对应协议系统用户"

=== "SSH 协议系统用户"

    | 名称        | 协议 | 用户名     | 认证方式 | 自动生成          | 自动推送          | Sudo | Shell     | SFTP根路径 |
    | ---------- | ---- | --------- | -------- | ---------------- | ---------------- | ---- | --------- | ---------- |
    | test_ssh01 | SSH  | testssh01 | 托管密码 | :material-check: | :material-check: | ALL  | /bin/bash | /tmp       |


=== "RDP 协议系统用户"

    | 名称        | 协议 | 用户名     | 认证方式 | 自动生成          | AD域名 | 自动推送          | 用户附属组 |
    | ---------- | ---- | --------- | ------- | ---------------- | ------ | ---------------- | --------- |
    | test_rdp01 | RDP  | testrdp01 | 托管密码 | :material-check: |        | :material-check: | Users     |

=== "MySQL 应用系统用户"

    | 名称              | 用户名 | 协议  | 认证方式 | 密码       | 命令过滤器 |
    | ----------------- | ------ | ----- | ------- | ---------- | --------- |
    | test_mysql01_root | root   | MySQL | 托管密码 | Test2020.M |           |

!!! warning "注意"
    - 在 `Jumpserver` 中，需要对资产不同的用途创建不同的 `系统用户`  
    - 我们针对不同的用途创建不同的 `系统用户`，`Linux` 通过 `Sudo` 来控制用户的权限，`Windows` 通过组来控制用户权限


## 4 创建授权规则

### 4.1 为用户分配资产

=== "授权已存在的系统用户"

    |      IP      |   Assets   |  System User               |       User      |
    | ------------ | ---------- | -------------------------- | --------------- |
    | 172.16.80.11 |  Centos 7  | 172.16.80.11_root          |      admin      |
    | 172.16.80.21 | Windows 10 | 172.16.80.21_administrator |      admin      |

    !!! note "点击页面左侧的 `授权管理` - `资产授权` - `创建授权规则` 创建两个授权"

    | 名称             | 用户                 | 用户组 | 资产                     | 节点 | 系统用户                                  | 权限                  |
    | ---------------- | -------------------- | ----- | ------------------------ | --- | ----------------------------------------- | -------------------- |
    | admin_ssh01_授权 | Administrator(admin) |       | test_ssh01(172.16.80.11) |     | 172.16.80.11_root(root)                   | :material-check: 全部 |
    | admin_rdp01_授权 | Administrator(admin) |       | test_rdp01(172.16.80.21) |     | 172.16.80.21_administrator(administrator) | :material-check: 全部 |

=== "推送系统用户到资产"

    |      IP      |   Assets   |  System User      |       User      |
    | ------------ | ---------- | ----------------- | --------------- |
    | 172.16.80.11 |  Centos 7  | test_ssh01        |      admin      |
    | 172.16.80.21 | Windows 10 | test_rdp01        |      admin      |

    !!! note "点击页面左侧的 `授权管理` - `资产授权` - `创建授权规则` 创建两个授权"

    | 名称                | 用户                 | 用户组 | 资产                     | 节点 | 系统用户                          | 权限                  |
    | ------------------ | -------------------- | ----- | ------------------------ | --- | --------------------------------- | -------------------- |
    | test_ssh01_推送测试 | Administrator(admin) |       | test_ssh01(172.16.80.11) |     | test_ssh01_测试系统用户(testssh01) | :material-check: 全部 |
    | test_rdp01_推送测试 | Administrator(admin) |       | test_rdp01(172.16.80.21) |     | test_rdp01_测试系统用户(testrdp01) | :material-check: 全部 |

### 4.2 为用户分配数据库应用

!!! note "点击页面左侧的 `授权管理` - `数据库应用` - `创建授权规则`  创建数据库授权"

|      IP      | applications |  System User               |       User      |
| ------------ | ------------ | -------------------------- | --------------- |
| 172.16.80.31 |  MySQL 5     | test_mysql01_root          |      admin      |

| 名称               | 用户                 | 用户组 | 数据库应用           | 节点 | 系统用户                |
| ------------------ | -------------------- | ----- | ------------------ | --- | ----------------------- |
| admin_mysql01_授权 | Administrator(admin) |       | test_mysql01(MySQL) |     | test_mysql01_root(root) |

!!! warning "注意"
    - `名称`，授权的名称，不能重复  
    - `用户` 和 `用户组` 二选一，不推荐即选择 `用户` 又选择 `用户组`  
    - `资产` 和 `节点` 二选一，选择 `节点` 会包含 `节点` 下面的所有 `资产`  
    - `系统用户`，`系统用户` 为连接资产的 `认证凭据`  
    - `用户(组)`，`资产(节点)`，`系统用户` 是一对一的关系，所以当拥有 `Linux`、`Windows` 不同类型资产时，应该分别给 `Linux` 资产和 `Windows` 资产创建 `授权规则`  
    - 一般情况下，`资产` 授权给 `用户`，`节点` 授权给 `用户组`，一个 `授权` 只能选择一个 `系统用户`


## 5 用户登录

!!! note "点击页面右上角的 `Web终端` 进行资产连接"

!!! warning "注意"
    用户只能看到自己被管理员授权了的 `资产`，如果登录后无资产，请联系管理员进行确认

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
[Redis 数据库纳管]: https://kb.fit2cloud.com/?p=179
[纳管数据库应用]: https://kb.fit2cloud.com/?p=79





