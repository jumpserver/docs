# Tengine 代理部署

## 环境

-  系统: CentOS 7
-  IP: 192.168.100.100

```
+----------+------------+-----------------+---------------+
| Protocol | ServerName |        IP       |      Port     |
+==========+============+=================+===============+
|    TCP   |  Tengine   | 192.168.100.100 | 80, 443, 2222 |
+----------+------------+-----------------+---------------+
```

## 安装步骤


### 1. 安装 epel 库

```sh
yum upgrade -y
yum -y install epel-release wget
```

### 2. 配置防火墙

```sh
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=443/tcp --permanent
firewall-cmd --zone=public --add-port=2222/tcp --permanent
firewall-cmd --reload
semanage fcontext -a -t httpd_sys_content_t '/opt/jumpserver(/.*)?'
setsebool -P httpd_can_network_connect 1
```

!!! warning "生产环境下不应该关闭 selinux"

### 3. 安装 tengine

```sh
cd /opt
yum localinstall -y http://demo.jumpserver.org/download/centos/7/tengine-2.3.2-1.el7.ngx.x86_64.rpm
```

??? warning "生产环境请自行编译安装 [tengine](http://tengine.taobao.org)"
    [该 rpm 源码点击此处](https://github.com/wojiushixiaobai/tengine-rpm)   

### 4. 下载 luna

```sh
cd /opt
wget https://github.com/jumpserver/luna/releases/download/1.5.8/luna.tar.gz
```

??? question "如果网络存在问题可以点击 [此处](https://demo.jumpserver.org/download/luna/) 下载"
    ```sh
    wget https://demo.jumpserver.org/download/luna/1.5.8/luna.tar.gz
    ```

### 5. 解压 luna

```sh
tar -xf luna.tar.gz
chown -R nginx:nginx luna
```

### 6. 安装 nfs

```sh
yum -y install nfs-utils
```

### 7. 挂载 nfs

```sh
showmount -e 192.168.100.99
mkdir -p /opt/jumpserver/data
restorecon -R /opt/jumpserver/data/
mount -t nfs 192.168.100.99:/data /opt/jumpserver/data
echo "192.168.100.99:/data /opt/jumpserver/data nfs defaults 0 0" >> /etc/fstab
```

!!! tip "192.168.100.99 为 nfs server 地址，请自行更改"

### 8. 配置 ssh 反向代理

```sh
vi /etc/nginx/nginx.conf
```
```vim
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}

stream {
    log_format  proxy  '$remote_addr [$time_local] '
                        '$protocol $status $bytes_sent $bytes_received '
                        '$session_time "$upstream_addr" '
                        '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';

    access_log /var/log/nginx/tcp-access.log  proxy;
    open_log_file_cache off;

    upstream kokossh {
        server 192.168.100.40:2222;
        server 192.168.100.41:2222;  # 多节点
        # 这里是 koko ssh 的后端ip
        least_conn;
    }

    server {
        listen 2222;
        proxy_pass kokossh;
        proxy_protocol on;
        proxy_connect_timeout 1s;
    }
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    # tcp_nopush     on;

    keepalive_timeout  65;

    # 关闭版本显示
    server_tokens off;

    include /etc/nginx/conf.d/*.conf;
}
```

### 9. 配置 http 反向代理

```sh
vi /etc/nginx/conf.d/jumpserver.conf

```
```vim
upstream jumpserver {
    server 192.168.100.30:80;
    server 192.168.100.31:80;
    # 这里是 core 的后端ip
    session_sticky;
}

upstream koko {
    server 192.168.100.40:5000;
    server 192.168.100.41:5001;  # 多节点
    # 这里是 koko 的后端ip
    session_sticky;
}

upstream guacamole {
    server 192.168.100.50:8081;
    server 192.168.100.51:8081;  # 多节点
    # 这里是 guacamole 的后端ip
    session_sticky;
}

server {
    listen 80;
    # server_name demo.jumpserver.org;  # 自行修改成你的域名
    # return 301 https://$server_name$request_uri;
# }

# server {
    # 推荐使用 https 访问, 请自行修改下面的选项
    # listen 443 ssl;
    # server_name demo.jumpserver.org;  # 自行修改成你的域名
    # ssl_certificate   /etc/nginx/sslkey/1_jumpserver.org_bundle.crt;  # 自行设置证书
    # ssl_certificate_key  /etc/nginx/sslkey/2_jumpserver.org.key;  # 自行设置证书
    # ssl_session_timeout 5m;
    # ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    # ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    # ssl_prefer_server_ciphers on;

    client_max_body_size 100m;  # 录像上传大小限制

    location /luna/ {
        try_files $uri / /index.html;
        alias /opt/luna/;  # luna 路径
    }

    location /media/ {
        add_header Content-Encoding gzip;
        root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
    }

    location /static/ {
        root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
    }

    location / {
        proxy_pass       http://jumpserver;  # jumpserver
        proxy_buffering  off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        access_log off;
    }

    location /koko/ {
        proxy_pass       http://koko;  # koko
        proxy_buffering  off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        access_log off;
    }

    location /guacamole/ {
        proxy_pass       http://guacamole/;  #  guacamole
        proxy_buffering  off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $http_connection;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        access_log off;
    }
}
```

### 10. 启动 nginx

```sh
nginx -t
systemctl enable nginx
systemctl start nginx
```

??? info "访问 http://192.168.100.100"
    默认账号: admin 密码: admin  
    到会话管理-终端管理 检查 koko Guacamole 等应用的注册  
    ```sh
    ssh -p2222 admin@192.168.100.100  
    sftp -P2222 admin@192.168.100.100  
    ```
    密码: admin  
    如果是用在 Windows 下, Xshell Terminal 登录语法如下  
    ```sh
    ssh admin@192.168.100.100 2222  
    sftp admin@192.168.100.100 2222  
    ```
    密码: admin   
    如果能登陆代表部署成功
