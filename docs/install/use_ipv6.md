# 启用 IPV6 支持

!!! info "说明"
    - 基于 NAT

!!! tip ""
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim hl_lines="3"
    ## IPV6
    DOCKER_SUBNET_IPV6=2001:db8:10::/64
    USE_IPV6=1
    ```
    ```sh
    cd /opt/jumpserver-installer-{{ jumpserver.version }}
    ./jmsctl.sh down
    ```
    ```sh
    firewall-cmd --add-masquerade --permanent
    firewall-cmd --reload
    ```
    ```sh
    systemctl restart docker
    ```
    ```sh
    ./jmsctl.sh start
    ```

??? warning "如果按照这样设置后无法正常连接 ipv6 资产, 请查看此处的帮助文档"
    - VMware 虚拟机可能会出现此问题, 可以先通过关闭防火墙的形式解决
    - 我们会继续查找原因, 后续会更新在文档里面

    ```sh
    systemctl stop firewalld
    systemctl restart docker
    ```
