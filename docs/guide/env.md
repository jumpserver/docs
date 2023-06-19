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
| REDIS_SSL_REQUIRED | 'none' | - | Redis SSL 证书是否必须 |
| REDIS_SENTINEL_HOSTS | '' | - | Redis 哨兵地址（多个地址使用 / 分割） |
| REDIS_SENTINEL_PASSWORD | '' | - | Redis 哨兵密码 |
| REDIS_SENTINEL_SOCKET_TIMEOUT | '' | - | Redis 哨兵 Socket 超时时间 |
| REDIS_DB_CELERY | 3 | 0-15	| Redis 库编号，Celery 任务使用 |
| REDIS_DB_CACHE | 4 | 0-15 | Redis 库编号，缓存使用 |
| REDIS_DB_SESSION | 5 | 0-15 | Redis 库编号，用户 Session 使用 |
| REDIS_DB_WS | 6 | - | Redis 库编号，WebSocket 使用 |
| TOKEN_EXPIRATION | 3600 * 24（s） | - | 通过 API 创建用户 Token 的有效期 <br> # 如果配置为空或者0，则默认值为 3600 |
| DEFAULT_EXPIRED_YEARS | 70（year） | - | 创建资源的默认过期年份，比如：授权规则 <br> # 不允许修改 |
| SESSION_COOKIE_DOMAIN | null | - | 用户 Session Cookie 域，比如：fit2cloud.com |
| CSRF_COOKIE_DOMAIN | null | - | 用户 CSRF Cookie 域，默认与 SESSION_COOKIE_DOMAIN 保持一致 |
| SESSION_COOKIE_NAME_PREFIX | jms_ | - | 用户 Session Cookie 名称的前缀 <br> # 如果配置了 SESSION_COOKIE_DOMAIN 参数，会使用 `.` 前的值作为默认值，比如：fit2cloud |
| SESSION_COOKIE_AGE | 3600 * 24（s） | - | 用户 Session Cookie 的有效期 |
| SESSION_EXPIRE_AT_BROWSER_CLOSE | false | true <br> false | 用户 Session 在浏览器关闭后过期 |
| CONNECTION_TOKEN_EXPIRATION | 5 * 60 | >= 5 * 60 | 有效期内 ConnectionToken 只能使用一次	 |
| CONNECTION_TOKEN_EXPIRATION_MAX | 3600 * 24 * 30（s） | - | 有效期内 ConnectionToken 可以多次使用 |
| CONNECTION_TOKEN_REUSABLE | false | true <br> false | ConnectionToken 是否可以多次使用 |
| AUTH_CUSTOM | false | true <br> false | 开启自定义用户认证 |
| AUTH_CUSTOM_FILE_MD5 | '' | - | 自定义用户认证的文件 md5 值 |
| MFA_CUSTOM | false | true <br> false | 开启自定义 MFA 认证 |
| MFA_CUSTOM_FILE_MD5 | '' | - | 自定义 MFA 认证的文件 md5 值 |
| AUTH_TEMP_TOKEN | false | true <br> false | 开启临时密码功能 |
| LOGIN_REDIRECT_TO_BACKEND | '' | Direct（直接进入内部登录页面） <br> OpenID <br> CAS <br> SAML2 <br> OAuth2 的服务提供商名称（系统设置） | 开启第三方认证后，不出现倒计时跳转页面直接跳转到认证服务，比如：OpenID |
| LOGIN_REDIRECT_MSG_ENABLED | true | true <br> false | 开启第三方跳转倒计时页面 |
| SYSLOG_ADDR | '' | - | SysLog 服务地址 |
| SYSLOG_FACILITY | user | - | SysLog FACILITY |
| SYSLOG_SOCKTYPE | 2 | - | SysLog SockType |
| PERM_EXPIRED_CHECK_PERIODIC | 60 * 60（s） | - | 校验过期的资产授权规则并过期用户授权树的周期 |
| LANGUAGE_CODE | zh | zh <br> en <br> ja | 语言 |
| TIME_ZONE | Asia/Shanghai | - | 时区 |
| SESSION_COOKIE_SECURE | false | true <br> false | 用户 Session Cookie 安全模式，开启后只允许在 https 协议下发送 |
| CSRF_COOKIE_SECURE | false | true <br> false | 用户 CSRF Token 安全模式，开启后只允许在 https 协议下发送 |
| REFERER_CHECK_ENABLED | false | true <br> false | 开启 REFERER 校验 |
| CSRF_TRUSTED_ORIGINS | - | - | CSRF 同源信任，多个地址使用 `,` 分割 |
| SESSION_ENGINE | cache | - | 用户 Session 引擎 |
| SESSION_SAVE_EVERY_REQUEST | true | true <br> false | 每个请求都要保存用户 Session |
| SESSION_EXPIRE_AT_BROWSER_CLOSE_FORCE | false | true <br> false | 浏览器关闭后强制过期用户 Session 会话 |
| SERVER_REPLAY_STORAGE | {} | - | 服务端录像存储 <br> 比如：<br> {<br>    'TYPE': 's3',<br>    'BUCKET': '',<br>    'ACCESS_KEY': '',<br>    'SECRET_KEY': '',<br>    'ENDPOINT': ''<br>}  <br> # 组件上传录像到 Core 服务，Core 自动上传到配置的对象存储服务 |
| CHANGE_AUTH_PLAN_SECURE_MODE_ENABLED | true | true <br> false | 改密计划安全模式 <br> 启用后，不支持用户自己改自己； <br> 禁用后，支持自己改自己； <br> 比如 root 改 root |
| SECURITY_VIEW_AUTH_NEED_MFA | true | true <br> false | 需要校验 MFA |
| SECURITY_DATA_CRYPTO_ALGO | aes（GMSSL_ENABLED=false） <br> gm（GMSSL_ENABLED=true） | aes_ecb <br> aes_gcm <br> aes <br> gm_sm4_ecb <br> gm | 数据加密算法 |
| GMSSL_ENABLED | false | true <br> false | 开启国密算法（数据加密算法） <br> SECURITY_DATA_CRYPTO_ALGO <br> GMSSL_ENABLED <br> # 如果同时配置，优先使用 SECURITY_DATA_CRYPTO_ALGO |
| OPERATE_LOG_ELASTICSEARCH_CONFIG | {} | - | 操作日志“变更字段”的存储ES配置 <br>比如：<br>{<br>    "INDEX": "",<br>    "HOSTS": "",<br>    "OTHER": "",<br>    "IGNORE_VERIFY_CERTS": "",<br>    "INDEX_BY_DATE": "",<br>    "DOC_TYPE": ""<br>} |
| MAGNUS_ORACLE_PORTS | 30000-30030 | - | Magnus 组件需要监听的 Oracle 端口范围 |
| APPLET_DOWNLOAD_HOST | '' | - | Applet 等软件的下载地址 |
| FTP_FILE_MAX_STORE | 100（M） | - |  FTP 文件上传下载备份阈值，单位(M)，当值<=0时，不备份文件 |

