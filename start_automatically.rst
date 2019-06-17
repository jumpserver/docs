开机自启
------------------

Docker 组件部署自启 (Centos 7)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 极速安装适用 (CentOS 7)
- 一体化部署适用 (CentOS 7)

.. code-block:: vim

    # Jumpserver
    $ vi /usr/lib/systemd/system/jms.service
    [Unit]
    Description=jms
    After=network.target mariadb.service redis.service docker.service
    Wants=mariadb.service redis.service docker.service

    [Service]
    Type=forking
    Environment="PATH=/opt/py3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
    ExecStart=/opt/jumpserver/jms start all -d
    ExecReload=
    ExecStop=/opt/jumpserver/jms stop

    [Install]
    WantedBy=multi-user.target

.. code-block:: vim

    # 启动
    $ vi /opt/start_jms.sh

    #!/bin/bash
    set -e

    export LANG=zh_CN.UTF-8

    systemctl start jms
    docker start jms_koko
    docker start jms_guacamole

    exit 0

.. code-block:: vim

    # 停止
    $ vi /opt/stop_jms.sh

    #!/bin/bash
    set -e

    export LANG=zh_CN.UTF-8

    docker stop jms_koko
    docker stop jms_guacamole
    systemctl stop jms

    exit 0

.. code-block:: shell

    # 写入 rc.local
    $ chmod +x /etc/rc.d/rc.local
    $ if [ "$(cat /etc/rc.local | grep start_jms.sh)" == "" ]; then echo "sh /opt/start_jms.sh" >> /etc/rc.local; fi

Docker 组件部署自启 (Ubuntu 18)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 一体化部署适用 (Ubuntu 18)

.. code-block:: vim

    # Jumpserver
    $ vi /lib/systemd/system/jms.service
    [Unit]
    Description=jms
    After=network.target mysql.service redis-server.service docker.service
    Wants=mysql.service redis-server.service docker.service

    [Service]
    Type=forking
    Environment="PATH=/opt/py3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
    ExecStart=/opt/jumpserver/jms start all -d
    ExecReload=
    ExecStop=/opt/jumpserver/jms stop

    [Install]
    WantedBy=multi-user.target

.. code-block:: vim

    # 启动
    $ vi /opt/start_jms.sh

    #!/bin/bash
    set -e

    export LANG=zh_CN.utf8

    systemctl start jms
    docker start jms_koko
    docker start jms_guacamole

    exit 0

.. code-block:: vim

    # 停止
    $ vi /opt/stop_jms.sh

    #!/bin/bash
    set -e

    export LANG=zh_CN.utf8

    docker stop jms_koko
    docker stop jms_guacamole
    systemctl stop jms

    exit 0

.. code-block:: shell

    # 写入 rc.local
    $ chmod +x /etc/rc.d/rc.local
    $ if [ "$(cat /etc/rc.local | grep start_jms.sh)" == "" ]; then echo "sh /opt/start_jms.sh" >> /etc/rc.local; fi
