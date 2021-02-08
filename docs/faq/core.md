# Core 常见问题

!!! info "常见问题记录"

### 1. core 启动异常

!!! question "启动 jms_core 报错"
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
    ERROR: for guacamole  Container "76b2e315f69d" is unhealthy.
    ERROR: for koko  Container "76b2e315f69d" is unhealthy.
    ERROR: Encountered errors while bringing up the project.
    ```
    ```sh
    docker logs -f jms_core --tail 200  # 如果没有报错就等表结构合并完毕后然后重新 start 即可
    ```
    ```vim
    2021-02-08 14:58:53 Mon Feb  8 14:58:53 2021
    2021-02-08 14:58:53 JumpServer version v2.7.1, more see https://www.jumpserver.org

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
      Applying users.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying admin.0003_logentry_add_action_flag_choices... OK
      Applying users.0002_auto_20171225_1157_squashed_0019_auto_20190304_1459... OK
      Applying users.0020_auto_20190612_1825... OK
      Applying users.0021_auto_20190625_1104... OK
      Applying users.0022_auto_20190625_1105... OK
      Applying users.0023_auto_20190724_1525... OK
      Applying users.0024_auto_20191118_1612... OK
      Applying users.0025_auto_20200206_1216... OK
      Applying users.0026_auto_20200508_2105... OK
      Applying users.0027_auto_20200616_1503... OK
      Applying users.0028_auto_20200728_1805... OK
      Applying users.0029_auto_20200814_1650... OK
      Applying users.0030_auto_20200819_2041... OK
      Applying assets.0001_initial... OK
      Applying perms.0001_initial... OK
      Applying assets.0002_auto_20180105_1807_squashed_0009_auto_20180307_1212... OK
      Applying assets.0010_auto_20180307_1749_squashed_0019_auto_20180816_1320... OK
      Applying perms.0002_auto_20171228_0025_squashed_0009_auto_20180903_1132... OK
      Applying perms.0003_action... OK
      Applying perms.0004_assetpermission_actions... OK
      Applying assets.0020_auto_20180816_1652... OK
      Applying assets.0021_auto_20180903_1132... OK
      Applying assets.0022_auto_20181012_1717... OK
      Applying assets.0023_auto_20181016_1650... OK
      Applying assets.0024_auto_20181219_1614... OK
      Applying assets.0025_auto_20190221_1902... OK
      Applying assets.0026_auto_20190325_2035... OK
      Applying applications.0001_initial... OK
      Applying perms.0005_auto_20190521_1619... OK
      Applying perms.0006_auto_20190628_1921... OK
      Applying perms.0007_remove_assetpermission_actions... OK
      Applying perms.0008_auto_20190911_1907... OK
      Applying assets.0027_auto_20190521_1703... OK
      Applying assets.0028_protocol... OK
      Applying assets.0029_auto_20190522_1114... OK
      Applying assets.0030_auto_20190619_1135... OK
      Applying assets.0031_auto_20190621_1332... OK
      Applying assets.0032_auto_20190624_2108... OK
      Applying assets.0033_auto_20190624_2108... OK
      Applying assets.0034_auto_20190705_1348... OK
      Applying assets.0035_auto_20190711_2018... OK
      Applying assets.0036_auto_20190716_1535... OK
      Applying assets.0037_auto_20190724_2002... OK
      Applying assets.0038_auto_20190911_1634... OK
      Applying perms.0009_remoteapppermission_system_users... OK
      Applying assets.0039_authbook_is_active... OK
      Applying assets.0040_auto_20190917_2056... OK
      Applying assets.0041_gathereduser... OK
      Applying assets.0042_favoriteasset... OK
      Applying assets.0043_auto_20191114_1111... OK
      Applying assets.0044_platform... OK
      Applying assets.0045_auto_20191206_1607... OK
      Applying assets.0046_auto_20191218_1705... OK
      Applying applications.0002_remove_remoteapp_system_user... OK
      Applying applications.0003_auto_20191210_1659... OK
      Applying applications.0004_auto_20191218_1705... OK
      Applying perms.0010_auto_20191218_1705... OK
      Applying perms.0011_auto_20200721_1739... OK
      Applying assets.0047_assetuser... OK
      Applying assets.0048_auto_20191230_1512... OK
      Applying assets.0049_systemuser_sftp_root... OK
      Applying assets.0050_auto_20200711_1740... OK
      Applying assets.0051_auto_20200713_1143... OK
      Applying assets.0052_auto_20200715_1535... OK
      Applying assets.0053_auto_20200723_1232... OK
      Applying assets.0054_auto_20200807_1032... OK
      Applying applications.0005_k8sapp... OK
      Applying perms.0012_k8sapppermission... OK
      Applying assets.0055_auto_20200811_1845... OK
      Applying assets.0056_auto_20200904_1751... OK
      Applying assets.0057_fill_node_value_assets_amount_and_parent_key...

      ................................................................. OK
      Applying perms.0013_rebuildusertreetask_usergrantedmappingnode... OK
      Applying perms.0014_build_users_perm_tree... OK
      Applying perms.0015_auto_20200929_1728... OK
      Applying assets.0058_auto_20201023_1115... OK
      Applying assets.0059_auto_20201027_1905... OK
      Applying applications.0006_application... OK
      Applying perms.0016_applicationpermission... OK
      Applying perms.0017_auto_20210104_0435... OK
      Applying applications.0007_auto_20201119_1110... OK
      Applying applications.0008_auto_20210104_0435... OK
      Applying assets.0060_node_full_value...
    - Start migrate node value if has /
    - Start migrate node full value
     OK
      Applying assets.0061_auto_20201116_1757... OK
      Applying assets.0062_auto_20201117_1938... OK
      Applying assets.0063_migrate_default_node_key...
    Check old default node `key=0 value=Default` not exists
     OK
      Applying assets.0064_auto_20201203_1100... OK
      Applying assets.0065_auto_20210121_1549... OK
      Applying audits.0001_initial... OK
      Applying audits.0002_ftplog_org_id... OK
      Applying audits.0003_auto_20180816_1652... OK
      Applying audits.0004_operatelog_passwordchangelog_userloginlog... OK
      Applying audits.0005_auto_20190228_1715... OK
      Applying audits.0006_auto_20190726_1753... OK
      Applying audits.0007_auto_20191202_1010... OK
      Applying audits.0008_auto_20200508_2105... OK
      Applying audits.0009_auto_20200624_1654... OK
      Applying audits.0010_auto_20200811_1122... OK
      Applying audits.0011_userloginlog_backend... OK
      Applying auth.0009_alter_user_last_name_max_length... OK
      Applying auth.0010_alter_group_name_max_length... OK
      Applying auth.0011_update_proxy_permissions... OK
      Applying auth.0012_alter_user_first_name_max_length... OK
      Applying authentication.0001_initial... OK
      Applying authentication.0002_auto_20190729_1423... OK
      Applying authentication.0003_loginconfirmsetting... OK
      Applying authentication.0004_ssotoken... OK
      Applying captcha.0001_initial... OK
      Applying common.0001_initial... OK
      Applying common.0002_auto_20180111_1407... OK
      Applying common.0003_setting_category... OK
      Applying common.0004_setting_encrypted... OK
      Applying common.0005_auto_20190221_1902... OK
      Applying common.0006_auto_20190304_1515... OK
      Applying django_cas_ng.0001_initial... OK
      Applying django_celery_beat.0001_initial... OK
      Applying django_celery_beat.0002_auto_20161118_0346... OK
      Applying django_celery_beat.0003_auto_20161209_0049... OK
      Applying django_celery_beat.0004_auto_20170221_0000... OK
      Applying django_celery_beat.0005_add_solarschedule_events_choices... OK
      Applying django_celery_beat.0006_auto_20180322_0932... OK
      Applying django_celery_beat.0007_auto_20180521_0826... OK
      Applying django_celery_beat.0008_auto_20180914_1922... OK
      Applying django_celery_beat.0006_auto_20180210_1226... OK
      Applying django_celery_beat.0006_periodictask_priority... OK
      Applying django_celery_beat.0009_periodictask_headers... OK
      Applying django_celery_beat.0010_auto_20190429_0326... OK
      Applying django_celery_beat.0011_auto_20190508_0153... OK
      Applying django_celery_beat.0012_periodictask_expire_seconds... OK
      Applying jms_oidc_rp.0001_initial... OK
      Applying ops.0001_initial... OK
      Applying ops.0002_celerytask... OK
      Applying ops.0003_auto_20181207_1744... OK
      Applying ops.0004_adhoc_run_as... OK
      Applying ops.0005_auto_20181219_1807... OK
      Applying ops.0006_auto_20190318_1023... OK
      Applying ops.0007_auto_20190724_2002... OK
      Applying ops.0008_auto_20190919_2100... OK
      Applying ops.0009_auto_20191217_1713... OK
      Applying ops.0010_auto_20191217_1758... OK
      Applying ops.0011_auto_20200106_1534... OK
      Applying ops.0012_auto_20200108_1659... OK
      Applying ops.0013_auto_20200108_1706... OK
      Applying ops.0014_auto_20200108_1749... OK
      Applying ops.0015_auto_20200108_1809... OK
      Applying ops.0016_commandexecution_org_id... OK
      Applying ops.0017_auto_20200306_1747... OK
      Applying ops.0018_auto_20200509_1434... OK
      Applying ops.0019_adhocexecution_celery_task_id... OK
      Applying orgs.0001_initial... OK
      Applying orgs.0002_auto_20180903_1132... OK
      Applying orgs.0003_auto_20190916_1057... OK
      Applying orgs.0004_organizationmember... OK
      Applying orgs.0005_auto_20200721_1937... OK
      Applying orgs.0006_auto_20200721_1937... OK
      Applying orgs.0007_auto_20200728_1805... OK
      Applying orgs.0008_auto_20200819_2041... OK
      Applying orgs.0009_auto_20201023_1628... OK
      Applying sessions.0001_initial... OK
      Applying settings.0001_initial... OK
      Applying terminal.0001_initial... OK
      Applying terminal.0002_auto_20171228_0025_squashed_0009_auto_20180326_0957... OK
      Applying terminal.0010_auto_20180423_1140... OK
      Applying terminal.0011_auto_20180807_1116... OK
      Applying terminal.0012_auto_20180816_1652... OK
      Applying terminal.0013_auto_20181123_1113... OK
      Applying terminal.0014_auto_20181226_1441... OK
      Applying terminal.0015_auto_20190923_1529... OK
      Applying terminal.0016_commandstorage_replaystorage... OK
      Applying terminal.0017_auto_20191125_0931... OK
      Applying terminal.0018_auto_20191202_1010... OK
      Applying terminal.0019_auto_20191206_1000... OK
      Applying terminal.0020_auto_20191218_1721... OK
      Applying terminal.0021_auto_20200213_1316... OK
      Applying terminal.0022_session_is_success... OK
      Applying terminal.0023_command_risk_level... OK
      Applying terminal.0024_auto_20200715_1713... OK
      Applying terminal.0025_auto_20200810_1735... OK
      Applying terminal.0026_auto_20201027_1905... OK
      Applying terminal.0027_auto_20201102_1651... OK
      Applying terminal.0028_auto_20201110_1918... OK
      Applying terminal.0029_auto_20201116_1757... OK
      Applying terminal.0030_terminal_type... OK
      Applying terminal.0031_auto_20210113_1356... OK
      Applying tickets.0001_initial... OK
      Applying tickets.0002_auto_20200728_1146... OK
      Applying tickets.0003_auto_20200804_1551... OK
      Applying tickets.0004_ticket_comment... OK
      Applying tickets.0005_ticket_meta_confirmed_system_users... OK
      Applying tickets.0006_auto_20201023_1628... OK
      Applying tickets.0007_auto_20201224_1821... OK
      Applying users.0031_auto_20201118_1801... OK
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
    ./jmsctl.sh start
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
