Windows SSH 设置说明
------------------------------

Windows 资产测试连接, 获取硬件, 自动推送需要进行相关设置

.. code-block:: shell

    # 登陆你的 windows 资产

    # 根据 https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html#windows-ssh-setup 教程
    # 到 https://github.com/PowerShell/Win32-OpenSSH/releases/latest 下载最新的 OpenSSH
    # 解压后，重命名到 C:\Program Files\OpenSSH

    # 通过管理员身份的方式打开 powershell , 并在 powershell 里面执行下面命令
    cd "C:\Program Files\OpenSSH"

    # 安装 OpenSSH
    powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1

    # 设置防火墙
    New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

    # 如果 New-NetFirewallRule 抱错, 就使用下面这条开启防火墙, 上面不报错跳过这条
    netsh advfirewall firewall add rule name=sshd dir=in action=allow protocol=TCP localport=22

    # 启动 OpenSSH
    net start sshd

    # 设置 OpenSSH 自启
    Set-Service sshd -StartupType Automatic


回到 Web 添加 Windows 资产

.. code-block:: vim

    "IP" 填写你 Windows 资产的 IP 地址
    "系统平台" 注意下, Windows 10/2012/2016/2019 选择 Windows(2016), 其他的选择 Windows 即可
    "协议组" 添加 RDP 的端口之外, 还要添加一个 SSH 端口, ssh 端口用来进行资产可连接测试、硬件获取、推送系统用户等 Ansible 任务
    "管理用户" 需要创建一个资产上面已经存在的 Administrators 组里面的用户, 也就是管理员身份的用户

创建 系统用户(推送, 通过 管理用户 自动在资产上面新建一个用户 )

.. code-block:: vim

    "名称" 就是 Windows 资产上面用户的 全名
    "登陆模式" 选择 自动登陆
    "用户名" 就是 Windows 资产上面用户的 名称
    "协议" 选择 RDP
    "自动生成密钥" 默认勾选
    "自动推送" 默认勾选

或者你可以使用资产上面已经存在的用户进行登陆

.. code-block:: vim

    "名称" 标识, 你可以随便起一个, 具有唯一性
    "登陆方式" 选择 自动登陆
    "用户名" 就是 Windows 资产上面已经创建好的用户的 名称 (如: administrator 或者 guest 等)
    "自动生成密钥" 不要勾选
    "自动推送" 不要勾选
    "密码" 就是上面用户的 密码 (比如上面的用户名是 administrator, 这里就输入 administrator 的密码)

或者你希望用户自己输入密码( 资产加域或者用户知道资产用户的情况下推荐使用 )

.. code-block:: vim

    "名称" 标识, 你可以随便起一个, 具有唯一性
    "登陆方式" 选择 手动登陆
    "用户名" 如果你知道用户登陆的用户名可以输入, 否则可以直接留空

然后授权即可
