# Deploy HAProxy Service

## 1 Preparation
### 1.1 Environment Information
!!! tip ""
    - HAProxy server information is as follows: 

    ```sh 
    192.168.100.100
    ```
    
### 1.2 Install Dependencies
!!! tip ""
    The Ubuntu official repository includes HAProxy. No need to install additional EPEL repositories. Just update the system package index:
    ```sh
    sudo apt update
    ```

## 2 Install and Configure HAProxy
### 2.1 Install HAProxy
!!! tip ""
    ```sh
    sudo apt install -y haproxy
    ```

### 2.2 Configure HAProxy
!!! tip ""
    ```sh
    # Open the HAProxy configuration file
    sudo vim /etc/haproxy/haproxy.cfg
    ```
    ```nginx
    global
        log         127.0.0.1 local2
        chroot      /var/lib/haproxy
        pidfile     /var/run/haproxy.pid
        maxconn     4096
        user        haproxy
        group       haproxy
        daemon
        stats socket /var/lib/haproxy/stats
    
    defaults
        log                     global
        mode                    tcp
        option                  tcplog
        option                  dontlognull
        retries                 3
        timeout connect 5000
        timeout client 50000
        timeout server 50000
        maxconn                 3000
    
    listen stats
        bind *:8080
        stats enable
        stats uri /haproxy
        stats refresh 30s
        stats admin if TRUE
        stats auth admin:KXOeyNgDeTdpeu9q       # Username and password. Please modify. Access http://192.168.100.100:8080/haproxy

    #---------------------------------------------------------------------
    # check parameter description
    # inter  check interval, unit: milliseconds
    # rise   consecutive successful checks, unit: times
    # fall   consecutive failed checks, unit: times
    # example: inter 2s rise 2 fall 3
    # means check every 2 seconds, service is normal after 2 consecutive successes, service is abnormal after 3 consecutive failures
    #
    # server parameter description
    # server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01
    # The first 192.168.100.21 is the identifier shown on the page, can be changed to any string
    # The second 192.168.100.21:80 is the actual backend service port
    # weight is the weight for load balancing among multiple nodes
    # cookie identifier will be included in user-side cookies to distinguish which backend node is being accessed
    # example: server db01 192.168.100.21:3306 weight 1 cookie db_01
    #---------------------------------------------------------------------

    listen jms-web
        bind *:80
        balance roundrobin
        option httpchk GET /api/health/
        default-server inter 2s rise 2 fall 3
        server 192.168.100.21 192.168.100.21:80 weight 1 cookie web01 check
        server 192.168.100.22 192.168.100.22:80 weight 1 cookie web02 check

    listen jms-ssh
        bind *:2222
        balance roundrobin
        default-server inter 2s rise 2 fall 3
        server 192.168.100.21 192.168.100.21:2222 weight 1 cookie ssh01 check
        server 192.168.100.22 192.168.100.22:2222 weight 1 cookie ssh02 check

    listen jms-rdp
        bind *:3389
        balance roundrobin
        default-server inter 2s rise 2 fall 3
        server 192.168.100.21 192.168.100.21:3389 weight 1 cookie rdp01 check
        server 192.168.100.22 192.168.100.22:3389 weight 1 cookie rdp02 check

    listen jms-https
        bind *:443
        balance roundrobin
        option httpchk GET /api/health/
        default-server inter 2s rise 2 fall 3
        server 192.168.100.21 192.168.100.21:443 weight 1 cookie https01 check
        server 192.168.100.22 192.168.100.22:443 weight 1 cookie https02 check
    ```


### 2.3 Start HAProxy
!!! tip ""
    ```sh
    sudo systemctl enable haproxy
    sudo systemctl start haproxy
    sudo systemctl status haproxy
    ```

## 3 Configure Firewall
!!! tip ""
    ```sh
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 2222/tcp
    sudo ufw allow 3389/tcp
    sudo ufw allow 8080/tcp
    sudo ufw reload
    ```
