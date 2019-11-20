sftp 使用说明
-------------------------------------------------------
在Windows上使用 sftp 工具传输文件到 Linux 系统, 默认的上传目录在 /tmp

.. code-block:: shell

    # 连接成功后, 可以看到当前拥有权限的资产, 打开资产, 然后选择系统用户, 即可到资产的 /tmp 目录
    $ sftp -P2222 admin@192.168.244.144  # Linux 语法
    $ sftp 2222 admin@192.168.244.144  # xshell 语法

    $ ls 列出资产目录
    $ cd 你的资产
    $ ls 列出你的系统用户
    $ cd 你的系统用户
    # 此处即是当前资产的 home 目录

如果需要修改 /tmp 为其他目录

.. code-block:: vim

    $ vi /opt/kokodir/config.yml

    # SFTP的根目录, 可选 /tmp, Home其他自定义目录
    # SFTP_ROOT: /tmp
    SFTP_ROOT: /

    # SFTP是否显示隐藏文件
    # SFTP_SHOW_HIDDEN_FILE: false

如果你的 koko 是 docker 方式部署

.. code-block:: vim

    $ docker exec -it jms_koko /bin/sh
    $ if [ ! -f "/opt/koko/config.yml" ]; then cp /opt/koko/config_example.yml /opt/koko/config.yml; sed -i '5d' /opt/koko/config.yml; sed -i "5i CORE_HOST: $CORE_HOST" /opt/koko/config.yml; sed -i "s/BOOTSTRAP_TOKEN: <PleasgeChangeSameWithJumpserver>/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/koko/config.yml; sed -i "s/# LOG_LEVEL: INFO/LOG_LEVEL: ERROR/g" /opt/koko/config.yml; fi

    $ vi config.yml

    # SFTP的根目录, 可选 /tmp, Home其他自定义目录
    # SFTP_ROOT: /tmp
    SFTP_ROOT: /

    # SFTP是否显示隐藏文件
    # SFTP_SHOW_HIDDEN_FILE: false
