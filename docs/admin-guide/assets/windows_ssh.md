# Windows SSH 资产要求

!!! info "Windows 资产测试连接, 获取硬件, 自动推送需要进行相关设置"
    注意: 按照下面的文档部署好 openssh 后, 在 web 的资产列表里面找到你的 windows 资产, 在协议组里面加入 rdp 3389, 再添加一个 ssh 22, 然后就可以使用 测试连接, 获取硬件, 自动推送 功能了

!!! tip "Win7/Win2008 需要升级 `powershell` 到 3.0 以上, 详情请参考 [ansible 客户端需求](https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html)"

!!! tip ""
    [下载最新的 OpenSSH](https://github.com/PowerShell/Win32-OpenSSH/releases/latest)  
    解压后，重命名到 C:\Program Files\OpenSSH  
    通过管理员身份的方式打开 powershell , 并在 powershell 里面执行下面命令

### 1. 安装 OpenSSH

!!! tip ""
    ```powershell
    cd "C:\Program Files\OpenSSH"
    powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1
    ```

### 2. 设置 Firewalld

!!! tip ""
    ```powershell
    New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
    ```

!!! question ""
    ```powershell
    # 如果 win7/win2008 执行上面的命令报错请执行此处的命令
    netsh advfirewall firewall add rule name=sshd dir=in action=allow protocol=TCP localport=22
    ```

### 3. 启动 OpenSSH

!!! tip ""
    ```powershell
    net start sshd
    Set-Service sshd -StartupType Automatic
    ```

### 4. 使用 Private Key

!!! tip ""
    - [Setup public key based authentication for windows](https://github.com/PowerShell/Win32-OpenSSH/wiki/Setup-public-key-based-authentication-for-windows)

    ```powershell
    ssh-keygen.exe -t rsa
    cp $env:USERPROFILE\.ssh\id_rsa.pub $env:USERPROFILE\.ssh\authorized_keys
    ```
    ```powershell
    notepad C:\ProgramData\ssh\sshd_config
    ```
    ```vim hl_lines="88-89"
    # This is the sshd server system-wide configuration file.  See
    # sshd_config(5) for more information.

    # The strategy used for options in the default sshd_config shipped with
    # OpenSSH is to specify options with their default value where
    # possible, but leave them commented.  Uncommented options override the
    # default value.

    #Port 22
    #AddressFamily any
    #ListenAddress 0.0.0.0
    #ListenAddress ::

    #HostKey __PROGRAMDATA__/ssh/ssh_host_rsa_key
    #HostKey __PROGRAMDATA__/ssh/ssh_host_dsa_key
    #HostKey __PROGRAMDATA__/ssh/ssh_host_ecdsa_key
    #HostKey __PROGRAMDATA__/ssh/ssh_host_ed25519_key

    # Ciphers and keying
    #RekeyLimit default none

    # Logging
    #SyslogFacility AUTH
    #LogLevel INFO

    # Authentication:

    #LoginGraceTime 2m
    #PermitRootLogin prohibit-password
    #StrictModes yes
    #MaxAuthTries 6
    #MaxSessions 10

    PubkeyAuthentication yes

    # The default is to check both .ssh/authorized_keys and .ssh/authorized_keys2
    # but this is overridden so installations will only check .ssh/authorized_keys
    AuthorizedKeysFile	.ssh/authorized_keys

    #AuthorizedPrincipalsFile none

    # For this to work you will also need host keys in %programData%/ssh/ssh_known_hosts
    #HostbasedAuthentication no
    # Change to yes if you don't trust ~/.ssh/known_hosts for
    # HostbasedAuthentication
    #IgnoreUserKnownHosts no
    # Don't read the user's ~/.rhosts and ~/.shosts files
    #IgnoreRhosts yes

    # To disable tunneled clear text passwords, change to no here!
    #PasswordAuthentication yes
    #PermitEmptyPasswords no

    # GSSAPI options
    #GSSAPIAuthentication no

    #AllowAgentForwarding yes
    #AllowTcpForwarding yes
    #GatewayPorts no
    #PermitTTY yes
    #PrintMotd yes
    #PrintLastLog yes
    #TCPKeepAlive yes
    #UseLogin no
    #PermitUserEnvironment no
    #ClientAliveInterval 0
    #ClientAliveCountMax 3
    #UseDNS no
    #PidFile /var/run/sshd.pid
    #MaxStartups 10:30:100
    #PermitTunnel no
    #ChrootDirectory none
    #VersionAddendum none

    # no default banner path
    #Banner none

    # override default of no subsystems
    Subsystem	sftp	sftp-server.exe

    # Example of overriding settings on a per-user basis
    #Match User anoncvs
    #	AllowTcpForwarding no
    #	PermitTTY no
    #	ForceCommand cvs server

    # 注释下面两行
    #Match Group administrators
    #       AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
    ```
    ```powershell
    net stop sshd
    net start sshd
    ```

!!! info "Private Key 使用方式"
    ```powershell
    ssh user@ip -i <private_key_absolute_path>        (local users)
    ssh user@domain@ip -i <private_key_absolute_path> (Domain users)
    ```
