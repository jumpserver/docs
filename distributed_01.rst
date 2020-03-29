分布式部署文档 - NFS 部署
----------------------------------------------------

说明
~~~~~~~
-  # 开头的行表示注释
-  $ 开头的行表示需要执行的命令

环境
~~~~~~~

-  系统: CentOS 7
-  IP: 192.168.100.99

+----------+------------+-----------------+------------------------+
| Protocol | ServerName |        IP       |         Used By        |
+==========+============+=================+========================+
|    TCP   |     NFS    |  192.168.100.99 |       Core, Tengine    |
+----------+------------+-----------------+------------------------+

开始安装
~~~~~~~~~~~~

.. code-block:: shell

    $ yum upgrade -y
    $ yum -y install epel-release wget

    # 部署 NFS
    $ yum -y install nfs-utils rpcbind
    $ systemctl enable rpcbind nfs-server nfs-lock nfs-idmap
    $ systemctl start rpcbind nfs-server nfs-lock nfs-idmap

    # 设置防火墙
    $ firewall-cmd --add-service=nfs --permanent --zone=public
    $ firewall-cmd --add-service=mountd --permanent --zone=public
    $ firewall-cmd --add-service=rpc-bind --permanent --zone=public
    $ firewall-cmd --reload

    # 创建 NFS 共享目录, 此共享目录存放 jumpserver 的录像及任务结果
    $ mkdir /data
    $ chmod 777 -R /data

.. code-block:: vim

    # 设置 NFS 访问权限, /data 是刚才创建的将被共享的目录, 192.168.100.* 表示整个 192.168.100.* 的资产都有括号里面的权限
    # 也可以写具体的授权对象 /data 192.168.100.30(rw,sync,no_root_squash) 192.168.100.31(rw,sync,no_root_squash)
    $ vi /etc/exports

    /data 192.168.100.*(rw,sync,all_squash,anonuid=0,anongid=0)

.. code-block:: vim

    # 使 exports 生效
    $ exportfs -a
