# 常见问题

## 查询日志方法

!!! tip "JumpServer 各组件查询日志方法"
    - 默认日志已经挂载到了持久化目录里面，也可以直接到持久化目录里面进行查看
    ```sh
    # 默认持久化目录 /opt/jumpserver
    ls -al /opt/jumpserver/core/logs
    ls -al /opt/jumpserver/koko/data/logs
    ls -al /opt/jumpserver/lion/data/logs
    ls -al /opt/jumpserver/nginx/log
    ```

    === "Core"
        ```sh
        docker exec -it jms_core bash
        cd /opt/jumpserver/logs
        ls -al
        ```
        ```nginx
        total 25160
        drwxr-xr-x 9 root root     4096 8月   7 23:59 .
        drwxr-xr-x 1 root root     4096 7月  21 17:09 ..
        drwxr-xr-x 2 root root     4096 8月   7 23:59 2021-08-07  # 历史日志, 按天切割
        -rw-r--r-- 1 root root    22738 8月   8 12:54 beat.log
        -rw-r--r-- 1 root root        0 8月   7 23:59 celery_ansible.log
        -rw-r--r-- 1 root root        0 3月  18 23:59 celery_check_asset_perm_expired.log
        -rw-r--r-- 1 root root    50921 8月   8 12:53 celery_default.log
        -rw-r--r-- 1 root root        0 3月  18 23:59 celery_heavy_tasks.log
        -rw-r--r-- 1 root root        1 8月   7 19:51 celery.log
        -rw-r--r-- 1 root root        0 3月  18 23:59 celery_node_tree.log
        -rw-r--r-- 1 root root        0 8月   7 23:59 daphne.log
        -rw-r--r-- 1 root root 16679320 8月   8 09:34 drf_exception.log
        -rw-r--r-- 1 root root        0 8月   7 23:59 flower.log
        -rw-r--r-- 1 root root   834058 8月   8 12:57 gunicorn.log
        -rw-r--r-- 1 root root        0 8月   7 23:59 jms.log
        -rw-r--r-- 1 root root  4964863 8月   6 22:56 jumpserver.log  # core 日志主要看这个
        -rw-r--r-- 1 root root  3129115 8月   6 22:50 unexpected_exception.log
        ```
        ```bash
        tail -f jumpserver.log -n 200
        # 如果无异常也可以查看其他的 log 是否有异常, 注意 log 的时间
        ```
        ```nginx hl_lines="2-14"
        # 在发日志给其他人员协助排错时，注意需要完整的日志，参考此处：
        2021-08-07 22:55:20 [ERROR]              <---- 注意开始时间一定要有
        Traceback (most recent call last):
          File "/usr/local/lib/python3.8/site-packages/rest_framework/views.py", line 497, in dispatch
            self.initial(request, *args, **kwargs)
          File "/opt/jumpserver/apps/assets/api/node.py", line 115, in initial
            return super().initial(request, *args, **kwargs)
          File "/usr/local/lib/python3.8/site-packages/rest_framework/views.py", line 415, in initial
            self.check_permissions(request)
          File "/usr/local/lib/python3.8/site-packages/rest_framework/views.py", line 333, in check_permissions
            self.permission_denied(
          File "/usr/local/lib/python3.8/site-packages/rest_framework/views.py", line 175, in permission_denied
            raise exceptions.PermissionDenied(detail=message, code=code)
        rest_framework.exceptions.PermissionDenied: 您没有执行该操作的权限。     <---- 有些用户会只发这一条，这是错误的
        2021-08-08 09:34:30 [ERROR]              <---- 到下一个时间这中间的所有报错都要完整的发送
        # 给其他人发送诊断日志时，请遵循此规则，如果是同一时间段内出现的多个报错，请根据时间点完整发送。
        # 如果是重复的日志，请先自行去重。
        ```

    === "Celery"
        ```sh
        docker exec -it jms_celery bash
        cd /opt/jumpserver/logs
        ls -al
        ```
        ```nginx
        total 25160
        drwxr-xr-x 9 root root     4096 8月   7 23:59 .
        drwxr-xr-x 1 root root     4096 7月  21 17:09 ..
        drwxr-xr-x 2 root root     4096 8月   7 23:59 2021-08-07
        -rw-r--r-- 1 root root    22738 8月   8 12:54 beat.log                                # 这个也是
        -rw-r--r-- 1 root root        0 8月   7 23:59 celery_ansible.log                      # celery 日志看 celery_ 开头的
        -rw-r--r-- 1 root root        0 3月  18 23:59 celery_check_asset_perm_expired.log
        -rw-r--r-- 1 root root    50921 8月   8 12:53 celery_default.log
        -rw-r--r-- 1 root root        0 3月  18 23:59 celery_heavy_tasks.log
        -rw-r--r-- 1 root root        1 8月   7 19:51 celery.log
        -rw-r--r-- 1 root root        0 3月  18 23:59 celery_node_tree.log                    # 到此结束, core 和 celery 日志目录是共用的
        -rw-r--r-- 1 root root        0 8月   7 23:59 daphne.log
        -rw-r--r-- 1 root root 16679320 8月   8 09:34 drf_exception.log
        -rw-r--r-- 1 root root        0 8月   7 23:59 flower.log
        -rw-r--r-- 1 root root   834058 8月   8 12:57 gunicorn.log
        -rw-r--r-- 1 root root        0 8月   7 23:59 jms.log
        -rw-r--r-- 1 root root  4964863 8月   6 22:56 jumpserver.log
        -rw-r--r-- 1 root root  3129115 8月   6 22:50 unexpected_exception.log
        ```
        ```sh
        tail -f celery_default.log -n 200
        ```
        ```nginx
        # celery 日志
        KeyError: 'assets.tasks.admin_user_connectivity.test_admin_user_connectivity_period'
        Received unregistered task of type 'assets.tasks.test_admin_user_connectivity_period'.
        The message has been ignored and discarded.

        Did you remember to import the module containing this task?
        Or maybe you're using relative imports?

        Please see
        http://docs.celeryq.org/en/latest/internals/protocol.html
        for more information.

        The full contents of the message body was:
        b'\x80\x02)}q\x00}q\x01(X\t\x00\x00\x00callbacksq\x02NX\x08\x00\x00\x00errbacksq\x03NX\x05\x00\x00\x00chainq\x04NX\x05\x00\x00\x00chordq\x05Nu\x87q\x06.' (74b)
        Traceback (most recent call last):
          File "/usr/local/lib/python3.8/site-packages/celery/worker/consumer/consumer.py", line 562, in on_task_received
            strategy = strategies[type_]
        ```

    === "KoKo"
        ```sh
        docker logs -f jms_koko --tail 200
        ```
        ```sh
        # 如果需要进入容器操作
        docker exec -it jms_koko bash
        cd /opt/koko/data/logs
        ls -al
        ```
        ```nginx
        total 69040
        drwxr--r-- 2 root root     4096 7月  19 22:09 .
        drwxr-xr-x 5 root root     4096 12月 18 2020 ..
        -rw-r--r-- 1 root root 52428600 7月  19 22:09 koko-2021-07-19T22-09-53.213.log
        -rw-r--r-- 1 root root 18248268 8月   8 12:46 koko.log      # koko 日志
        ```
        ```sh
        tail -f koko.log -n 200
        ```
        ```nginx
        # koko 日志
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        2021-07-19 22:09:51 [ERRO] User root Authenticate err: POST http://core:8080/api/v1/authentication/tokens/ failed, get code: 400, {"error":"block_login","msg":"账号已被锁定（请联系管理员解锁 或 30分钟后重试）"}
        ```

    === "Lion"
        ```sh
        docker logs -f jms_lion --tail 200
        ```
        ```sh
        # 如果需要进入容器操作
        docker exec -it jms_lion bash
        cd /opt/lion/data/logs
        ls -al
        ```
        ```nginx
        total 116
        drwxr-xr-x 2 root root   4096 7月  15 22:37 .
        drwxr-xr-x 9 root root   4096 7月  15 21:32 ..
        -rw-r--r-- 1 root root 103103 8月   7 19:38 lion.log
        ```
        ```sh
        tail -f lion.log -n 200
        ```
        ```nginx
        # lion 日志
        2021-07-15 10:06:31 tunnel conn.go [ERROR] Session[e8b56e52-d7a4-47e1-b5a1-5f6ec59e2a83] receive web client disconnect opcode
        2021-07-15 10:06:31 tunnel conn.go [ERROR] Session[e8b56e52-d7a4-47e1-b5a1-5f6ec59e2a83] web client read err: websocket: close 1005 (no status)
        2021-07-15 10:06:31 tunnel conn.go [ERROR] Session[e8b56e52-d7a4-47e1-b5a1-5f6ec59e2a83] send web client err: websocket: close sent
        2021-07-15 10:06:32 session server.go [ERROR] 录像文件小于1024字节，可判断连接失败，未能产生有效的录像文件
        ```

    === "Nginx"
        ```sh
        docker logs -f jms_nginx --tail 200
        ```
        ```sh
        # 如果需要进入容器操作
        docker exec -it jms_lion sh
        cd /var/log/nginx
        ls -al
        ```
        ```nginx
        total 84652
        -rw-r--r-- 1 root root 53237275 8月   8 13:46 access.log
        -rw-r--r-- 1 root root    83858 8月   8 12:03 error.log
        -rw-r--r-- 1 root root 12870135 8月   8 12:46 tcp-access.log
        ```
        ```sh
        tail -f error.log -n 200
        ```
        ```nginx
        # nginx 日志
        2021/08/07 16:01:19 [error] 1113#1113: *395030 recv() failed (104: Connection reset by peer) while proxying upgraded connection, client: 192.168.250.1, server: , request: "GET /ws/notifications/site-msg/ HTTP/1.1", upstream: "http://192.168.250.2:8070/ws/notifications/site-msg/", host: "192.168.100.100"
        2021/08/07 17:51:55 [error] 1113#1113: *397564 recv() failed (104: Connection reset by peer) while proxying upgraded connection, client: 192.168.250.1, server: , request: "GET /ws/notifications/site-msg/ HTTP/1.1", upstream: "http://192.168.250.2:8070/ws/notifications/site-msg/", host: "192.168.100.100"
        2021/08/07 17:52:19 [error] 1113#1113: *413161 recv() failed (104: Connection reset by peer) while proxying upgraded connection, client: 192.168.250.1, server: , request: "GET /ws/notifications/site-msg/ HTTP/1.1", upstream: "http://192.168.250.2:8070/ws/notifications/site-msg/", host: "192.168.100.100"
        2021/08/07 22:31:31 [warn] 1113#1113: *416920 an upstream response is buffered to a temporary file /var/cache/nginx/proxy_temp/6/01/0000000016 while reading upstream, client: 192.168.250.1, server: , request: "GET /api/docs/?format=openapi HTTP/1.1", upstream: "http://192.168.250.2:8080/api/docs/?format=openapi", host: "192.168.100.100", referrer: "https://192.168.100.100/api/docs/"
        2021/08/08 12:03:28 [error] 1113#1113: *410227 recv() failed (104: Connection reset by peer) while proxying upgraded connection, client: 192.168.250.1, server: , request: "GET /ws/notifications/site-msg/ HTTP/1.1", upstream: "http://192.168.250.2:8070/ws/notifications/site-msg/", host: "192.168.100.100"
        ```


