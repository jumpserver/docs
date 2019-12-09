Jms_koko 常见问题
-----------------------

- Jms_koko 是指 https://github.com/jumpserver/koko 项目
- Jms_koko 默认的路径为 /opt/koko 或者 /opt/kokodir

1. Jms_koko 启动异常或者启动失败

.. code-block:: shell

    - 提示 [ERRO] POST http://127.0.0.1:8080/api/v2/terminal/terminal-registrations/ failed, get code: 403, {"detail":"身份认证信息未提供。"}
    # 这是因为 koko 里面的 BOOTSTRAP_TOKEN 与 jumpserver 的 BOOTSTRAP_TOKEN 不一样

    $ cat /opt/jumpserver/config.yml | grep BOOTSTRAP_TOKEN

    # 首先到 web - 会话管理 - 终端管理 里面删除 koko 的注册 ( 在线显示红色的那个 )

    # 如果是极速安装部署的 koko
    $ docker stop jms_koko
    $ docker rm jms_koko
    $ Server_IP=`ip addr | grep 'state UP' -A2 | grep inet | egrep -v '(127.0.0.1|inet6|docker)' | awk '{print $2}' | tr -d "addr:" | head -n 1 | cut -d / -f1`
    $ docker run --name jms_koko -d -p 2222:2222 -p 127.0.0.1:5000:5000 -e CORE_HOST=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN --restart=always jumpserver/jms_koko:1.5.5

    # 如果是正常部署的 koko
    $ rm /opt/kokodir/keys/*
    $ vi /opt/kokodir/config.yml

    ...

    # 修改下面 BOOTSTRAP_TOKEN 与 jumpserver 一致
    BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>

    ...

    $ ./koko

    - 提示 [ERRO] POST http://127.0.0.1:8080/api/v2/terminal/terminal-registrations/ failed, get code: 400, {"name":["名称重复"]}
    # 这个问题一般只会在正常部署中出现, 原因一般是 access_key 丢失导致的
    $ vi /opt/kokodir/config.yml

    ...

    # 项目名称, 会用来向Jumpserver注册, 识别而已, 不能重复
    # NAME: {{ Hostname }}
    NAME: koko01  # 把 koko01 换成你想要的名字

    ...

    $ ./koko

2. SSH 无法连接到 Jms_koko

.. code-block:: shell

    # koko 默认的 ssh 端口是 2222
    $ ssh admin@Jumpserver_IP -p2222

3. 修改 sftp 默认的路径

.. code-block:: shell

    $ vi /opt/kokodir/config.yml

    # SFTP的根目录, 可选 /tmp, Home其他自定义目录
    # SFTP_ROOT: /tmp
    SFTP_ROOT: /
    # 如果想使用用户自己的Home目录, 直接 SFTP_ROOT: Home 即可

    # SFTP是否显示隐藏文件
    # SFTP_SHOW_HIDDEN_FILE: false

    - 如果你的 koko 是 docker 方式部署
    $ docker exec -it jms_koko /bin/sh
    $ if [ ! -f "/opt/koko/config.yml" ]; then cp /opt/koko/config_example.yml /opt/koko/config.yml; sed -i '5d' /opt/koko/config.yml; sed -i "5i CORE_HOST: $CORE_HOST" /opt/koko/config.yml; sed -i "s/BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/koko/config.yml; sed -i "s/# LOG_LEVEL: INFO/LOG_LEVEL: ERROR/g" /opt/koko/config.yml; fi

    $ vi config.yml

    # SFTP的根目录, 可选 /tmp, Home其他自定义目录
    # SFTP_ROOT: /tmp
    SFTP_ROOT: /

    # SFTP是否显示隐藏文件
    # SFTP_SHOW_HIDDEN_FILE: false
