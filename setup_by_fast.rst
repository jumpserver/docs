极速安装
--------

.. toctree::
   :maxdepth: 1

   setup_by_localcloud

**说明**

- 全新安装的 Centos7 (7.x)
- 需要连接 互联网
- 使用 root 用户执行

脚本做了一定的容错, 可以多次执行, 安装完成后请勿再次执行

**Koko、Guacamole 容器化部署(推荐)**

.. code-block:: shell

    $ cd /opt
    $ yum -y install wget
    $ wget -O /opt/jms_install.sh https://demo.jumpserver.org/download/jms_install.sh
    $ sh jms_install.sh

**Koko、Guacamole 正常部署(仅测试环境使用)**

.. code-block:: shell

    $ yum -y install wget
    $ cd /opt
    $ wget -O jms_localinstall.sh https://demo.jumpserver.org/download/jms_localinstall.sh
    $ sh jms_localinstall.sh
