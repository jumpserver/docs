更新升级
-------------

1.4.8 升级到 1.5.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Jumpserver**

.. code-block:: shell

    $ cd /opt/jumpserver
    $ source /opt/py3/bin/activate
    $ ./jms stop
    $ git fetch
    $ git checkout 1.5.2
    $ pip install -r requirements/requirements.txt

    $ ./jms start -d

**Luna**

说明: 直接下载 release 包

.. code-block:: shell

    $ cd /opt
    $ rm -rf luna luna.tar.gz
    $ wget https://github.com/jumpserver/luna/releases/download/1.5.2/luna.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/luna/1.5.2/luna.tar.gz

    $ tar xf luna.tar.gz
    $ chown -R root:root luna

    # 注意把浏览器缓存清理下

**Koko**

说明: 在之后的版本中, koko 将会取带 coco

.. code-block:: shell

    $ cd /opt

    $ wget https://github.com/jumpserver/koko/releases/download/1.5.2/koko-master-6d4e69b-linux-amd64.tar.gz

    # 如果网络有问题导致下载无法完成可以使用下面地址
    $ wget https://demo.jumpserver.org/download/koko/1.5.2/koko-master-6d4e69b-linux-amd64.tar.gz


    $ tar xf koko-master-6d4e69b-linux-amd64.tar.gz
    $ chown -R root:root kokodir
    $ cd kokodir
    $ cp config_example.yml config.yml
    $ sed -i "s/BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/kokodir/config.yml
    $ sed -i "s/# LOG_LEVEL: INFO/LOG_LEVEL: ERROR/g" /opt/kokodir/config.yml
    $ vim config.yml  # 配置文件与 coco 一样

    $ ./koko

docker 部署的 koko

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 koko 组件
    $ docker stop jms_koko
    $ docker rm jms_koko
    $ docker pull jumpserver/jms_koko:1.5.2
    $ docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> jumpserver/jms_koko:1.5.2
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_koko -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 jumpserver/jms_koko:1.5.2

**Coco**

说明: 在未来的版本中, coco 组件将会被 koko 组件取代, 推荐使用 koko

.. code-block:: shell

    $ cd /opt/coco
    $ source /opt/py3/bin/activate
    $ ./cocod stop
    $ git pull
    $ pip install -r requirements/requirements.txt
    $ ./cocod start -d

docker 部署的 coco

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 coco 组件
    $ docker stop jms_coco
    $ docker rm jms_coco
    $ docker pull jumpserver/jms_coco:1.5.2
    $ docker run --name jms_coco -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> jumpserver/jms_coco:1.5.2
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_coco -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 jumpserver/jms_coco:1.5.2

**Guacamole**

正常部署的 guacamole

.. code-block:: shell

    $ /etc/init.d/guacd stop
    $ sh /config/tomcat8/bin/shutdown.sh
    $ cd /opt/docker-guacamole
    $ git pull
    $ cd /config
    $ rm -rf /cofig/tomcat8

    # 访问 https://tomcat.apache.org/download-90.cgi 下载最新的 tomcat9
    $ wget http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-9/v9.0.22/bin/apache-tomcat-9.0.22.tar.gz
    $ tar xf apache-tomcat-9.0.22.tar.gz
    $ mv apache-tomcat-9.0.22 tomcat9
    $ rm -rf /config/tomcat9/webapps/*
    $ sed -i 's/Connector port="8080"/Connector port="8081"/g' /config/tomcat9/conf/server.xml
    $ echo "java.util.logging.ConsoleHandler.encoding = UTF-8" >> /config/tomcat9/conf/logging.properties
    $ ln -sf /opt/docker-guacamole/guacamole-1.0.0.war /config/tomcat9/webapps/ROOT.war
    $ ln -sf /opt/docker-guacamole/guacamole-auth-jumpserver-1.0.0.jar /config/guacamole/extensions/guacamole-auth-jumpserver-1.0.0.jar
    $ ln -sf /opt/docker-guacamole/root/app/guacamole/guacamole.properties /config/guacamole/guacamole.properties

    $ /etc/init.d/guacd start
    $ sh /config/tomcat9/bin/startup.sh

docker 部署的 guacamole

.. code-block:: shell

    # 先到 Web 会话管理 - 终端管理 删掉 guacamole 组件
    $ docker stop jms_guacamole
    $ docker rm jms_guacamole
    $ docker pull jumpserver/jms_guacamole:1.5.2

    $ docker run --name jms_guacamole -d -p 8081:8081 -e JUMPSERVER_SERVER=http://<Jumpserver_url> -e BOOTSTRAP_TOKEN=<Jumpserver_BOOTSTRAP_TOKEN> jumpserver/jms_guacamole:<Tag>
    # <Jumpserver_url> 为 jumpserver 的 url 地址, <Jumpserver_BOOTSTRAP_TOKEN> 需要从 jumpserver/config.yml 里面获取, 保证一致, <Tag> 是版本
    # 例: docker run --name jms_guacamole -d -p 8081:8081 -e JUMPSERVER_SERVER=http://192.168.244.144:8080 -e BOOTSTRAP_TOKEN=abcdefg1234 jumpserver/jms_guacamole:1.5.2

到 Web 会话管理 - 终端管理 查看组件是否已经在线
