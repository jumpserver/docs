# 部署 HAProxy 服务

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - HAProxy 服务器信息如下: 

    ```sh 
    192.168.100.100
    ```
    
### 1.2 安装依赖
!!! tip ""
    Ubuntu 官方源已包含 HAProxy，无需额外安装 EPEL 源，直接更新系统包索引即可：
    ```sh
    sudo apt update
    ```

## 2 安装配置 HAProxy
### 2.1 安装 HAProxy
!!! tip ""
    ```sh
    sudo apt install -y haproxy
    ```

### 2.2 配置 HAProxy
!!! tip ""
    ```sh
    # 打开 HAProxy 的配置文件
    sudo vim /etc/haproxy/haproxy.cfg
    ```
    ```nginx
    global
        log         127.0.0.1 local2
        chroot      /var/lib/haproxy
        pidfile     /var/run/haproxy.pid
        maxconn     4000
        user        haproxy
        group       haproxy
        daemon

        # turn on stats unix socket
        stats socket /var/lib/haproxy/stats
    defaults
        log                     global
        option                  dontlognull
        option                  redispatch
        retries                 3
        timeout http-request    10s
        timeout queue           1m
        timeout connect         10s
        timeout client          1m
        timeout server          1m
        timeout http-keep-alive 10s
        timeout check           10s
        maxconn                 3000
    listen stats
        bind *:8080
        mode http
        stats enable
        stats uri /haproxy                      # 监控页面, 请自行修改. 访问地址为 http://192.168.100.100:8080/haproxy
        stats refresh 5s
        stats realm haproxy-status
        stats auth admin:KXOeyNgDeTdpeu9q       # 账户密码, 请自行修改. 访问 http://192.168.100.100:8080/haproxy 会要求输入

    #---------------------------------------------------------------------
    # check  检活参数说明
    # inter  间隔时间, 单位: 毫秒
    # rise   连续成功的次数, 单位: 次
    # fall   连续失败的次数, 单位: 次
    # 例: inter 2s rise 2 fall 3
    # 表示 2 秒检查一次状态, 连续成功 2 次服务正常, 连续失败 3 次服务异常
    #
    # server 服务参数说明
    # server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01
    # 第一个 192.168.100.21 做为页面展示的标识, 可以修改为其他任意字符串
    # 第二个 192.168.100.21:80 是实际的后端服务端口
    # weight 为权重, 多节点时安装权重进行负载均衡
    # cookie 用户侧的 cookie 会包含此标识, 便于区分当前访问的后端节点
    # 例: server db01 192.168.100.21:3306 weight 1 cookie db_01
    #---------------------------------------------------------------------

    listen jms-web
        bind *:80                               # 监听 80 端口
        mode http

        # redirect scheme https if !{ ssl_fc }  # 重定向到 https
        # bind *:443 ssl crt /opt/ssl.pem       # https 设置

        option httpchk GET /api/health/         # Core 检活接口
        
        stick-table type ip size 200k expire 30m
        stick on src

        balance leastconn
        server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01 check inter 2s rise 2 fall 3  # JumpServer 服务器
        server 192.168.100.22 192.168.100.22:80 weight 1 cookie web02 check inter 2s rise 2 fall 3

    listen jms-ssh
        bind *:2222
        mode tcp

        option tcp-check

        fullconn 500
        balance source
        server 192.168.100.21 192.168.100.21:2222 weight 1 check inter 2s rise 2 fall 3 send-proxy
        server 192.168.100.22 192.168.100.22:2222 weight 1 check inter 2s rise 2 fall 3 send-proxy

    listen jms-koko
        mode http

        option httpclose
        option forwardfor
        option httpchk GET /koko/health/ HTTP/1.1\r\nHost:\ 192.168.100.100  # KoKo 检活接口, host 填写 HAProxy 的 ip 地址

        cookie SERVERID insert indirect
        hash-type consistent
        fullconn 500
        balance leastconn
        server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01 check inter 2s rise 2 fall 3
        server 192.168.100.22 192.168.100.22:80 weight 1 cookie web02 check inter 2s rise 2 fall 3

    listen jms-lion
        mode http

        option httpclose
        option forwardfor
        option httpchk GET /lion/health/ HTTP/1.1\r\nHost:\ 192.168.100.100  # Lion 检活接口, host 填写 HAProxy 的 ip 地址

        cookie SERVERID insert indirect
        hash-type consistent
        fullconn 500
        balance leastconn
        server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01 check inter 2s rise 2 fall 3
        server 192.168.100.22 192.168.100.22:80 weight 1 cookie web02 check inter 2s rise 2 fall 3

    listen jms-magnus
        bind *:30000
        mode tcp

        option tcp-check

        fullconn 500
        balance source
        server 192.168.100.21 192.168.100.21:30000 weight 1 check inter 2s rise 2 fall 3 send-proxy
        server 192.168.100.22 192.168.100.22:30000 weight 1 check inter 2s rise 2 fall 3 send-proxy
    ```


### 2.3 启动 HAProxy
!!! tip ""
    ```sh
    sudo systemctl enable haproxy
    sudo systemctl start haproxy
    sudo systemctl status haproxy
    ```

## 3 配置防火墙
!!! tip ""
    ```sh
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 2222/tcp
    sudo ufw allow 33060/tcp
    sudo ufw allow 33061/tcp
    sudo ufw reload
    ```