# 升级 常见问题

!!! question "下载 Docker 镜像很慢"
    ```sh
    cat /etc/docker/daemon.json
    ```
    ```yaml
    {
      "registry-mirrors": [
        "https://hub-mirror.c.163.com",
        "https://bmtrgdvx.mirror.aliyuncs.com",
        "http://f1361db2.m.daocloud.io"
      ],
      "log-driver": "json-file",
      "log-opts": {
        "max-file": "3",
        "max-size": "10m"
      }
    }
    ```
    可以使用其他的镜像源, 推荐使用阿里云的镜像源  _[申请地址](https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors)_

!!! question "导入数据库报错"
    ```sh
    ./jmsctl.sh restore_db /opt/jumpserver.sql
    ```
    ```vim hl_lines="3"
    开始还原数据库: /opt/jumpserver.sql
    mysql: [Warning] Using a password on the command line interface can be insecure.
    ERROR 1022 (23000) at line 1237: Can't write; duplicate key in table 'xxxxxx'
    ERRO[0008] error waiting for container: context canceled
    read unix @->ar/run/docker.sock: read: connection reset by peer
    数据库恢复失败,请检查数据库文件是否完整，或尝试手动恢复！
    ```
    ```sh
    ./jmsctl.sh stop
    ```
    ```sh
    docker exec -it jms_mysql /bin/bash
    ```
    ```sh
    mysql -uroot -p$MYSQL_ROOT_PASSWORD
    ```
    ```mysql
    drop database jumpserver;
    create database jumpserver default charset 'utf8' collate 'utf8_bin';
    exit;
    exit
    ```
    ```sh
    ./jmsctl.sh restore_db /opt/jumpserver.sql
    # 注意: 确定在导入数据库的过程中没有错误
    ```
    ```sh
    ./jmsctl.sh start
    ```

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

!!! question "Table 'xxxxxx' already exists"
    ```sh
    ./jmsctl.sh stop
    ```
    ```sh
    if grep -q 'CHARSET=utf8;' /opt/jumpserver.sql; then
        cp /opt/jumpserver.sql /opt/jumpserver_bak.sql
        sed -i 's@CHARSET=utf8;@CHARSET=utf8 COLLATE=utf8_bin;@g' /opt/jumpserver.sql
    else
        echo "备份数据库字符集正确";
    fi
    ```
    ```sh
    docker exec -it jms_mysql /bin/bash
    ```
    ```sh
    mysql -uroot -p$MYSQL_ROOT_PASSWORD
    ```
    ```mysql
    drop database jumpserver;
    create database jumpserver default charset 'utf8' collate 'utf8_bin';
    exit;
    exit
    ```
    ```sh
    ./jmsctl.sh restore_db /opt/jumpserver.sql
    # 注意: 确定在导入数据库的过程中没有错误
    ```
    ```sh
    ./jmsctl.sh start
    ```

!!! question "kombu.exceptions.OperationalError"
    ```vim
    # Redis < 5.0.0 导致, 请更新 Redis 版本
    kombu.exceptions.OperationalError:
    Cannot route message for exchange 'ansible': Table empty or key no longer exists.
    Probably the key ('_kombu.binding.ansible') has been removed from the Redis databa
    ```

!!! question "Internal Server Error"
    ```sh
    docker logs -f jms_core --tail 200
    # 查看是否有报错，如果没有或者不完整请进入容器查看日志
    ```
    ```sh
    docker exec -it jms_core /bin/bash
    cat logs/jumpserver.log
    # 根据报错处理
    ```

!!! question "修改对外访问端口"
    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim hl_lines="23"
    # 说明
    #### 这是项目总的配置文件, 会作为环境变量加载到各个容器中
    #### 格式必须是 KEY=VALUE 不能有空格等

    # Compose项目设置
    COMPOSE_PROJECT_NAME=jms
    COMPOSE_HTTP_TIMEOUT=3600
    DOCKER_CLIENT_TIMEOUT=3600
    DOCKER_SUBNET=192.168.250.0/24

    ## IPV6
    DOCKER_SUBNET_IPV6=2001:db8:10::/64
    USE_IPV6=0

    ### 持久化目录, 安装启动后不能再修改, 除非移动原来的持久化到新的位置
    VOLUME_DIR=/opt/jumpserver

    ## 是否使用外部MYSQL和REDIS
    USE_EXTERNAL_MYSQL=0
    USE_EXTERNAL_REDIS=0

    ## Nginx 配置，这个Nginx是用来分发路径到不同的服务
    HTTP_PORT=80           # 默认单节点对外 http  端口  (*)
    HTTPS_PORT=8443
    SSH_PORT=2222

    ## LB 配置, 这个Nginx是HA时可以启动负载均衡到不同的主机
    USE_LB=0
    LB_HTTP_PORT=80         
    LB_HTTPS_PORT=443
    LB_SSH_PORT=2223

    ## Task 配置
    USE_TASK=1

    ## XPack
    USE_XPACK=0


    # Koko配置
    CORE_HOST=http://core:8080
    ENABLE_PROXY_PROTOCOL=true


    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=
    BOOTSTRAP_TOKEN=
    LOG_LEVEL=INFO
    # SESSION_COOKIE_AGE=86400
    # SESSION_EXPIRE_AT_BROWSER_CLOSE=false

    ## MySQL数据库配置
    DB_ENGINE=mysql
    DB_HOST=mysql
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=
    DB_NAME=jumpserver

    ## Redis配置
    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_PASSWORD=

    ### Keycloak 配置方式
    ### AUTH_OPENID=true
    ### BASE_SITE_URL=https://jumpserver.company.com/
    ### AUTH_OPENID_SERVER_URL=https://keycloak.company.com/auth
    ### AUTH_OPENID_REALM_NAME=cmp
    ### AUTH_OPENID_CLIENT_ID=jumpserver
    ### AUTH_OPENID_CLIENT_SECRET=
    ### AUTH_OPENID_SHARE_SESSION=true
    ### AUTH_OPENID_IGNORE_SSL_VERIFICATION=true


    # Guacamole 配置
    JUMPSERVER_SERVER=http://core:8080
    JUMPSERVER_KEY_DIR=/config/guacamole/data/key/
    JUMPSERVER_RECORD_PATH=/config/guacamole/data/record/
    JUMPSERVER_DRIVE_PATH=/config/guacamole/data/drive/
    JUMPSERVER_ENABLE_DRIVE=true
    JUMPSERVER_CLEAR_DRIVE_SESSION=true
    JUMPSERVER_CLEAR_DRIVE_SCHEDULE=24

    # MySQL 容器配置
    MYSQL_ROOT_PASSWORD=
    MYSQL_DATABASE=jumpserver
    ```
    ```sh
    ./jmsctl.sh restart
    ```