### 1. Core 启动异常

```sh
./jmsctl.sh start
```
```vim hl_lines="5-9"
Creating network "jms_net" with driver "bridge"
Creating jms_mysql ... done
Creating jms_redis ... done
Creating jms_core  ... done
ERROR: for celery  Container "76b2e315f69d" is unhealthy.
ERROR: for lina  Container "76b2e315f69d" is unhealthy.
ERROR: for luna  Container "76b2e315f69d" is unhealthy.
ERROR: for lion  Container "76b2e315f69d" is unhealthy.
ERROR: for koko  Container "76b2e315f69d" is unhealthy.
ERROR: Encountered errors while bringing up the project.
```
```sh
# 如果出现上面的错误, 执行下面的命令, 直到出现 Check service status 为止
docker logs -f jms_core --tail 200  # 如果没有报错就等表结构合并完毕后然后重新 start 即可
```
```yaml
2021-02-08 14:58:53 Mon Feb  8 14:58:53 2021
2021-02-08 14:58:53 JumpServer version {{ jumpserver.version }}, more see https://www.jumpserver.org

- Start Gunicorn WSGI HTTP Server
2021-02-08 14:58:53 Check database connection ...
users
  [ ] 0001_initial
  [ ] 0002_auto_20171225_1157_squashed_0019_auto_20190304_1459 (18 squashed migrations)
  [ ] 0020_auto_20190612_1825
  [ ] 0021_auto_20190625_1104
  [ ] 0022_auto_20190625_1105
  [ ] 0023_auto_20190724_1525
  [ ] 0024_auto_20191118_1612
  [ ] 0025_auto_20200206_1216
  [ ] 0026_auto_20200508_2105
  [ ] 0027_auto_20200616_1503
  [ ] 0028_auto_20200728_1805
  [ ] 0029_auto_20200814_1650
  [ ] 0030_auto_20200819_2041
  [ ] 0031_auto_20201118_1801
  2021-02-08 14:58:58 Database connect success
  Operations to perform:
    Apply all migrations: admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, ops, orgs, perms, sessions, settings, terminal, tickets, users
  Running migrations:
    Applying contenttypes.0001_initial... OK
    Applying contenttypes.0002_remove_content_type_name... OK
    Applying auth.0001_initial... OK
    Applying auth.0002_alter_permission_name_max_length... OK
    Applying auth.0003_alter_user_email_max_length... OK
    Applying auth.0004_alter_user_username_opts... OK
    Applying auth.0005_alter_user_last_login_null... OK
    Applying auth.0006_require_contenttypes_0002... OK
    Applying auth.0007_alter_validators_add_error_messages... OK
    Applying auth.0008_alter_user_username_max_length... OK
    ... 省略
    Applying tickets.0001_initial... OK
    Applying tickets.0002_auto_20200728_1146... OK
    Applying tickets.0003_auto_20200804_1551... OK
    Applying tickets.0004_ticket_comment... OK
    Applying tickets.0005_ticket_meta_confirmed_system_users... OK
    Applying tickets.0006_auto_20201023_1628... OK
    Applying tickets.0007_auto_20201224_1821... OK
    Applying users.0031_auto_20201118_1801... OK
    # 确定这上面都是显示 ok，不能有 error
  2021-02-08 14:59:31 [cache INFO] CACHE: Send refresh task <orgs.caches.OrgResourceStatisticsCache object at 0x7fb9122ce0d0>.('nodes_amount',)
  Operations to perform:
    Apply all migrations: admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, ops, orgs, perms, sessions, settings, terminal, tickets, users
  Running migrations:
    No migrations to apply.

  - Start Flower as Task Monitor

  - Start Daphne ASGI WS Server
  2021-02-08 15:01:02 Check service status: gunicorn -> running at 38
  2021-02-08 15:01:02 Check service status: flower -> running at 44
  2021-02-08 15:01:02 Check service status: daphne -> running at 54
```
```sh
# 确定上面都是 ok 的没有报错, 提示 Check service status 后就可以重新启动其他组件
./jmsctl.sh start
```

