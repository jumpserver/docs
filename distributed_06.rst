分布式部署文档 - koko 部署
----------------------------------------------------

说明
~~~~~~~
-  # 开头的行表示注释
-  $ 开头的行表示需要执行的命令

环境
~~~~~~~

-  系统: CentOS 7
-  IP: 192.168.100.40

+----------+------------+-----------------+---------------+------------------------+
| Protocol | ServerName |        IP       |      Port     |         Used By        |
+==========+============+=================+===============+========================+
|    TCP   |    koko    | 192.168.100.40  |   2222, 5000  |         Tengine        |
+----------+------------+-----------------+---------------+------------------------+
|    TCP   |    koko    | 192.168.100.41  |   2222, 5000  |         Tengine        |
+----------+------------+-----------------+---------------+------------------------+

开始安装
~~~~~~~~~~~~

.. code-block:: shell

    # 升级系统
    $ yum upgrade -y

    # 设置防火墙, 开放 2222 5000 端口 给 Tengine 访问
    $ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="2222" accept"
    $ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="5000" accept"
    $ firewall-cmd --reload

    # 安装 docker
    $ yum install -y yum-utils device-mapper-persistent-data lvm2 wget
    $ yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    $ yum makecache fast
    $ yum -y install docker-ce
    $ mkdir /etc/docker
    $ wget -O /etc/docker/daemon.json http://demo.jumpserver.org/download/docker/daemon.json
    $ systemctl enable docker
    $ systemctl start docker

    # 通过 docker 部署
    $ docker run --name jms_koko -d \
        -p 2222:2222 \
        -p 5000:5000 \
        -e CORE_HOST=http://192.168.100.100 \
        -e BOOTSTRAP_TOKEN=你的token \
        -e LOG_LEVEL=ERROR \
        -e REDIS_HOST=192.168.100.20 \
        -e REDIS_PORT=6379 \
        -e REDIS_PASSWORD=weakPassword \
        jumpserver/jms_koko:1.5.8

    # 访问 http://192.168.100.100/terminal/terminal/ 检查 koko 注册

多节点部署
~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # 登录到新的节点服务器, 前面安装 docker 都是一样的, 这里就懒得写了
    $ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="2222" accept"
    $ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="5000" accept"
    $ firewall-cmd --reload

    $ docker run --name jms_koko -d \
        -p 2223:2222 \
        -p 5001:5000 \
        -e CORE_HOST=http://192.168.100.100 \
        -e BOOTSTRAP_TOKEN=你的token \
        -e LOG_LEVEL=ERROR \
        -e REDIS_HOST=192.168.100.20 \
        -e REDIS_PORT=6379 \
        -e REDIS_PASSWORD=weakPassword \
        jumpserver/jms_koko:1.5.8

    # 访问 http://192.168.100.100/terminal/terminal/ 检查 koko 注册
