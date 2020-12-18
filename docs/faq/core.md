# Core 常见问题

!!! info "常见问题记录"

### 1. core 启动异常

!!! question "查看日志"
    ```sh
    docker logs -f jms_core --tail 100
    ```

### 2. Web 登录失败

!!! question "忘记密码, 密码过期"
    如果忘了密码或者密码过期, 可以点击找回密码通过邮件找回  
    如果无法通过邮件找回, 可以通过控制台重置
    ```sh
    docker exec -it jms_core /bin/bash
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
    docker exec -it jms_core /bin/bash
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

!!! question "如果是设置 其他身份认证 后无法登录, 注释掉 jumpserver/config/config.txt 里面的身份认证设置重启即可"

### 4. 管理用户 和 系统用户

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
    如果仍然一样, 表示 nginx 也有错误, 根据安装文档进行修改后重启 nginx 即可

### 5. 更新 Core 报错

!!! question "启动报错 Cannot add foreign key constraint"
    这是因为旧版本的数据库字符集和新版本数据库字符集不一样导致，备份好数据库，然后进行如下操作
    ```mysql
    alter database jumpserver character set utf8 collate utf8_bin;
    use jumpserver;
    SET FOREIGN_KEY_CHECKS = 0;
    alter table applications_remoteapp convert to character set utf8 collate utf8_bin;
    SET FOREIGN_KEY_CHECKS = 1;
    ```
    把所有表都修改一下，重启 core 即可(applications_remoteapp 就是表名，把 jumpserver 数据库的所有表都改一下，注意备份)
    ```sh
    # 表很多，可以用 shell 快速生成 sql 语句
    sql=`mysql -uroot -e "use jumpserver; show tables;" | grep -v "Tables_in" | awk '{print $1}'`
    for i in $sql; do echo "alter table $i convert to character set utf8 collate utf8_bin;"; done
    # 然后登陆 mysql 服务参考上面的教程处理即可
    mysql -uroot
    ```
    ```mysql
    alter database jumpserver character set utf8 collate utf8_bin;
    use jumpserver;
    SET FOREIGN_KEY_CHECKS = 0;
    alter table applications_databaseapp convert to character set utf8 collate utf8_bin;
    alter table applications_remoteapp convert to character set utf8 collate utf8_bin;
    alter table assets_adminuser convert to character set utf8 collate utf8_bin;
    alter table assets_asset convert to character set utf8 collate utf8_bin;
    ... 把刚才查询到 sql 语句执行完
    SET FOREIGN_KEY_CHECKS = 1;
    ```
