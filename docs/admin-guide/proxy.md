# 反向代理

!!! info "反向代理 JumpServer要求说明"
    - rdp 协议复制粘贴需要部署可信任的 ssl 证书
    - 通过 https 协议访问就能在 rdp 资产里面使用复制粘贴

### 1. nginx ssl 部署

!!! tip "请准备好 nginx 证书"
    - 将证书放到 /opt/jumpserver/config/nginx/cert 里面

!!! tip ""
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim hl_lines="9"
    ...

    ## Nginx 配置，这个 Nginx 是用来分发路径到不同的服务
    HTTP_PORT=8080
    HTTPS_PORT=127.0.0.1:8443
    SSH_PORT=2222

    ## LB 配置, 这个 Nginx 是 HA 时可以启动负载均衡到不同的主机
    USE_LB=1
    LB_HTTP_PORT=80
    LB_HTTPS_PORT=443
    LB_SSH_PORT=2223
    ```
    ```sh
    vi /opt/jumpserver/config/nginx/lb_http_server.conf
    ```
    ```nginx hl_lines="4 10 16 18-19"
    # Todo: May be can auto discovery
    upstream http_server {
      sticky name=jms_route;
      server nginx:8080;    # 这个是 config.txt 里面的 HTTP_PORT 端口
      # server HOST2:8080;  # 另外的要写真实IP
    }

    server {
      listen 80;
      server_name demo.jumpserver.org;  # 自行修改成你自己的域名
      return 301 https://$server_name$request_uri;
    }

    server {
      listen 443 ssl;
      server_name demo.jumpserver.org;      # 自行修改成你自己的域名
      server_tokens off;
      ssl_certificate cert/server.crt;      # 修改成你自己的证书
      ssl_certificate_key cert/server.key;  # 修改成你自己的证书
      ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

      ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4:!DH:!DHE;
      add_header Strict-Transport-Security "max-age=31536000";

      client_max_body_size 5000m;

      location / {
        proxy_pass http://http_server;
        proxy_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $http_connection;

        proxy_ignore_client_abort on;
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 6000;
      }
    }
    ```

### 2. 多层 nginx 反向代理

!!! tip ""
    - 适合上层还有统一对外出口的反向代理服务器
    - 属于多层 nginx 反向代理
    - 每一层都需要设置 websocket 长连接

!!! tip ""
    ```sh
    vi /etc/nginx/conf.d/jumpserver.conf
    ```
    ```vim
    server {

        listen 80;
        server_name demo.jumpserver.org;  # 自行修改成你的域名

        client_max_body_size 4096m;  # 上传录像大小限制

        location / {
                # 这里的 ip 是后端 JumpServer nginx 的 ip
                proxy_pass http://192.168.244.144;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

??? tip "推荐部署 ssl 使用更安全的 https 协议访问"
    ```vim
    server {
        listen 80;
        server_name demo.jumpserver.org;  # 自行修改成你的域名
        return 301 https://$server_name$request_uri;
    }
    server {
        listen 443 ssl;
        server_name demo.jumpserver.org;  # 自行修改成你的域名
        ssl_certificate   /etc/nginx/sslkey/1_jumpserver.org_bundle.crt;  # 自行设置证书
        ssl_certificate_key  /etc/nginx/sslkey/2_jumpserver.org.key;  # 自行设置证书
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;  # 自行替换成你证书支持的加密套件
        ssl_protocols TLSv1.1 TLSv1.2;  # 支持的协议
        ssl_prefer_server_ciphers on;

        client_max_body_size 4096m;  # 录像及文件上传大小限制
        location / {
            # 这里的 ip 是后端 JumpServer nginx 的 ip
            proxy_pass http://192.168.244.144;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

### 3. 其他 slb

!!! tip ""
    - 需要注意 websocket 长连接设置即可
    - 需要注意 session 问题
