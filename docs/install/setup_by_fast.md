# 安装文档

!!! info "说明"
    全新安装的 Centos7 (7.x)  
    需要连接 互联网  
    使用 root 用户执行  

- 可以使用由 [华为云](https://www.huaweicloud.com/) 提供的容器镜像服务 :heart:{: .heart }

| 区域          | 镜像仓库地址                         | 配置文件 /opt/jumpserver/config/config.txt                |
| :----------- | :----------------------------------- | -------------------------------------------------------- |
| 华北-北京一   | swr.cn-north-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-1.myhuaweicloud.com     |
| 华北-北京四   | swr.cn-north-4.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-north-4.myhuaweicloud.com     |
| 华南-广州     | swr.cn-south-1.myhuaweicloud.com     | DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com     |
| 华东-上海一   | swr.cn-east-3.myhuaweicloud.com      | DOCKER_IMAGE_PREFIX=swr.cn-east-3.myhuaweicloud.com      |
| 亚太-香港     | swr.ap-southeast-1.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-1.myhuaweicloud.com |
| 亚太-新加坡   | swr.ap-southeast-3.myhuaweicloud.com | DOCKER_IMAGE_PREFIX=swr.ap-southeast-3.myhuaweicloud.com |

## 安装方式

- 可以参考 [安装演示视频](https://www.bilibili.com/video/bv19a4y1i7i9)

!!! info "外置环境要求"
    - 推荐使用外置 数据库 和 Redis, 方便日后扩展升级

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 5.0  |
| MariaDB | >= 10.2 |    |       |         |

=== "自动部署"
    !!! tip ""
        ```sh
        curl -sSL https://github.com/jumpserver/jumpserver/releases/download/{{ jumpserver.version }}/quick_start.sh | bash
        ```

=== "手动部署"
    !!! tip ""
        ```sh
        cd /opt
        yum -y install wget
        wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.version }}
        cat config-example.txt
        ```

    ???+ info "配置文件说明"
        ```vim
        # 以下设置如果为空系统会自动生成随机字符串填入
        ## 迁移请修改 SECRET_KEY 和 BOOTSTRAP_TOKEN 为原来的设置

        ## 安装配置
        DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        VOLUME_DIR=/opt/jumpserver
        DOCKER_DIR=/var/lib/docker
        SECRET_KEY=
        BOOTSTRAP_TOKEN=
        LOG_LEVEL=ERROR

        ## 使用外置 MySQL 配置
        USE_EXTERNAL_MYSQL=0
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        ## 使用外置 Redis 配置
        USE_EXTERNAL_REDIS=0
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        ## Compose 项目设置
        COMPOSE_PROJECT_NAME=jms
        COMPOSE_HTTP_TIMEOUT=3600
        DOCKER_CLIENT_TIMEOUT=3600
        DOCKER_SUBNET=192.168.250.0/24

        ## IPV6
        DOCKER_SUBNET_IPV6=2001:db8:10::/64
        USE_IPV6=0

        ## Nginx 配置，这个 Nginx 是用来分发路径到不同的服务
        HTTP_PORT=80
        HTTPS_PORT=443
        SSH_PORT=2222

        ## LB 配置, 这个 Nginx 是 HA 时可以启动负载均衡到不同的主机
        USE_LB=0
        LB_HTTP_PORT=80
        LB_HTTPS_PORT=443
        LB_SSH_PORT=2222

        ## Task 配置
        USE_TASK=1

        ## XPack
        USE_XPACK=0

        # Mysql 容器配置
        MYSQL_ROOT_PASSWORD=
        MYSQL_DATABASE=jumpserver

        # Core 配置
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=true

        ### Keycloak 配置方式
        ### AUTH_OPENID=true
        ### BASE_SITE_URL=https://jumpserver.company.com/
        ### AUTH_OPENID_SERVER_URL=https://keycloak.company.com/auth
        ### AUTH_OPENID_REALM_NAME=cmp
        ### AUTH_OPENID_CLIENT_ID=jumpserver
        ### AUTH_OPENID_CLIENT_SECRET=
        ### AUTH_OPENID_SHARE_SESSION=true
        ### AUTH_OPENID_IGNORE_SSL_VERIFICATION=true

        # Koko 配置
        CORE_HOST=http://core:8080

        # Guacamole 配置
        JUMPSERVER_SERVER=http://core:8080
        JUMPSERVER_KEY_DIR=/config/guacamole/data/key/
        JUMPSERVER_RECORD_PATH=/config/guacamole/data/record/
        JUMPSERVER_DRIVE_PATH=/config/guacamole/data/drive/
        JUMPSERVER_ENABLE_DRIVE=true
        JUMPSERVER_CLEAR_DRIVE_SESSION=true
        JUMPSERVER_CLEAR_DRIVE_SCHEDULE=24
        ```

??? warning "如果启动过程报错请查看此处的帮助文档"
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
    # 确定上面都是 ok, 没有 error, 重新 start 即可
    ./jmsctl.sh start
    ```

## 使用方式

- 安装目录 /opt/jumpserver-install-{{ jumpserver.version }}

!!! tip "Install"
    ```sh
    ./jmsctl.sh install
    ```

!!! tip "Help"
    ```sh
    ./jmsctl.sh -h
    ```

!!! tip "Upgrade"
    ```sh
    ./jmsctl.sh check_update
    ```

后续的使用请参考 [安全建议](install_security.md) [快速入门](../../admin-guide/quick_start/)  