### 2. Web 页面异常

!!! question "Server error occur, contact administrator"

```sh
docker logs -f jms_core --tail 200
# 查看是否有报错，如果没有或者不完整请进入容器查看日志
```
```sh
docker exec -it jms_core /bin/bash
cat logs/jumpserver.log
# 根据报错处理
```

### 3. Web 登录失败

!!! question "忘记密码，密码过期"
    如果忘了密码或者密码过期，可以点击找回密码通过邮件找回  
    如果无法通过邮件找回，可以通过控制台重置

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

!!! tip "admin 为你要修改的账户名称，password 为你要修改的密码"

!!! question "登录频繁账号被锁定"
    找管理员重置，管理员可以在对应用户的个人页面重置  
    或者通过下面的 shell 解决

```bash
docker exec -it jms_core /bin/bash
cd /opt/jumpserver/apps
python manage.py shell
```
```python
from django.core.cache import cache
cache.delete_pattern('_LOGIN_BLOCK_*')
cache.delete_pattern('_LOGIN_LIMIT_*')
```

!!! tip "或者你也可以新建一个超级管理员来对其他用户进行设置"

```sh
docker exec -it jms_core /bin/bash
cd /opt/jumpserver/apps
python manage.py createsuperuser --username=user --email=user@domain.com
```

