# 反向代理

!!! info "反向代理 JumpServer要求说明"

### 1. nginx ssl 部署

!!! tip ""
    ```sh
    vi /etc/nginx/conf.d/jumpserver.conf
    ```
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
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;  # 支持的协议
        ssl_prefer_server_ciphers on;

        client_max_body_size 100m;  # 录像及文件上传大小限制

        location /ui/ {
            try_files $uri / /index.html;
            alias /opt/lina/;
        }

        location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
        }

        location /media/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
        }

        location /static/ {
            root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        }

        location /koko/ {
            proxy_pass       http://localhost:5000;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /guacamole/ {
            proxy_pass       http://localhost:8081/;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /ws/ {
            proxy_pass http://localhost:8070;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }

        location /api/ {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://localhost:8080;
        }
        location /core/ {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://localhost:8080;
        }
        location / {
            rewrite ^/(.*)$ /ui/$1 last;
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

        client_max_body_size 100m;  # 上传录像大小限制

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

        client_max_body_size 100m;  # 录像及文件上传大小限制
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
