安装过程中常见的问题
----------------------------

1. git clone 提示 ssl 错误

.. code-block:: vim

    # 一般是由于时间不同步, 或者网络有问题导致的
    # 可以尝试下载 releases 包

2. pip install 提示 ssl 错误

.. code-block:: vim

    # 参考第一条解决

3. pip install 提示 download 错误或者卡在某个依赖很久不动

.. code-block:: vim

    # 一般是由于网络不好, 导致下载文件失败, 重新执行命令即可
    # 如果多次重试均无效, 请更换网络环境
    $ vim ~/.pydistutils.cfg
    [easy_install]
    index_url = https://mirrors.aliyun.com/pypi/simple/

4. pip install 提示 Could not find a version that satisfies the requirement xxxxxx==x.x.xx(版本)

.. code-block:: shell

    # 一般是由于镜像源未同步, -i 指定官方源即可, 如：
    $ pip install -r requirement.txt -i https://pypi.org/simple
    $ pip install xxxxx==x.x.xx -i https://pypi.org/simple

5. pip install 提示 install for mysqlclient ... error /usr/bin/ld: 找不到 -lmariadb

.. code-block:: shell

    # 如果是 Mariadb 大于 10 版本
    $ yum install MariaDB-shared

6. sh make_migrations.sh 时报错 from config import config as CONFIG File "/opt/jumpserver/config.yml", line 38

.. code-block:: vim

    # 这是由于 config.yml 里面的内容格式不对, 请参考安装文档的说明, 把提示的内容与上一行对齐即可

7. sh make_migrations.sh 时报错 Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?

.. code-block:: shell

    # 一般是由于 py3 环境未载入
    $ source /opt/py3/bin/activate

    # 看到下面的提示符代表成功, 以后运行 Jumpserver 都要先运行以上 source 命令, 以下所有命令均在该虚拟环境中运行
    (py3) [root@localhost py3]

    # 如果已经在 py3 虚拟环境下, 任然报 Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?
    $ cd /opt/jumpserver/requirements
    $ pip install -r requirements.txt
    # 然后重新执行 sh make_migrations.sh

8.  sh make_migrations.sh 报错 CommandError: Conflicting migrations detected; multiple ... django_celery_beat ...

.. code-block:: shell

    # 这是由于 django-celery-beat老版本有bug引起的
    $ rm -rf /opt/py3/lib/python3.6/site-packages/django_celery_beat/migrations/
    $ pip uninstall django-celery-beat
    $ pip install django-celery-beat

9. 执行 ./jms start 后一直卡在 beat: Waking up in 1.00 minute.

.. code-block:: vim

    # 如果没有error提示进程无法启动, 那么这是正常现象
    # 如果不想在前台启动, 可以使用 ./jms start -d 在后台启动

10. 执行 ./jms start 后提示 xxx is stopped

.. code-block:: shell

    # Error: xxx start error
    # xxx is stopped
    $ ./jms restart xxx  # 如 ./jms restart gunicorn

    # 如果经常这样, 可能是硬件配置不够, 可以尝试升级硬件

11. 执行 ./jms start 后提示 WARNINGS: ?: (mysql.W002) MySQL Strict Mode is not set for database connection 'default' ...

.. code-block:: vim

    # 这是严格模式的警告, 可以参考后面的url解决, 或者忽略

12. 启动 Jumpserver 报错 Error: expected '<document start>', but found '<scalar>'

.. code-block:: vim

    # 这是因为你的 config.yml 文件格式有误
    # 常见的错误就是字段为空和: 后面少一个空格, 参考下面, 请勿照抄
    # SECRET_KEY: 5RLbBjm8AkMSvnft...  # 不要忽略: 后面的空格, 不支持纯数字
    # BOOTSTRAP_TOKEN: ihR4WG4gRShCnpQL...  # 不要忽略: 后面的空格, 不支持纯数字
    # DB_PASSWORD: '123456'  # 密码纯数字用单引号括起来
    # DB_PASSWORD: cPzxaiUAtA5IkdT2...  # 非纯数字可以不用单引号
    # REDIS_PASSWORD: '888888'  # 密码纯数字用单引号括起来
    # REDIS_PASSWORD: Ma5bzA3gVK5oY17l...  # 非纯数字可以不用单引号

13. 启动 jumpserver 后, 访问 8080 端口页面显示不正常

.. code-block:: vim

    # 这是因为你在 config.yml 里面设置了 DEBUG: false
    # 跟着教程继续操作, 后面搭建 nginx 代理即可正常访问

14. 通过 nginx 代理的端口访问 jumpserver 页面显示不正常

.. code-block:: nginx

    # 这是因为你没有按照教程进行安装, 修改了安装目录, 需要在 nginx 的配置文件里面修改资源路径
    $ vi /etc/nginx/conf.d/jumpserver.conf

    ...

    server {
        listen 80;  # 代理端口, 以后将通过此端口进行访问, 不再通过8080端口

        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
        }

        location /media/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
        }

        location /static/ {
            root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        }

        location /koko/ {
            proxy_pass       http://localhost:5000/;  # 如果koko安装在别的服务器, 请填写它的ip
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /guacamole/ {
            proxy_pass       http://localhost:8081/;  # 如果guacamole安装在别的服务器, 请填写它的ip
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            access_log off;
            client_max_body_size 100m;  # Windows 文件上传大小限制
        }

        location / {
            proxy_pass http://localhost:8080;  # 如果jumpserver安装在别的服务器, 请填写它的ip
        }
    }

    ...

15. 访问 luna 页面提示 Luna是单独部署的一个程序, 你需要部署luna, koko, 配置nginx做url分发...

.. code-block:: vim

    # 请通过 nginx 代理的端口访问 jumpserver 页面, 不要再直接访问 8080 端口

16. 启动 koko 或者 koko 提示 "name":["名称重复"]

.. code-block:: vim

    $ vi config.yml

    NAME: koko01  # 把 koko01 换成你想要的名字, 注意默认是 # NAME: {{ Hostname }}, 注意去掉注释#

17. 启动 koko 提示 "detail":"身份认证信息未提供"

.. code-block:: vim

    $ vi config.yml

    BOOTSTRAP_TOKEN: xxxxxx  # 把 xxxxxx 换成跟 jumpserver/config.yml 的 BOOTSTRAP_TOKEN: 一样的内容

    # 如果是 guacamole 提示 "detail":"身份认证信息未提供"
    $ env | grep BOOTSTRAP_TOKEN
    $ cat /opt/jumpserver/config.yml | grep BOOTSTRAP_TOKEN

    # 对比, 如果不一致请修改 ~/.bashrc 文件里面的内容
    $ vi ~/.bashrc

    export BOOTSTRAP_TOKEN=xxxxxx  # 把 xxxxxx 换成跟 jumpserver/config.yml 的 BOOTSTRAP_TOKEN: 一样的内容

    # 如果是 docker 部署出现的
    $ docker stop jms_koko
    $ docker stop jms_guacamole
    $ docker rm jms_koko
    $ docker rm jms_guacamole

    # 重新 docker run 即可, 注意 BOOTSTRAP_TOKEN 需要跟 jumpserver/config.yml 的 BOOTSTRAP_TOKEN: 一样
