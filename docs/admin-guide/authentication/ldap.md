# LDAP 认证

!!! tip "LDAP 支持 使用 LADP 与 Windows AD 的用户作为 JumpServer 登录用户"

=== "LDAP"

    |             |                                                   |
    | :---------- | :------------------------------------------------ |
    | LDAP地址    | ldap://serverurl:389                               |
    | 绑定DN      | administrator@jumpserver.org                       |
    | 密码        | ********                                           |
    | 用户OU      | ou=jumpserver,dc=jumpserver,dc=org                 |
    | 用户过滤器   | (cn=%(user)s)                                     |
    | LADP属性映射 | {"username": "cn", "name": "sn", "email": "mail"} |
    | 启动LDAP认证 | ☑️                                                 |

=== "LDAPS"

    - ldap ssl 证书需要放到持久化目录 `jumpserver/core/data/certs/ldap_ca.pem`

    |             |                                                   |
    | :---------- | :------------------------------------------------ |
    | LDAP地址    | ldaps://serverurl:636                              |
    | 绑定DN      | administrator@jumpserver.org                       |
    | 密码        | ********                                           |
    | 用户OU      | ou=jumpserver,dc=jumpserver,dc=org                 |
    | 用户过滤器   | (cn=%(user)s)                                     |
    | LADP属性映射 | {"username": "cn", "name": "sn", "email": "mail"} |
    | 启动LDAP认证 | ☑️                                                 |

!!! tip "选项说明"
    `DN` 一定要是完整的DN，不能跳过OU，可以使用其他工具查询  
    `cn=admin,ou=aaa,dc=jumpserver,dc=org` 或者用 `user@domain.com` 形式

    `用户OU` 用户OU可以只写顶层OU，不写子OU  
    `ou=aaa,ou=bbb,ou=ccc,dc=jumpserver,dc=org`，可以只写 `ou=ccc,dc=jumpserver,dc=org`

    `用户过滤器` 根据规则到 `用户OU` 里面去检索用户，支持 memberof  
    `(uid=%(user)s)` 或 `(sAMAccountName=%(user)s)`

    `LADP属性映射` username name email 这三项不可修改删除  
    `{"username": "uid", "name": "sn", "email": "mail"}` 或 `{"username": "sAMAccountName", "name": "cn", "email": "mail"}`

    注意: 用户过滤器用什么筛选，LDAP属性映射字段要与其一致，过滤器用 uid，LDAP属性映射也要用 uid


!!! tip "LDAP 的部分功能在 jumpserver/config/config.txt 进行设置"
    ```vim
    # LDAP/AD settings
    # LDAP 搜索分页数量
    AUTH_LDAP_SEARCH_PAGED_SIZE=1000
    #
    # 定时同步用户
    # 启用 / 禁用
    AUTH_LDAP_SYNC_IS_PERIODIC=True
    # 同步间隔 (单位: 时) (优先）
    AUTH_LDAP_SYNC_INTERVAL=12
    # Crontab 表达式
    AUTH_LDAP_SYNC_CRONTAB=* 6 * * *
    #
    # LDAP 用户登录时仅允许在用户列表中的用户执行 LDAP Server 认证
    AUTH_LDAP_USER_LOGIN_ONLY_IN_USERS=False
    #
    # LDAP 认证时如果日志中出现以下信息将参数设置为 0 (详情参见：https://www.python-ldap.org/en/latest/faq.html)
    # In order to perform this operation a successful bind must be completed on the connection
    AUTH_LDAP_OPTIONS_OPT_REFERRALS=-1
    ```
