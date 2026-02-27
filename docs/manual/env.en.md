# Parameter Description

!!! warning "Attention"
    - Close JumpServer service before modifying configuration files.

## 1 Core Parameter Description
!!! tip ""
    - Open the config.txt configuration file.

    ```sh
    vi /opt/jumpserver/config/config.txt
    ```

!!! tip ""
    - Core parameters are as follows:

| Parameter Name | Default Value | Optional | Description |
| :--- | :--- | :--- | :--- |
| SECRET_KEY | '' | - | Key for encrypting/decrypting sensitive fields |
| BOOTSTRAP_TOKEN | '' | - | Token used for component registration with Core service |
| DEBUG | false | true <br> false | Debug mode; shows more information when page requests API errors if enabled |
| DEBUG_DEV | false | true <br> false | Debug development mode; backend logs show more information if enabled |
| LOG_LEVEL | DEBUG | DEBUG <br> INFO <br> WARNING <br> ERROR <br> CRITICAL | Log level |
| LOG_DIR | /data/jumpserver/core/logs | - | Log directory |
| DB_ENGINE | mysql | - | Database engine |
| DB_NAME | jumpserver | - | Database name |
| DB_HOST | 127.0.0.1 | - | Database address |
| DB_PORT | 3306 | - | Database port |
| DB_USER | root | - | Database user |
| DB_PASSWORD | '' | - | Database user password |
| DB_USE_SSL | false | true <br> false | Enable SSL for database |
| REDIS_HOST | 127.0.0.1 | - | Redis address |
| REDIS_PORT | 6379 | - | Redis port |
| REDIS_PASSWORD | '' | - | Redis password |
| REDIS_USE_SSL | false | true <br> false | Enable SSL for Redis |
| REDIS_SSL_KEY | null | - | Redis SSL Key |
| REDIS_SSL_CERT | null | - | Redis SSL certificate |
| REDIS_SSL_CA | null | - | Redis SSL CA certificate |
| REDIS_SSL_REQUIRED | null | - | Whether Redis SSL certificate is required |
| REDIS_MAX_CONNECTIONS | 100 | - | Maximum Redis connections |
| REDIS_SENTINEL_HOSTS | '' | - | Redis Sentinel addresses (multiple addresses separated by /) |
| REDIS_SENTINEL_PASSWORD | '' | - | Redis Sentinel password |
| REDIS_SENTINEL_SOCKET_TIMEOUT | null | - | Redis Sentinel Socket timeout |
| REDIS_DB_CELERY | 3 | 0-15 | Redis database number for Celery tasks |
| REDIS_DB_CACHE | 4 | 0-15 | Redis database number for cache |
| REDIS_DB_SESSION | 5 | 0-15 | Redis database number for user sessions |
| REDIS_DB_WS | 6 | - | Redis database number for WebSocket |
| TOKEN_EXPIRATION | 3600 * 24 (s) | - | Expiration time for API-created user tokens <br> # If configured as empty or 0, default is 3600 |
| DEFAULT_EXPIRED_YEARS | 70 (year) | - | Default expiration years for created resources, e.g. authorization rules <br> # Not allowed to modify |
| SESSION_COOKIE_DOMAIN | null | - | User session cookie domain, e.g. fit2cloud.com |
| CSRF_COOKIE_DOMAIN | null | - | User CSRF cookie domain; defaults to same as SESSION_COOKIE_DOMAIN |
| SESSION_COOKIE_NAME_PREFIX | null | - | User-set session cookie name prefix |
| SESSION_COOKIE_AGE | 3600 * 24 (s) | - | User session cookie expiration time |
| SESSION_EXPIRE_AT_BROWSER_CLOSE | false | true <br> false | User session expires after browser closes |
| CONNECTION_TOKEN_ONETIME_EXPIRATION | 5 * 60 | >= 5 * 60 | ConnectionToken can only be used once within validity period |
| CONNECTION_TOKEN_REUSABLE_EXPIRATION | 3600 * 24 * 30 (s) | - | ConnectionToken can be reused multiple times within validity period |
| CONNECTION_TOKEN_REUSABLE | false | true <br> false | Whether ConnectionToken can be reused multiple times |
| AUTH_CUSTOM | false | true <br> false | Enable custom user authentication |
| AUTH_CUSTOM_FILE_MD5 | '' | - | MD5 value of custom user authentication file |
| MFA_CUSTOM | false | true <br> false | Enable custom MFA authentication |
| MFA_CUSTOM_FILE_MD5 | '' | - | MD5 value of custom MFA authentication file |
| AUTH_TEMP_TOKEN | false | true <br> false | Enable temporary password feature |
| AUTH_SSO | false | true <br> false | Enable SSO authentication |
| AUTH_SSO_AUTHKEY_TTL | 60 * 15 (s) | SSO authentication key TTL |
| LOGIN_REDIRECT_TO_BACKEND | '' | Direct (direct to internal login page) <br> OpenID <br> CAS <br> SAML2 <br> OAuth2 service provider name (System Settings) | After enabling third-party authentication, directly redirect to authentication service without countdown page, e.g. OpenID |
| LOGIN_REDIRECT_MSG_ENABLED | true | true <br> false | Enable third-party redirect countdown page |
| SYSLOG_ADDR | '' | - | SysLog service address |
| SYSLOG_FACILITY | user | - | SysLog FACILITY |
| SYSLOG_SOCKTYPE | 2 | - | SysLog SockType |
| PERM_EXPIRED_CHECK_PERIODIC | 60 * 60 (s) | - | Period for checking expired asset authorization rules and expiring user authorization trees |
| LANGUAGE_CODE | en | zh <br> en <br> ja | Language |
| TIME_ZONE | Asia/Shanghai | - | Time zone |
| SESSION_COOKIE_SECURE | false | true <br> false | User session cookie security mode; only allows HTTPS when enabled |
| DOMAINS | '' | - | Specify allowed domains for JumpServer application |
| CSRF_COOKIE_SECURE | false | true <br> false | User CSRF token security mode; only allows HTTPS when enabled |
| REFERER_CHECK_ENABLED | false | true <br> false | Whether to enable REFERER validation |
| CSRF_TRUSTED_ORIGINS | - | - | CSRF same-origin trust; multiple addresses separated by `,` |
| SESSION_ENGINE | cache | - | User session engine |
| SESSION_SAVE_EVERY_REQUEST | true | true <br> false | Save user session on every request |
| SESSION_EXPIRE_AT_BROWSER_CLOSE_FORCE | false | true <br> false | Force session expiration after browser closes |
| SERVER_REPLAY_STORAGE | {} | - | Server-side recording storage <br> e.g.: <br> {<br>    'TYPE': 's3',<br>    'BUCKET': '',<br>    'ACCESS_KEY': '',<br>    'SECRET_KEY': '',<br>    'ENDPOINT': ''<br>} <br> # Components upload recordings to Core service, Core automatically uploads to configured object storage |
| CHANGE_AUTH_PLAN_SECURE_MODE_ENABLED | true | true <br> false | Change password plan secure mode <br> When enabled, users cannot change their own password; <br> When disabled, users can change their own password; <br> e.g. root changing root |
| SECURITY_VIEW_AUTH_NEED_MFA | true | true <br> false | Require MFA verification |
| SECURITY_DATA_CRYPTO_ALGO | null | - | Data encryption algorithm |
| GMSSL_ENABLED | false | true <br> false | Enable national encryption algorithm (data encryption algorithm) <br> SECURITY_DATA_CRYPTO_ALGO <br> GMSSL_ENABLED <br> # If both configured, SECURITY_DATA_CRYPTO_ALGO takes priority |
| OPERATE_LOG_ELASTICSEARCH_CONFIG | {} | - | Storage ES configuration for "changed fields" in operation logs <br> e.g.: <br> {<br>    "INDEX": "",<br>    "HOSTS": "",<br>    "OTHER": "",<br>    "IGNORE_VERIFY_CERTS": "",<br>    "INDEX_BY_DATE": "",<br>    "DOC_TYPE": ""<br>} |
| MAGNUS_ORACLE_PORTS | 30000-30030 | - | Oracle port range that Magnus component needs to listen to |
| APPLET_DOWNLOAD_HOST | '' | - | Download address for Applet and other software |
| FTP_FILE_MAX_STORE | 0 | - | FTP file upload/download backup threshold (unit: M); when value ≤ 0, files are not backed up |
| MAX_LIMIT_PER_PAGE | 10000 | - | Set maximum number of allowed export records |
| FILE_UPLOAD_SIZE_LIMIT_MB | 200 | - | Set maximum file upload size limit (unit: MB) |
| THROTTLE_RATES_ANON | 60/min | string | Rate limit for unauthenticated users |
| THROTTLE_RATES_USER | 180/min | string | Rate limit for users |
| THROTTLE_RATES_SERVICE_ACCOUNT | 300/min | string | Rate limit for component accounts |
