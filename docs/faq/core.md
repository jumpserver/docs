# Core 常见问题

!!! info "常见问题记录"

### 1. core 启动异常

!!! question "ModuleNotFoundError: No module named 'daemon'"
    ```sh
    source /opt/py3/bin/activate
    pip install -r requirements/requirements.txt
    ```

!!! question "redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:6379. Connection refused"
    检查 config.yml 的 redis 设置

!!! question "django.db.utils.OperationalError: (2006, "Can't connect to MySQL server on '127.0.0.1' (115)")"
    检查 config.yml 的 mysql 设置

!!! info "config.yml 格式说明"
    ```yaml
    常见的错误就是字段为空和: 后面少一个空格, 参考下面, 请勿照抄  
    SECRET_KEY: 5RLbBjm8AkMSvnft...  # 不要忽略: 后面的空格, 不支持纯数字  
    BOOTSTRAP_TOKEN: ihR4WG4gRShCnpQL...  # 不要忽略: 后面的空格, 不支持纯数字  
    DB_PASSWORD: '123456'  # 密码纯数字用单引号括起来  
    DB_PASSWORD: cPzxaiUAtA5IkdT2...  # 非纯数字可以不用单引号  
    REDIS_PASSWORD: '888888'  # 密码纯数字用单引号括起来  
    REDIS_PASSWORD: Ma5bzA3gVK5oY17l...  # 非纯数字可以不用单引号  
    ```

### 2. Web 登录页面异常

!!! question "页面显示不正常"
    不要通过 8080 端口访问 Web 页面  
    不支持 IE 浏览器  
    其他异常, 请查看 jumpserver/logs/ 和 /var/log/nginx 下面的 log, 根据相应的错误排查问题

### 3. Web 登录失败

!!! question "忘记密码"
    如果忘了密码, 可以点击找回密码通过邮件找回  
    如果无法通过邮件找回, 可以通过控制台重置
    ```sh
    source /opt/py3/bin/activate
    cd /opt/jumpserver/apps
    python manage.py shell
    ```
    ```python
    from users.models import User
    u = User.objects.get(username='admin')
    u.reset_password('password')
    u.save()
    ```

    !!! tip "admin 为你要修改的账户名称, password 为你要修改的密码"

!!! question "登录频繁账号被锁定"
    找管理员重置, 管理员可以在对应用户的个人页面重置  
    或者通过下面的 shell 解决
    ```
    source /opt/py3/bin/activate
    cd /opt/jumpserver/apps
    python manage.py shell
    ```
    ```python
    from django.core.cache import cache
    cache.delete_pattern('_LOGIN_BLOCK_*')
    cache.delete_pattern('_LOGIN_LIMIT_*')
    ```

!!! question "如果是设置了 LDAP 后无法登录, 请登录数据库禁用 ldap 登录, 然后重新设置 LDAP"
    ```sh
    mysql -uroot -p
    ```
    ```mysql
    use jumpserver;
    update settings_setting set value='false' where name='AUTH_LDAP';
    ```

!!! question "如果是设置 其他身份认证 后无法登录, 注释掉 jumpserver/config.yml 里面的身份认证设置重启即可"

### 4. 管理用户 和 系统用户

!!! question "资产测试可连接性、更新硬件信息、推送提示 ..........."
    ```
    source /opt/py3/bin/activate
    ./jms stop
    ps aux | grep py3 | awk '{print $2}' | xargs kill -9
    rm -rf tmp/*.pid
    ./jms start -d
    ```

!!! question "资产测试可连接性、更新硬件信息 报 Permission denied 或者 Authentication failure"
    一般都是管理用户账户密码不正确

!!! question "资产测试可连接性、更新硬件信息 报 /usr/bin/python: not found"
    在一般是资产 python 未安装或者 python 异常, 一般出现在 ubuntu 资产上

!!! question "系统用户测试资产可连接性错误"
    确定系统用户是否正确, 如果系统用户使用了自动推送, 确保管理用户正确  
    系统用户设置为 root 的情况下, 请关闭自动推送, 并输入正确的 root 密码

!!! question "提示 timeout"
    ```sh
    vi /etc/ssh/sshd_config
    ```
    ```vim
    UseDNS no
    ```
    ```sh
    systemctl restart docker
    docker restart jms_koko
    ```

!!! question "Connect websocket server error"
    kill 掉进程再重启 core  
    如果任然一样, 表示 nginx 也有错误, 根据安装文档进行修改后重启 nginx 即可
