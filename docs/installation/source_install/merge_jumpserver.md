# JumpServer 环境整合
## 1 操作过程
### 1.1 编辑配置文件
!!! tip ""

    ```bash
    vi /etc/nginx/conf.d/jumpserver.conf
    ```

### 1.2 选择部署方式
!!! tip ""
    === "源代码部署"

        ```nginx
        server {
          listen 80;
          # server_name _;

          client_max_body_size 5000m; 文件大小限制

          # Luna 配置
          location /luna/ {
            # 注意将模板中的组件名称替换为服务实际 ip 地址， 如都在本机部署
            # proxy_pass       http://127.0.0.1:4200;
            proxy_pass http://luna:4200;
          }

          # Core data 静态资源
          location /media/replay/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver-{{ jumpserver.tag }}/data/;
          }

          location /static/ {
            root /opt/jumpserver-{{ jumpserver.tag }}/data/;
          }

          # KoKo Lion 配置
          location /koko/ {
            # 注意将模板中的组件名称替换为服务实际 ip 地址， 如都在本机部署
            # proxy_pass       http://127.0.0.1:5000;
            proxy_pass       http://koko:5000;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
          }

          # lion 配置
          location /lion/ {
            # 注意将模板中的组件名称替换为服务实际 ip 地址， 如都在本机部署
            # proxy_pass       http://127.0.0.1:8081;
            proxy_pass http://lion:8081;
            proxy_buffering off;
            proxy_request_buffering off;
            proxy_http_version 1.1;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_ignore_client_abort on;
            proxy_connect_timeout 600;
            proxy_send_timeout 600;
            proxy_read_timeout 600;
            send_timeout 6000;
          }

          location ~ ^/(core|api|media)/ {
            # 注意将模板中的组件名称替换为服务实际 ip 地址， 如都在本机部署
            # proxy_pass       http://127.0.0.1:8080;
            proxy_pass http://core:8080;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }

          # 前端 Lina
          location /ui/ {
            # 注意将模板中的组件名称替换为服务实际 ip 地址， 如都在本机部署
            # proxy_pass       http://127.0.0.1:9528;
            proxy_pass http://lina:9528;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }

          location / {
            rewrite ^/(.*)$ /ui/$1 last;
          }
        }
        ```

    === "使用 Release"

        ```nginx
        server {
          listen 80;
          # server_name _;

          client_max_body_size 5000m; 文件大小限制

          # 前端 Lina
          location /ui/ {
            try_files $uri / /index.html;
            alias /opt/lina-{{ jumpserver.tag }}/;
            expires 24h;
          }

          # Luna 配置
          location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna-{{ jumpserver.tag }}/;
            expires 24h;
          }

          # Core data 静态资源
          location /media/replay/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver-{{ jumpserver.tag }}/data/;
          }

          location /static/ {
            root /opt/jumpserver-{{ jumpserver.tag }}/data/;
            expires 24h;
          }

          # KoKo Lion 配置
          location /koko/ {
            # 注意将模板中的组件名称替换为服务实际 ip 地址， 如都在本机部署
            # proxy_pass       http://127.0.0.1:5000;
            proxy_pass       http://koko:5000;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
          }

          # lion 配置
          location /lion/ {
            # 注意将模板中的组件名称替换为服务实际 ip 地址， 如都在本机部署
            # proxy_pass       http://127.0.0.1:8081;
            proxy_pass http://lion:8081;
            proxy_buffering off;
            proxy_request_buffering off;
            proxy_http_version 1.1;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_ignore_client_abort on;
            proxy_connect_timeout 600;
            proxy_send_timeout 600;
            proxy_read_timeout 600;
            send_timeout 6000;
          }

          location ~ ^/(core|api|media)/ {
            # 注意将模板中的组件名称替换为服务实际 ip 地址， 如都在本机部署
            # proxy_pass       http://127.0.0.1:8080;
            proxy_pass http://core:8080;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }

          location / {
            rewrite ^/(.*)$ /ui/$1 last;
          }
        }
        ```

    ```bash
    nginx -t
    ```
    ```bash
    nginx -s reload
    ```