!!! question "如果是设置了 LDAP 后无法登录，请登录数据库禁用 ldap 登录，然后重新设置 LDAP"

```sh
mysql -uroot -p
```
```mysql
use jumpserver;
update settings_setting set value='false' where name='AUTH_LDAP';
```
```sh
redis-cli -a $REDIS_PASSWORD
```
```redis
select 4
keys *LDAP*
del :1:_SETTING_AUTH_LDAP
```

!!! question "如果是设置 其他身份认证 后无法登录，注释掉 jumpserver/config/config.txt 里面的身份认证设置重启即可"

### 4. 管理用户 和 系统用户

!!! question "资产测试可连接性、更新硬件信息 报 Permission denied 或者 Authentication failure"
    一般都是管理用户账户密码不正确

!!! question "资产测试可连接性、更新硬件信息 报 /usr/bin/python: not found"
    在一般是资产 python 未安装或者 python 异常，一般出现在 ubuntu 资产上

!!! question "系统用户测试资产可连接性错误"
    确定系统用户是否正确，如果系统用户使用了自动推送，确保管理用户正确  
    系统用户设置为 root 的情况下，请关闭自动推送，并输入正确的 root 密码

!!! question "提示 timeout"

```sh
# 手动 ssh 登录提示 timeout 的那台服务器
vi /etc/ssh/sshd_config
```
```vim
UseDNS no
```
```sh
# 重启 JumpServer 服务器的 docker
systemctl restart docker
docker restart jms_koko
```

!!! question "Connect websocket server error"
    一般情况下 nginx 未配置 websocket 导致，根据反向代理文档进行修改后重启 nginx 即可
