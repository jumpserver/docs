# 反向代理

!!! info "反向代理 JumpServer 要求说明"
    - rdp 协议复制粘贴需要部署可信任的 ssl 证书
    - 通过 https 协议访问就能在 rdp 资产里面使用复制粘贴
    - 遵循 [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) 建议

### 1. nginx ssl 部署

!!! tip "请准备好 ssl 证书"
    - 将证书放到 /opt/jumpserver/config/nginx/cert 里面

!!! tip ""
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim
    ...

    ## Nginx 配置, USE_LB=1 表示开启, 为 0 的情况下, HTTPS_PORT 定义不生效
    HTTP_PORT=80
    SSH_PORT=2222
    RDP_PORT=3389

    USE_LB=1           # 1 表示开启此选项
    HTTPS_PORT=443     # 对外 https 端口
    ```
    ```sh
    vi /opt/jumpserver/config/nginx/lb_http_server.conf
    ```
    ```nginx hl_lines="10 16 18-19 25 29"
    # Todo: May be can auto discovery
    upstream http_server {
      sticky name=jms_route;
      server nginx:80;
      # server HOST2:80;  # 多节点
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
      ssl_session_timeout 1d;
      ssl_session_cache shared:MozSSL:10m;
      ssl_session_tickets off;
      ssl_protocols TLSv1.1 TLSv1.2;

      ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
      ssl_prefer_server_ciphers off;
      add_header Strict-Transport-Security "max-age=63072000" always;

      client_max_body_size 5000m;  # 上传文件大小限制

      location / {
        proxy_pass http://http_server;
        proxy_buffering off;
        proxy_request_buffering off;
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
    ```sh
    ./jmsctl.sh restart
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
    ```vim hl_lines="4 6 10"
    server {

        listen 80;
        server_name demo.jumpserver.org;  # 自行修改成你的域名

        client_max_body_size 4096m;  # 上传文件大小限制

        location / {
                # 这里的 ip 是后端 JumpServer nginx 的 ip
                proxy_pass http://192.168.244.144;
                proxy_http_version 1.1;
                proxy_buffering off;
                proxy_request_buffering off;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

!!! tip "推荐部署 ssl 使用更安全的 https 协议访问"
    - 遵循 [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) 建议

    ```vim hl_lines="3 8-10 13 18 21"
    server {
        listen 80;
        server_name demo.jumpserver.org;  # 自行修改成你的域名
        return 301 https://$server_name$request_uri;
    }
    server {
        listen 443 ssl;
        server_name          demo.jumpserver.org;  # 自行修改成你的域名
        ssl_certificate      sslkey/1_jumpserver.org_bundle.crt;  # 自行设置证书
        ssl_certificate_key  sslkey/2_jumpserver.org_bundle.key;  # 自行设置证书
        ssl_session_timeout 1d;
        ssl_session_cache shared:MozSSL:10m;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_protocols TLSv1.1 TLSv1.2;
        add_header Strict-Transport-Security "max-age=63072000" always;

        client_max_body_size 4096m;  # 录像及文件上传大小限制
        location / {
            # 这里的 ip 是后端 JumpServer nginx 的 ip
            proxy_pass http://192.168.244.144;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_request_buffering off;
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