## 2 KoKo 参数说明
!!! tip ""
    - KoKo 参数如下：

|  参数名称   | 默认值  | 可选项  | 说明  |
|  :-----  | :-----  |  :-----  | :-----  |
| NAME | hostname | - | 主机名 |
| CORE_HOST | http://127.0.0.1:8080 | - | Jumpserver 项目的 Url，API 请求注册会使用 |
| BOOTSTRAP_TOKEN | '' | - | 预共享秘钥，请和JumpServer 配置文件中保持一致	 |
| BIND_HOST | 0.0.0.0 | - | 启动时绑定的IP |
| SSHD_PORT	 | 2222 | - | 监听的SSH端口号 |
| HTTPD_PORT | 5000 | - | 监听的HTTP/WS端口号 |
| ACCESS_KEY | '' | - | 项目使用的ACCESS KEY, 默认会注册,并保存到文件 |
| ACCESS_KEY_FILE | data/keys/.access_key | - | ACCESS KEY 保存的地址, 默认注册后会保存到该文件中 |
| LOG_LEVEL | DEBUG | DEBUG <br> INFO <br> WARNING <br> ERROR <br> CRITICAL | 日志级别 |
| SSH_TIMEOUT | 15 | - | SSH 连接超时时间(单位=秒) <br> # 如果用户服务器启用了 useDNS 这些参数，有可能登录时间超过 15S，需要修改此参数 |
| LANGUAGE_CODE | zh | zh <br> en <br> ja | 语言 |
| UPLOAD_FAILED_REPLAY_ON_START | true | true <br> false | 未上传录像遗留文件，启动时是否上传 |
| SFTP_SHOW_HIDDEN_FILE | false | true <br> false | SFTP 是否显示隐藏文件 |
| REUSE_CONNECTION | true | true <br> false | 是否复用同一用户的 SSH 连接 |
| ASSET_LOAD_POLICY | all | - | all 则用户资产缓存本地搜索分页；默认异步加载资产, 异步搜索分页 |
| ZIP_MAX_SIZE | 1024M | - | Web Sftp 文件下载，zip 支持压缩的最大额度 (单位=M) |
| ZIP_TMP_PATH | /tmp | - | Web Sftp 文件下载，zip压缩文件存放的临时目录 |
| CLIENT_ALIVE_INTERVAL | 30 | 30 <br> 0 | 用户 SSH 登录 KoKo 之后，KoKo 给 SSH Client 发送的心跳间隔，默认为30，0则表示不发送，保持登录用户连接不断开 |
| RETRY_ALIVE_COUNT_MAX | 3 | - | 登录资产之后，KoKo 向资产发送心跳包出现错误的重试次数，默认为3。 <br> # 当网络不稳定时，可以数值可设置大一些。 |
| SHARE_ROOM_TYPE | local | local <br> redis | 会话监控和共享使用的方式 |
| REDIS_HOST | 127.0.0.1 | - | Reids 地址 |
| REDIS_PORT | 6379 | - | Redis 端口 |
| REDIS_PASSWORD | '' | - | Redis 密码 |
| REDIS_DB_ROOM | 0 | - | 选择的 Redis 库索引 |
| ENABLE_LOCAL_PORT_FORWARD | true | true <br> false | 是否开启本地转发 (目前仅对 VScode Remote SSH 有效果) |
| ENABLE_VSCODE_SUPPORT | true | true <br> false | 是否开启针对 VScode 的 Remote SSH 远程开发支持 <br> # 前置条件: 必须开启 ENABLE_LOCAL_PORT_FORWARD |

