FAQ
==========
.. toctree::
   :maxdepth: 1

   MFA 使用说明 <faq_mfa.rst>
   LDAP 使用说明 <faq_ldap.rst>
   Docker 使用说明 <faq_docker.rst>
   Radius 使用说明 <faq_radius.rst>
   Jms_core 常见问题 <faq_core.rst>
   Jms_koko 常见问题 <faq_koko.rst>
   Jms_guacamole 常见问题 <faq_guacamole.rst>
   Windows SSH 设置说明 <faq_rdp.rst>
   升级过程 常见问题 <faq_upgrade.rst>
   Nginx SSL 使用说明 <faq_nginx.rst>
   Firewalld 使用说明 <faq_firewalld.rst>
   添加组织 及 组织管理员说明 <faq_org.rst>

其他问题
~~~~~~~~~~~~~~~~~~~~~

1. 用户、系统用户、管理用户的关系

.. code-block:: vim

    # 用户管理里面的用户列表 是用来登录jumpserver平台的用户, 用户需要先登录jumpserver平台, 才能管理或者连接资产
    # 资产管理里面的管理用户 是jumpserver用来管理资产需要的服务账户, Linux资产需要root或 NOPASSWD: ALL sudo
    权限, JumpServer使用该用户来 '推送系统用户'、'获取资产硬件信息'等。Windows资产随意指定一个, 暂无作用
    # 资产管理里面的系统用户 是jumpserver用户连接资产需要的登录账户, Linux资产可以自动推送该系统用户到资产上,
    Windows需要指定资产上已经创建的系统用户

2. luna 无法访问

.. code-block:: vim

    # 访问 Web终端 提示 Luna是单独部署的一个程序, 请不要通过 8080 端口访问 jumpserver, 通过 nginx 代理端口进行访问
    # 访问 Web终端 提示 403 Forbidden错误, 一般是nginx配置文件的luna路径不正确或者下载了源代码, 请重新下载编译好的代码
    # 访问 Web终端 提示 502 Bad Gateway错误, 一般是selinux和防火墙的问题, 请根据nginx的errorlog来检查

3. 设置浏览器会话过期

.. code-block:: shell

    $ vi /opt/jumpserver/config.yml

    # 找到如下行(可参考 django 设置 session 过期时间), 修改你要的设置即可
    # SESSION_COOKIE_AGE: 86400
    # SESSION_EXPIRE_AT_BROWSER_CLOSE: false

    # 如下, 设置关闭浏览器 cookie 失效, 则修改为
    # SESSION_COOKIE_AGE: 86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE: true

    # 86400 单位是秒(s)

4. 资产授权说明

.. code-block:: vim

    资产授权就是把 系统用户关联到用户 并授权到 对应的资产
    用户只能看到自己被授权的资产

5. Web Terminal 页面经常需要重新刷新页面才能连接资产

.. code-block:: nginx

    # 具体表现为在luna页面一会可以连接资产, 一会就不行, 需要多次刷新页面
    # 如果从开发者工具里面看, 可以看到部分不正常的 502 koko
    # 此问题一般是由最前端一层的nginx反向代理造成的, 需要在每层的代理上添加(注意是每层)
    $ vi /etc/nginx/conf.d/jumpserver.conf
    server {

        listen 80;
        server_name demo.jumpserver.org;

        client_max_body_size 100m;  # 上传录像大小限制

        location / {
                # 这里的 IP 是后端 nginx 的 IP
                proxy_pass http://192.168.244.144;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

6. 重启服务器后无法访问 JumpServer, 页面提示502 或者 403等

.. code-block:: shell

    # 确定 防火墙 和 selinux 已经正确放行或者关闭, 然后检查 jms 是否已经启动成功

7. 传递明文数据到 JumpServer 数据库(数据导入)

.. code-block:: shell

    # 以导入 admin 用户 public_key 为例
    $ source /opt/py3/bin/activate
    $ cd /opt/jumpserver/apps
    $ python manage.py shell
    >>> from users.models import User
    >>> user = User.objects.get(username='admin')
    >>> user.public_key = '明文key'
    >>> user.save()

8. 登录提示登录频繁

.. code-block:: shell

    $ source /opt/py3/bin/activate
    $ cd /opt/jumpserver/utils
    $ sh unblock_all_user.sh

    # 如果不存在 unblock_all_user.sh 文件
    $ source /opt/py3/bin/activate
    $ cd /opt/jumpserver/apps
    $ python manage.py shell
    >>> from django.core.cache import cache
    >>> cache.delete_pattern('_LOGIN_BLOCK_*')
    >>> cache.delete_pattern('_LOGIN_LIMIT_*')
    >>> exit()

9. 清理celery产生的数据(无法正常推送及连接资产, 一直显示........等可以使用, 请确定字符集是zh_CN.UTF-8)

.. code-block:: shell

    $ source /opt/py3/bin/activate
    $ cd /opt/jumpserver/apps
    $ celery -A ops purge -f

    # 如果任然异常, 手动结束所有jumpserver进程, 然后kill掉未能正常结束的jumpserver相关进程, 在重新启动jumpserver即可
