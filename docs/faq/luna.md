# Luna 常见问题

!!! question "luna 页面访问异常"
    请不要通过 8080 端口访问 jumpserver, 通过 nginx 代理端口进行访问  
    如果下载了 luna 源代码, 请先编译好, 并在 nginx 里把 luna 目录指向编译好的目录  
    如果组件都已经启动, 但是访问提示 502 或者 403, 可以检查下 防火墙 和 selinux

!!! question "访问 rdp vnc 资产白屏"
    根据 faq guacamole 文档第一条, 重新部署 guacamole  
    确定 `web` - `会话管理` - `终端管理` 里面的组件都 `在线`, 在线图标处于 `绿色` 状态

!!! question "访问 rdp vnc 资产提示无权限"
    根据 faq guacamole 文档第一条, 重新部署 guacamole  
    确定 `web` - `会话管理` - `终端管理` 里面的组件都 `在线`, 在线图标处于 `绿色` 状态

!!! question "访问 ssh telnet 资产无反应"
    只有一个白色光标, 无任何其他提示, 根据 faq koko 文档第一条, 重新部署 koko  
    确定 `web` - `会话管理` - `终端管理` 里面的组件都 `在线`, 在线图标处于 `绿色` 状态

!!! question "访问 ssh 资产错误"
    `unable to authenticate, attempted methods [none]` 表示资产上面不存在此用户   
    `unable to authenticate, attempted methods [none password]` 表示系统用户的密码错误  
    `unable to authenticate, attempted methods [password publickey none]` 表示系统用户的密码和key都错误  

    以上三种错误都是系统用户不正确, 可以到 `资产列表` - `系统用户` - `系统用户详情` 里面进行推送或者修改

!!! question "error: dial tcp x.x.x.x: i/o timeout"
    访问资产超时, 检查资产的 ssh 设置 `USEDNS` 是否已经关闭, 自行检查网络和防火墙

!!! question "无法连接服务器, 请联系管理员"
    rdp 协议资产出现此问题请认真看管理文档的[Windows RDP 资产要求](../admin-guide/assets/windows_rdp.md)

!!! question "No asset id or system user id found"
    此问题一般是 `授权` 不当导致, 比如一个 `授权` 里面存着多个不同 `协议` 的 `系统用户  `
    或者 `系统用户` 的 `协议` 与 `资产` `协议` 不匹配  
    或者 `授权` 里面不存在 `系统用户`（一般会提示 该主机没有授权系统用户）

!!! question "You don't have permission login"
    未授权资产连接权限（`授权规则` - `资产授权` 里面的 `动作` 勾上 `连接` 选项即可）
