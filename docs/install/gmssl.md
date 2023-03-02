# 国密改造

!!! info "应相关单位要求，本文以沃通证书为例"
    - [国密SSL证书试用申请指南](https://www.wotrus.com/support/freetestv1_apply_guide.htm)
    - 并非所有浏览器都支持国密，请做好相应的准备工作。

## 1 操作过程
### 1.1 配置 JumpServer
!!! tip ""
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```

    ```nginx hl_lines="4"
    ...

    # 使用国密算法
    SECURITY_DATA_CRYPTO_ALGO=gm
    ```

    ```sh
    # 重启 JumpServer 服务
    ./jmsctl.sh restart
    ```

### 1.2 配置 Nginx
!!! tip ""
    ```sh
    # Nginx 镜像下载
    docker pull wojiushixiaobai/wotrus_nginx:v1.20.2
    docker tag wojiushixiaobai/wotrus_nginx:v1.20.2 jumpserver/wotrus_nginx:v1.20.2
    docker rmi wojiushixiaobai/wotrus_nginx:v1.20.2
    ```
    ```sh
    # 解压 ssl 证书
    ll /opt/sslkey

    总用量 24
    -rw-r--r--. 1 root root 6281 12月  2 19:34 test.domain.localhost_bundle.crt
    -rw-r--r--. 1 root root 1675 12月  2 19:34 test.domain.localhost_RSA.key
    -rw-r--r--. 1 root root 3048 12月  2 19:11 test.domain.localhost_sm2_encrypt_bundle.crt
    -rw-r--r--. 1 root root  227 12月  2 19:11 test.domain.localhost_SM2.key
    -rw-r--r--. 1 root root 3048 12月  2 19:11 test.domain.localhost_sm2_sign_bundle.crt
    ```
    ```sh
    #  Nginx 配置文件编辑
    vi /opt/default.conf
    ```
    ```nginx hl_lines="3 9 12 17-18 20-21 23-24 29"
    server {
        listen 80;
        server_name test.domain.localhost;  # 自行修改成你的域名
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name test.domain.localhost;  # 自行修改成你的域名

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers ECC-SM4-SM3:ECDH:AESGCM:HIGH:MEDIUM:!RC4:!DH:!MD5:!aNULL:!eNULL;  # 算法
        ssl_verify_client off;
        ssl_session_timeout 5m;
        ssl_prefer_server_ciphers on;

        # ssl_certificate sslkey/test.domain.localhost_bundle.crt;             # rsa 证书，过渡使用
        # ssl_certificate_key sslkey/test.domain.localhost_RSA.key;

        ssl_certificate sslkey/test.domain.localhost_sm2_sign_bundle.crt;      # 配置国密签名证书/私钥
        ssl_certificate_key sslkey/test.domain.localhost_SM2.key;

        ssl_certificate sslkey/test.domain.localhost_sm2_encrypt_bundle.crt;   # 配置国密加密证书/私钥
        ssl_certificate_key sslkey/test.domain.localhost_SM2.key;

        client_max_body_size 5000m;  # 上传文件大小限制

        location / {
            proxy_pass http://192.168.100.100;  # 后端 jumpserver 访问地址
            proxy_buffering off;
            proxy_request_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_set_header X-Forwarded-For $remote_addr;

            proxy_ignore_client_abort on;
            proxy_connect_timeout 600;
            proxy_send_timeout 600;
            proxy_read_timeout 600;
            send_timeout 6000;
        }
    }
    ```
### 1.3 启动容器
!!! tip ""   
    ```sh
    docker run --name nginx -d --restart=always \
      -p 80:80 -p 443:443 \
      -v /opt/sslkey:/etc/nginx/sslkey \
      -v /opt/default.conf:/etc/nginx/conf.d/default.conf \
      jumpserver/wotrus_nginx:v1.20.2
    ```
