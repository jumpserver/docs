Jms_core 常见问题
-----------------------

- Jms_core 是指 https://github.com/jumpserver/jumpserver 项目
- Jms_core 默认的路径为 /opt/jumpserver

有关安装过程中出现的问题请参考 `安装常见问题文档 <faq_install.html>`_

1. Jms_core 启动异常或者启动失败

.. code-block:: shell

    # 请先检查宿主环境的硬件配置是否达到 JumpServer 的最低硬件要求

    - 提示 ModuleNotFoundError: No module named 'daemon'
    $ source /opt/py3/bin/activate
    $ pip install -r requirements/requirements.txt

    - 提示 redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:6379. Connection refused
    # 检查 redis 是否设置不当或者服务未启动

    - 提示 django.db.utils.OperationalError: (2006, "Can't connect to MySQL server on '127.0.0.1' (115)")
    # 检查 数据库 是否设置不当或者服务未启动

    - 提示 xxxx is running: 0
    $ ./jms stop
    $ rm -rf tmp/*.pid
    $ ps aux | grep python3  # 确定进程都已经退出后, 再继续操作, 否则 kill 掉
    $ ./jms start -d

    - config.yml 设置说明
    # 常见的错误就是字段为空和: 后面少一个空格, 参考下面, 请勿照抄
    # SECRET_KEY: 5RLbBjm8AkMSvnft...  # 不要忽略: 后面的空格, 不支持纯数字
    # BOOTSTRAP_TOKEN: ihR4WG4gRShCnpQL...  # 不要忽略: 后面的空格, 不支持纯数字
    # DB_PASSWORD: '123456'  # 密码纯数字用单引号括起来
    # DB_PASSWORD: cPzxaiUAtA5IkdT2...  # 非纯数字可以不用单引号
    # REDIS_PASSWORD: '888888'  # 密码纯数字用单引号括起来
    # REDIS_PASSWORD: Ma5bzA3gVK5oY17l...  # 非纯数字可以不用单引号

2. Web 登录页面异常

.. code-block:: shell

    # 再解释亿次, 不要通过 8080 端口访问 Web 页面, 请通过 nginx 反向代理的端口, 默认 80 端口访问
    # 不支持 IE 浏览器

    # 如果是其他的错误异常, 请查看 jumpserver/logs/ 下面的 log, 根据相应的错误排查问题

3. Web 登录失败

.. code-block:: shell

    # 默认的管理员账户密码都是 admin
    # 如果输入密码的错误次数超过了安全设置里面的次数, 则登录账号被锁定

    - 如果你是忘了密码, 如果你设置好了 smtp, 那你可以直接点击找回密码重置密码, 你也可以通过控制台重置密码
    $ source /opt/py3/bin/activate
    $ cd /opt/jumpserver/apps
    $ python manage.py changepassword  <user_name>

    - 新建超级用户的命令如下命令
    $ python manage.py createsuperuser --username=user --email=user@domain.com

    - 登陆提示密码过期可以直接点击忘记密码, 通过邮箱重置; 如果未设置邮箱, 通过以下代码重置
    $ source /opt/py3/bin/activate
    $ cd /opt/jumpserver/apps
    $ python manage.py shell
    > from users.models import User
    > u = User.objects.get(username='admin')  # admin 为你要修改的用户
    > u.reset_password('password')  # password 为你要修改的密码
    > u.save()

    - 如果是设置了 LDAP 后无法登录, 请登录数据库禁用 ldap 登录, 然后重新设置 LDAP
    $ mysql -uroot
    $ use jumpserver;
    $ update settings_setting set value='false' where name='AUTH_LDAP';

    - 如果是设置了 OpenID 或者 Radius 导致无法登录, 请在 config.yml 里面禁用后重新调试
    $ vim config.yam

    - 提示登录频繁
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

4. 管理用户 和 系统用户 常见错误

.. code-block:: shell

    - 管理用户 为 jumpserver 使用的服务账户, 因为需要创建用户和修改用户权限, 所以需要管理员权限, linux 需要 NOPASSWD: ALL 的用户, Windows 需要 Administrators 组的用户, telnet 协议和 vnc 协议可以随意设置一个
    # 管理用户为 推送 系统用户 到 相对应的 资产

    - 系统用户是给使用 jumpserver 连接资产的用户分配的资产上面的普通用户, jumpserver 管理员可以根据实际情况给予授权, 资产上面不存在的系统用户, 可以通过自动推送推送到资产上面, 详情请参考快速入门文档
    # 使用 jumpserver 的 用户 登录资产使用的认证凭据就是 系统用户

    - 资产测试可连接性、更新硬件信息、推送提示 ...........
    $ ./jms stop
    $ ps aux | grep python3  # 把未能正常结束的进程 kill 掉

    $ ./jms start -d

    - 资产测试可连接性、更新硬件信息 报 Permission denied 或者 Authentication failure
    # 一般都是管理用户账户密码不正确

    - 资产测试可连接性、更新硬件信息 报 /usr/bin/python: not found
    # 在一般是资产 python 未安装或者 python 异常, 一般出现在 ubuntu 资产上面

    - 系统用户测试资产可连接性错误
    # 确定系统用户是否正确, 如果系统用户使用了自动推送, 确保管理用户正确

    - 连接资产提示 timeout
    .. code-block:: vim

    # 如果在 系统用户 详情里面测试提示 ok, 但是 web 连接资产提示 timeout, 请手动登录该资产修改 /etc/ssh/sshd_config 的 usedns 为 no
    $ vim /etc/ssh/sshd_config

    ...

    # UseDNS no
    UseDNS no

    ...

    # 修改后, 重启 ssh 服务, 再次在 web 上连接资产, 如果任然提示 timeout, 重启 docker
    $ systemctl restart docker
    $ docker restart jms_koko

    # 如果在 系统用户 详情里面测试提示 其他错误, 请检查推送或者系统用户是否设置正确

    # 如果同一个组里面, 出现个别用户无法登录某个资产, 组的其他人可以正常使用的, 请关闭 koko/config.yml 的 连接复用功能
    $ vim koko/config.yml

    ...

    # REUSE_CONNECTION: true
    REUSE_CONNECTION: false

    ...

5. Telnet 使用说明

.. code-block:: shell

    - telnet 连不上
    # 需要在 Web "系统设置"-"终端设置" 添加成功判断代码
    # 是 通过 "tenlet" 命令登录 telnet设备 "成功" 的返回字符串

    - 举例
    $ telnet 172.16.0.1

    Login authentication

    login: admin
    password: *********
    Info: The max number or VTY users is 10, and the number
          of current VTY users on line is 1.
    <RA-L7-RD>

    # 把 <RA-L7-RD> 写入到 Web "系统设置"-"终端设置"-"Telnet 成功正则表达式" 里面, 多个不一样的字符串用 | 隔开, 如 <RA-L7-RD>|<CHXZ-Group-S7503-LB2>|success|成功
    # <RA-L7-RD> 正则可用 <.*> 表示 或者 <RA-.*>

    # RW-F1-1  正则可用 RW-.*

    # 不会写正则直接写设备名就行, 设备1名|设备2名|设备3名|设备4名|success|成功
    # RW-1F-1|RW-2F-1|RW-3F-1|success|成功
    # <RA-L7-RD>|<RA-L6-RD>|<RA-L5-RD>|success|成功
    # <.*>|.*>|success|成功
