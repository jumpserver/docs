分布式部署文档 - mariadb 部署
----------------------------------------------------

说明
~~~~~~~
-  # 开头的行表示注释
-  $ 开头的行表示需要执行的命令
-  > 开头的行表示需要在数据库中执行

环境
~~~~~~~

-  系统: CentOS 7
-  服务: MariaDB Server

+----------+------------+-----------------+---------------+------------------------+
| Protocol | ServerName |        IP       |      Port     |         Used By        |
+==========+============+=================+===============+========================+
|    TCP   |   Mariadb  | 192.168.100.10  |      3306     |           Core         |
+----------+------------+-----------------+---------------+------------------------+

开始安装
~~~~~~~~~~~~

.. code-block:: shell

    $ yum upgrade -y
    $ yum -y install epel-release wget

    # 安装 MariaDB
    $ yum install -y mariadb mariadb-server mariadb-devel

    # 设置 Firewalld 和 Selinux
    $ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="3306" accept"
    # 192.168.100.0/24 为整个 JumpServer 网络网段, 这里就偷懒了, 自己根据实际情况修改即可

    $ firewall-cmd --reload

.. code-block:: shell

    # 启动 MariaDB

    $ systemctl enable mariadb
    $ systemctl start mariadb

.. code-block:: shell

    # 创建 JumpServer 数据库及授权
    $ mysql -uroot
    > create database jumpserver default charset 'utf8' collate 'utf8_bin';
    > grant all on jumpserver.* to 'jumpserver'@'192.168.100.%' identified by 'weakPassword';
    > flush privileges;
    > quit
