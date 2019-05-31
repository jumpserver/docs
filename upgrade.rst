更新升级
-------------

1.4.8 升级到最新版本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Jumpserver**

.. code-block:: shell

    $ cd /opt/jumpserver
    $ source /opt/py3/bin/activate
    $ ./jms stop
    $ git checkout master
    $ git pull
    $ pip install -r requirements/requirements.txt

    $ cd ../
    $ ./jms start all -d

**Luna**

说明: 直接下载 release 包

.. code-block:: shell

    $ cd /opt
    $ rm -rf luna luna.tar.gz
    $ wget https://github.com/jumpserver/luna/releases/download/1.5.0/luna.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/luna/1.5.0/luna.tar.gz

    $ tar xf luna.tar.gz
    $ chown -R root:root luna

    # 注意把浏览器缓存清理下

**Docker Coco Guacamole**

说明: Docker 部署的 coco 与 guacamole 升级说明

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉所有组件
    $ docker stop jms_coco
    $ docker stop jms_guacamole
    $ docker rm jms_coco
    $ docker rm jms_guacamole
    $ docker pull jumpserver/jms_coco:1.5.0
    $ docker pull jumpserver/jms_guacamole:1.5.0
    $ docker run --name jms_coco -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN jumpserver/jms_coco:1.5.0
    $ docker run --name jms_guacamole -d -p 8081:8081 -e JUMPSERVER_SERVER=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN jumpserver/jms_guacamole:1.5.0

    # 到 Web 会话管理 - 终端管理 查看组件是否已经在线
