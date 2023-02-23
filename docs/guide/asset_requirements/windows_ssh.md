# Windows SSH 资产要求

!!! info "Windows 资产的测试连接、硬件信息获取、用户自动推送功能需要进行以下相关设置"
    注意：按照下面的文档部署好 Openssh 后，在 Web 的资产列表里面找到您的 Windows 资产，在协议组中加入 rdp 3389和 ssh 22协议，然后就可以使用资产测试连接、硬件信息获取、用户自动推送的功能。

!!! tip "Win7/Win2008 需要升级 `powershell` 到 3.0 以上，详情请参考 [ansible 客户端需求](https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html){:target="_blank"}"

## 1 安装 OpenSSH

!!! tip ""
    [下载最新的 OpenSSH-Win64.msi](https://github.com/PowerShell/Win32-OpenSSH/releases/latest){:target="_blank"}  
    - 通过管理员身份的直接运行即可，安装过程无需交互，安装完成后不需要任何配置即可直接使用。


## 2 使用 Private Key

!!! tip ""
    - [Setup public key based authentication for windows](https://github.com/PowerShell/Win32-OpenSSH/wiki/Setup-public-key-based-authentication-for-windows){:target="_blank"}

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

## 3 Private Key 使用方式
!!! tip ""
    ```powershell
    ssh user@ip -i <private_key_absolute_path>        (local users)
    ssh user@domain@ip -i <private_key_absolute_path> (Domain users)
    ```
