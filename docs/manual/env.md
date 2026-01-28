# 参数说明

!!! warning "注意"
    - 修改配置文件前请先关闭 JumpServer 服务。

## 1 Core 参数说明
!!! tip ""
    - 打开 config.txt 配置文件。

    ```sh
    vi /opt/jumpserver/config/config.txt
    ```

!!! tip ""
    - Core 参数如下：

|  参数名称   | 默认值  | 可选项  | 说明  |
|  :-----  | :-----  |  :-----  | :-----  |
| SECRET_KEY  | '' | - | 用于对敏感字段进行加解密的 Key |
| BOOTSTRAP_TOKEN | '' | - | 用于组件向 Core 服务注册使用的 Token |
| DEBUG  | false | true <br> false | Debug 模式，如果开启页面请求 API 报错时会显示更多信息 |
| DEBUG_DEV  | false | true <br> false | Debug 开发模式，如果开启后端日志会显示更多信息 |
| LOG_LEVEL | DEBUG | DEBUG <br> INFO <br> WARNING <br> ERROR <br> CRITICAL | 日志级别 |
| LOG_DIR | /data/jumpserver/core/logs | - | 日志目录 |
| DB_ENGINE | mysql | - | 数据库引擎 |
| DB_NAME | jumpserver | - | 数据库名 |
| DB_HOST | 127.0.0.1 | - | 数据库地址 |
| DB_PORT | 3306 | - | 数据库端口	 |
| DB_USER| root | - | 数据库用户 |
| DB_PASSWORD | '' | - | 数据库用户密码 |
| DB_USE_SSL | false | true <br> false | 数据库启用 SSL 方式 |
| REDIS_HOST | 127.0.0.1 | - | Reids 地址 |
| REDIS_PORT | 6379 | - | Redis 端口 |
| REDIS_PASSWORD | '' | - | Redis 密码 |
| REDIS_USE_SSL | false | true <br> false | Redis 启用 SSL 方式 |
| REDIS_SSL_KEY | null | - | Redis SSL Key |
| REDIS_SSL_CERT | null | - | Redis SSL Cert 证书 |
| REDIS_SSL_CA | null | - | Redis SSL CA Cert 证书 |
| REDIS_SSL_REQUIRED | null | - | Redis SSL 证书是否必须 |
| REDIS_MAX_CONNECTIONS | 100 | - | Redis最大连接数 |
| REDIS_SENTINEL_HOSTS | '' | - | Redis 哨兵地址（多个地址使用 / 分割） |
| REDIS_SENTINEL_PASSWORD | '' | - | Redis 哨兵密码 |
| REDIS_SENTINEL_SOCKET_TIMEOUT | null | - | Redis 哨兵 Socket 超时时间 |
| REDIS_DB_CELERY | 3 | 0-15 | Redis 库编号，Celery 任务使用 |
| REDIS_DB_CACHE | 4 | 0-15 | Redis 库编号，缓存使用 |
| REDIS_DB_SESSION | 5 | 0-15 | Redis 库编号，用户 Session 使用 |
| REDIS_DB_WS | 6 | - | Redis 库编号，WebSocket 使用 |
| TOKEN_EXPIRATION | 3600 * 24（s） | - | 通过 API 创建用户 Token 的有效期 <br> # 如果配置为空或者0，则默认值为 3600 |
| DEFAULT_EXPIRED_YEARS | 70（year） | - | 创建资源的默认过期年份，比如：授权规则 <br> # 不允许修改 | 
| SESSION_COOKIE_DOMAIN | null | - | 用户 Session Cookie 域，比如：fit2cloud.com |
| CSRF_COOKIE_DOMAIN | null | - | 用户 CSRF Cookie 域，默认与 SESSION_COOKIE_DOMAIN 保持一致 |
| SESSION_COOKIE_NAME_PREFIX | null | - | 用户设置 Session Cookie 的名称前缀 |
| SESSION_COOKIE_AGE | 3600 * 24（s） | - | 用户 Session Cookie 的有效期 |
| SESSION_EXPIRE_AT_BROWSER_CLOSE | false | true <br> false | 用户 Session 在浏览器关闭后过期 |
| CONNECTION_TOKEN_ONETIME_EXPIRATION | 5 * 60 | >= 5 * 60 | 有效期内 ConnectionToken 只能使用一次	 |
| CONNECTION_TOKEN_REUSABLE_EXPIRATION | 3600 * 24 * 30（s） | - | 有效期内 ConnectionToken 可以多次使用 |
| CONNECTION_TOKEN_REUSABLE | false | true <br> false | ConnectionToken 是否可以多次使用 |
| AUTH_CUSTOM | false | true <br> false | 开启自定义用户认证 |
| AUTH_CUSTOM_FILE_MD5 | '' | - | 自定义用户认证的文件 md5 值 |
| MFA_CUSTOM | false | true <br> false | 开启自定义 MFA 认证 |
| MFA_CUSTOM_FILE_MD5 | '' | - | 自定义 MFA 认证的文件 md5 值 |
| AUTH_TEMP_TOKEN | false | true <br> false | 开启临时密码功能 |
| AUTH_SSO |false | true <br> false | 启用 SSO 认证 |
| AUTH_SSO_AUTHKEY_TTL | 60 * 15(s) | SSO 认证密钥 TTL |
| LOGIN_REDIRECT_TO_BACKEND | '' | Direct（直接进入内部登录页面） <br> OpenID <br> CAS <br> SAML2 <br> OAuth2 的服务提供商名称（系统设置） | 开启第三方认证后，不出现倒计时跳转页面直接跳转到认证服务，比如：OpenID |
| LOGIN_REDIRECT_MSG_ENABLED | true | true <br> false | 开启第三方跳转倒计时页面 |
| SYSLOG_ADDR | '' | - | SysLog 服务地址 |
| SYSLOG_FACILITY | user | - | SysLog FACILITY |
| SYSLOG_SOCKTYPE | 2 | - | SysLog SockType |
| PERM_EXPIRED_CHECK_PERIODIC | 60 * 60（s） | - | 校验过期的资产授权规则并过期用户授权树的周期 |
| LANGUAGE_CODE | en | zh <br> en <br> ja | 语言 |
| TIME_ZONE | Asia/Shanghai | - | 时区 |
| SESSION_COOKIE_SECURE | false | true <br> false | 用户 Session Cookie 安全模式，开启后只允许在 https 协议下发送 |
| DOMAINS |	'' | -| 指定JumpServer应用程序允许的域名 |
| CSRF_COOKIE_SECURE | false | true <br> false | 用户 CSRF Token 安全模式，开启后只允许在 https 协议下发送 |
| REFERER_CHECK_ENABLED | false | true <br> false | 是否开启 REFERER 校验 |
| CSRF_TRUSTED_ORIGINS | - | - | CSRF 同源信任，多个地址使用 `,` 分割 |
| SESSION_ENGINE | cache | - | 用户 Session 引擎 |
| SESSION_SAVE_EVERY_REQUEST | true | true <br> false | 每个请求都要保存用户 Session |
| SESSION_EXPIRE_AT_BROWSER_CLOSE_FORCE | false | true <br> false | 浏览器关闭后强制过期用户 Session 会话 |
| SERVER_REPLAY_STORAGE | {} | - | 服务端录像存储 <br> 比如：<br> {<br>    'TYPE': 's3',<br>    'BUCKET': '',<br>    'ACCESS_KEY': '',<br>    'SECRET_KEY': '',<br>    'ENDPOINT': ''<br>}  <br> # 组件上传录像到 Core 服务，Core 自动上传到配置的对象存储服务 |
| CHANGE_AUTH_PLAN_SECURE_MODE_ENABLED | true | true <br> false | 改密计划安全模式 <br> 启用后，不支持用户自己改自己； <br> 禁用后，支持自己改自己； <br> 比如 root 改 root |
| SECURITY_VIEW_AUTH_NEED_MFA | true | true <br> false | 需要校验 MFA |
| SECURITY_DATA_CRYPTO_ALGO | null | - | 数据加密算法 |
| GMSSL_ENABLED | false | true <br> false | 开启国密算法（数据加密算法） <br> SECURITY_DATA_CRYPTO_ALGO <br> GMSSL_ENABLED <br> # 如果同时配置，优先使用 SECURITY_DATA_CRYPTO_ALGO |
| OPERATE_LOG_ELASTICSEARCH_CONFIG | {} | - | 操作日志“变更字段”的存储 ES 配置 <br>比如：<br>{<br>    "INDEX": "",<br>    "HOSTS": "",<br>    "OTHER": "",<br>    "IGNORE_VERIFY_CERTS": "",<br>    "INDEX_BY_DATE": "",<br>    "DOC_TYPE": ""<br>} |
| MAGNUS_ORACLE_PORTS | 30000-30030 | - | Magnus 组件需要监听的 Oracle 端口范围 |
| APPLET_DOWNLOAD_HOST | '' | - | Applet 等软件的下载地址 |
| FTP_FILE_MAX_STORE | 0 | - |  FTP 文件上传下载备份阈值，单位(M)，当值<=0时，不备份文件 |
| MAX_LIMIT_PER_PAGE | 10000	| - | 设置允许的最大导出记录数 |
| FILE_UPLOAD_SIZE_LIMIT_MB	| 200 | - | 设置文件上传的最大大小限制（单位：MB） |
| THROTTLE_RATES_ANON | 60/min | string | 未登录用户访问限流 |
| THROTTLE_RATES_USER | 180/min	| string | 用户访问限流 |
| THROTTLE_RATES_SERVICE_ACCOUNT | 300/min | string | 组件账号访问限流 |