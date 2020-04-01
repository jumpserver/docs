极速安装
--------

**说明**

- 全新安装的 Centos7 (7.x)
- 需要连接 互联网
- 使用 root 用户执行

.. code-block:: shell

    $ cd /opt
    $ yum -y install wget git
    $ git clone --depth=1 https://github.com/wojiushixiaobai/jms_install.git
    $ cd jms_install
    $ cp config_example.conf config.conf
    $ vi config.conf
    $ chmod +x ./jmsctl.sh

    # Install
    $ ./jmsctl.sh install

    # Help
    $ ./jmsctl.sh -h

.. code-block:: shell

    # 如果网络有问题无法连接到 github
    $ wget -O /opt/jms_install.tar.gz http://demo.jumpserver.org/download/jms_install.tar.gz
    $ cd /opt
    $ tar -xf jms_install.tar.gz
    $ cd jms_install
    $ git pull
    $ ./jmsctl.sh -h
