# JumpServer Environment Integration

## 1 Operation Process

### 1.1 Edit Configuration File

!!! tip ""
    ```bash
    vi /etc/nginx/conf.d/jumpserver.conf
    ```

### 1.2 Select Deployment Method

!!! tip ""
    === "Source Code Deployment"

        ```nginx
        server {
          listen 80;
          server_name _;
          client_max_body_size 5000m;

          # Luna Configuration
          location /luna/ {
            proxy_pass http://localhost:4200;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }

          # Core Static Resources
          location /media/replay/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver-v4.10.9/data/;
          }

          location /static/ {
            root /opt/jumpserver-v4.10.9/data/;
          }

          # KoKo Lion Configuration
          location /koko/ {
            proxy_pass http://localhost:2222;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_request_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
          }

          # Lion Configuration
          location /lion/ {
            proxy_pass http://localhost:8081;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
          }

          # Core Configuration
          location / {
            proxy_pass http://localhost:8000;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_request_buffering off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
          }
        }
        ```

    === "Using Release"

        ```nginx
        server {
          listen 80;
          server_name _;
          client_max_body_size 5000m;

          # Luna Configuration
          location /luna/ {
            alias /opt/jumpserver-v4.10.9/lina/;
            try_files $uri $uri/ /luna/index.html;
          }

          # Lina Configuration
          location / {
            alias /opt/jumpserver-v4.10.9/lina/;
            try_files $uri $uri/ /index.html;
          }

          # Core Static Resources
          location /media/replay/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver-v4.10.9/;
          }

          location /static/ {
            root /opt/jumpserver-v4.10.9/;
          }

          # KoKo Configuration
          location /koko/ {
            proxy_pass http://127.0.0.1:2222;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
          }

          # Core API Configuration
          location /api/ {
            proxy_pass http://127.0.0.1:8000;
            proxy_http_version 1.1;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }
        }
        ```

    ```bash
    nginx -t
    nginx -s reload
    ```
