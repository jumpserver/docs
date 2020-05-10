# 反向代理

!!! info "反向代理 jumpserver要求说明"

- 适合上层还有统一对外出口的反向代理服务器
- 属于多层 nginx 反向代理

### 1. nginx 反向代理

```sh
vi /etc/nginx/conf.d/jumpserver.conf
```

```vim
server {

    listen 80;
    server_name demo.jumpserver.org;  # 自行修改成你的域名

    client_max_body_size 100m;  # 上传录像大小限制

    location / {
            # 这里的 ip 是后端 jumpserver nginx 的 ip
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
            # 这里的 ip 是后端 jumpserver nginx 的 ip
            proxy_pass http://192.168.244.144;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    ```

### 2. 其他 slb

- 需要注意 websocket 长连接设置即可
- 需要注意 session 问题
