# Linux SSH 资产要求

!!! tip "资产要求"
    - 资产必须部署 openssh-server。
    - 防火墙 ssh 端口必须开放给 JumpServer 所有服务器访问。
    - 请检查 `/etc/hosts.allow` `/etc/hosts.deny` `/etc/ssh/sshd_config` 是否有登录限制。
    - 资产连接超时 timeout 请检查 `/etc/ssh/sshd_config` 的 `USEDNS` 项是否为 `no`。
    ```vim
    UseDNS no
    ```
