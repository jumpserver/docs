# Reverse Proxy

!!! info "JumpServer Reverse Proxy Requirements"
    - RDP protocol copy/paste requires deploying trusted SSL certificates.
    - Access via HTTPS protocol enables copy/paste functionality in RDP assets.
    - Follow recommendations from [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/){:target="_blank"}.

## 1 Nginx SSL Deployment

!!! tip "Prepare SSL certificates (note: certificates must be in pem format)"
    - Place certificates in /opt/jumpserver/config/nginx/cert.
    - Close JumpServer service before modifying configuration files.

!!! tip ""
    ```bash
    # Close JumpServer service
    ./jmsctl.sh stop
    ```
    ```bash
    # Edit JumpServer main configuration file
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim
    ...

    ## Nginx Configuration
    HTTP_PORT=80
    SSH_PORT=2222
    RDP_PORT=3389

    ## HTTPS Configuration
    HTTPS_PORT=443               # External HTTPS port, default 443
    SSL_CERTIFICATE=/opt/jumpserver/config/nginx/cert/server.crt
    SSL_CERTIFICATE_KEY=/opt/jumpserver/config/nginx/cert/server.key
    ```

## 2 Multi-layer Nginx Reverse Proxy

!!! tip "Note"
    - Suitable for environments with unified external exit reverse proxy servers
    - Each layer must set websocket long connection

!!! tip ""
    ```nginx
    upstream jumpserver {
      server jumpserver_ip:80;
    }

    server {
      listen 80;
      server_name _;
      client_max_body_size 5000m;
      
      location / {
        proxy_pass http://jumpserver;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
      }
    }
    ```

!!! tip "Recommend deploying SSL for more secure HTTPS protocol access"
    - Follow [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) recommendations.

## 3 Other SLB

!!! tip "Note"
    - Just need to pay attention to websocket long connection settings.
    - Need to pay attention to session issues.
