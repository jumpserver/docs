# 常见问题

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

!!! question "如果是设置了 LDAP 后无法登录, 请登录数据库禁用 ldap 登录, 然后重新设置 LDAP"

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
    一般情况下 nginx 未配置 websocket 导致, 根据反向代理文档进行修改后重启 nginx 即可
