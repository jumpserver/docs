分布式部署文档 - redis 部署
----------------------------------------------------

说明
~~~~~~~
-  # 开头的行表示注释
-  $ 开头的行表示需要执行的命令

环境
~~~~~~~

-  系统: CentOS 7
-  IP: 192.168.100.20

+----------+------------+-----------------+---------------+------------------------+
| Protocol | ServerName |        IP       |      Port     |         Used By        |
+==========+============+=================+===============+========================+
|    TCP   |    Redis   | 192.168.100.20  |      6379     |           Core         |
+----------+------------+-----------------+---------------+------------------------+

注意: Redis 的数据库 3,4,5 被 Core 使用, 6 被 Koko 使用

开始安装
~~~~~~~~~~~~

.. code-block:: shell

    # 升级系统
    $ yum upgrade -y

    # 安装 redis 服务
    $ yum install -y install epel-release
    $ yum install -y redis

    # 设置防火墙, 开放 6379 端口 给 Core Koko 访问
    $ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="6379" accept"
    $ firewall-cmd --reload

    # 设置 Redis 自启
    $ systemctl enable redis

.. code-block:: vim

    # 修改 redis 配置文件
    $ vi /etc/redis.conf

    ...

    # bind 127.0.0.1  # 注释这行, 新增如下内容
    bind 0.0.0.0
    requirepass weakPassword  # redis 连接密码
    maxmemory-policy allkeys-lru  # 清理策略, 优先移除最近未使用的key

    ...

.. code-block:: shell

    # 启动 Redis
    $ systemctl start redis