## 3 Lion 参数说明
!!! tip ""
    - Lion 参数如下：

|  参数名称   | 默认值  | 可选项  | 说明  |
|  :-----  | :-----  |  :-----  | :-----  |
| NAME | hostname | - | 主机名 |
| CORE_HOST | http://127.0.0.1:8080 | - | Jumpserver 项目的 Url，API 请求注册会使用 |
| BOOTSTRAP_TOKEN | '' | - | 预共享秘钥，请和JumpServer 配置文件中保持一致	 |
| BIND_HOST | 0.0.0.0 | - | 启动时绑定的IP |
| HTTPD_PORT | 8081 | - | 监听的 HTTP/WS 端口号 |
| GUA_HOST | 127.0.0.1 | - | Guacd 项目 URL |
| GUA_PORT | 4822 | - | Guacd 项目端口 |
| LOG_LEVEL | DEBUG | DEBUG <br> INFO <br> WARNING <br> ERROR <br> CRITICAL | 日志级别 |
| SHARE_ROOM_TYPE | local | local <br> redis | 会话监控和共享使用的方式 |
| REDIS_HOST | 127.0.0.1 | - | Reids 地址 |
| REDIS_PORT | 6379 | - | Redis 端口 |
| REDIS_PASSWORD | '' | - | Redis 密码 |
| REDIS_DB_ROOM | 0 | - | 选择的 Redis 库索引 |
| JUMPSERVER_DISABLE_ALL_COPY_PASTE | false | true <br> false | 全局禁用上传下载 |
| JUMPSERVER_DISABLE_ALL_UPLOAD_DOWNLOAD | false | true <br> false | 全局禁用剪切板粘贴复制 |
| JUMPSERVER_REMOTE_APP_UPLOAD_DOWNLOAD_ENABLE | false | true <br> false | 开启Remote App的上传下载 |
| JUMPSERVER_REMOTE_APP_COPY_PASTE_ENABLE | false | true <br> false | 开启Remote app的剪切板粘贴复制 |
| JUMPSERVER_COLOR_DEPTH | 32 | 低色 16位 <br> 真彩 24位 <br> 真彩 32位 | 颜色深度 |
| JUMPSERVER_DPI | 120 | 120 <br> 160 <br> 240 | 图像每英寸长度内的像素点数 |
| JUMPSERVER_DISABLE_AUDIO | false | true <br> false | 禁止声音 |
| JUMPSERVER_ENABLE_WALLPAPER | false | true <br> false | 启用墙纸 |
| JUMPSERVER_ENABLE_THEMING | false | true <br> false | 启用主题 |
| JUMPSERVER_ENABLE_FONT_SMOOTHING | false | true <br> false | 启用平滑字体 |
| JUMPSERVER_ENABLE_FULL_WINDOW_DRAG | false | true <br> false | 启用拖拽窗口时渲染全部内容 |
| JUMPSERVER_ENABLE_DESKTOP_COMPOSITION | false | true <br> false | 启用透明窗口和阴影等图形效果 |
| JUMPSERVER_ENABLE_MENU_ANIMATIONS | false | true <br> false | 启用菜单开关动画 |
| JUMPSERVER_DISABLE_BITMAP_CACHING | true | true <br> false | 禁用RDP的内置位图缓存功能 |
| JUMPSERVER_DISABLE_OFFSCREEN_CACHING | true | true <br> false | 禁用客户端中当前不可见的屏幕区域缓存 |
| JUMPSERVER_DISABLE_GLYPH_CACHING | true | true <br> false | 禁用RDP会话中的字形缓存 |
| JUMPSERVER_CLEAN_DRIVE_SCHEDULE_TIME | 1 <br> 0 | - | 定时清理挂载盘文件的时间间隔 (单位：小时) ，如果设置值 0，则不清理 |
