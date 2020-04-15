升级常见问题
---------------------

**请务必认真详细阅读每一个文字并理解后才能操作升级事宜**

1. git pull 时提示 error: Your local changes to the following file would be overwritten by merge

.. code-block:: shell

    # 这是因为你修改了本地文件导致代码冲突, 请确认修改的内容并手动进行合并, 请谨慎处理

    # 如果希望保留你的改动 (不推荐)
    $ git stash
    $ git pull
    $ git stash pop
    # 可以使用git diff -w +文件名 来确认代码自动合并的情况

    # 或者放弃本地的修改 (推荐)
    # 可以使用 git checkout + 文件名来撤销文件的更改
    # 如 git checkout apps/jumpserver/settings.py  # 这里的 apps/jumpserver/settings.py 就是报错的路径文件

    # 或者取消所有更改, (谨慎执行)
    $ git reset --hard
    $ git pull

2. sh make_migrations.sh 时提示 1064, "You have an error in your SQL syntax; check the manual than corresponds to your MySql server version for the right syntax to use near '(6) NOT NULL'"

.. code-block:: vim

    # 这是因为你的数据库版本不对, 从 1.4.x 版本开始 mysql 版本需要大于等于 5.6, mariadb 版本需要大于等于 5.5.6
    # 请更换数据库重新操作

3. 数据库表结构不完整导致升级失败的, 按如下内容进行处理

.. code-block:: shell

    # 一定要知道自己升级之前的版本, 记住是升级之前, 也可以通过 web 页面的右下角来查看当前版本信息

    # 备份当前版本数据库, 忽略 django_migrations 表
    $ mysqldump -uroot -p jumpserver --ignore-table=jumpserver.django_migrations > /opt/jumpserver.sql

    # 重命名 JumpServer 目录
    $ mv /opt/jumpserver /opt/jumpserver_bak

    # 重新 clone 代码
    $ cd /opt
    $ git clone https://github.com/jumpserver/jumpserver.git
    $ cd jumpserver

    # 检出你之前的版本, 比如之前的版本是1.4.0
    $ git checkout 1.4.0  # 1.4.0 表示版本号, 自己手动更换成你当前的版本, 如 1.3.1 则输入 git checkout 1.3.1

    # 依赖安装
    $ source /opt/py3/bin/activate
    $ yum -y install $(cat /opt/jumpserver/requirements/rpm_requirements.txt)
    $ pip install wheel
    $ pip install --upgrade pip setuptools
    $ pip install -r /opt/jumpserver/requirements/requirements.txt

    # 重新创建一个数据库
    $ mysql -uroot
    > create database jumpserver01 default charset 'utf8' collate utf8_bin;
    > grant all on jumpserver01.* to 'jumpserver01'@'127.0.0.1' identified by 'weakPassword';
    > flush privileges;
    > quit

    # 修改配置文件
    $ cp /opt/jumpserver_bak/config.py /opt/jumpserver/
    $ vim /opt/jumpserver/config.py
    DB_ENGINE = 'mysql'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'jumpserver01'
    DB_PASSWORD = 'weakPassword'
    DB_NAME = 'jumpserver01'

    # 初始化数据库(版本大于 1.4.5 请跳过此步骤)
    $ cd /opt/jumpserver/utils  # 当前版本大于 1.4.5 请跳过此命令
    $ sh make_migrations.sh  # 当前版本大于 1.4.5 请跳过此命令

    # 初始化数据库(版本大于 1.4.5 请执行下面命令初始化数据库)
    $ ./jms start  # 如果未报错, 全部提示 ok 然后 ctrl + c 退出

    # 确定初始化没有错误, 把旧的数据库导入
    $ mysql -uroot
    > use jumpserver01;
    > source /opt/jumpserver.sql

    # 启动 jumpserver, 确定没有错误
    $ cd /opt/jumpserver
    $ ./jms start

    # 打开 web 页面检查是否都正常

    $ 参考升级文档继续升级到最新版本即可

    # 删除原数据库命令(谨慎操作)
    $ mysql -uroot
    > drop database jumpserver;
    > quit
