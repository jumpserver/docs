# 启用 IPV6 支持

!!! info "说明"
    - 基于 NAT
    - 请使用最新版本的 Docker

!!! tip ""
    ```sh
    cd /opt/jumpserver-installerer-{{ jumpserver.version }}
    ./jmsctl.sh down
    ```
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim hl_lines="3"
    ## IPV6
    DOCKER_SUBNET_IPV6=fc00:200::/24
    USE_IPV6=1
    ```
    ```sh
    vi /etc/docker/daemon.json
    ```
    ```json
    # 加入下面内容，注意不要覆盖已有的内容
    {
      "ipv6": true,
      "fixed-cidr-v6": "fc00:100::/24",
      "experimental": true,
      "ip6tables": true,
    }
    ```
    ```sh
    systemctl restart docker
    ```
    ```sh
    ./jmsctl.sh start
    ```

!!! tip "修改完成后的 daemon.json 供参考"
    ```json
    {
        "data-root": "/var/lib/docker",
        "experimental": true,
        "fixed-cidr-v6": "fc00:1010:1111:100::/64",
        "ip6tables": true,
        "ipv6": true,
        "live-restore": true,
        "log-driver": "json-file",
        "log-opts": { "max-file": "3", "max-size": "10m" },
        "registry-mirrors": [ "https://hub-mirror.c.163.com", "http://f1361db2.m.daocloud.io" ]
    }
    ```
