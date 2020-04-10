极速安装
--------

**说明**

- 全新安装的 Centos7 (7.x)
- 需要连接 互联网
- 使用 root 用户执行

.. code-block:: shell

    $ cd /opt
    $ yum -y install wget git
    $ git clone --depth=1 https://github.com/jumpserver/setuptools.git
    $ cd setuptools
    $ cp config_example.conf config.conf
    $ vi config.conf

    # Install
    $ ./jmsctl.sh install

    # Help
    $ ./jmsctl.sh -h

.. code-block:: shell

    # 如果网络有问题无法连接到 github
    $ wget -O /opt/setuptools.tar.gz http://demo.jumpserver.org/download/setuptools.tar.gz
    $ cd /opt
    $ tar -xf setuptools.tar.gz
    $ cd setuptools
    $ git pull
    $ ./jmsctl.sh -h
