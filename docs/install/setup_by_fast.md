# 安装文档

!!! info "说明"
    全新安装的 Linux(x64)  
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
| MySQL   | >= 5.7  |    | Redis | >= 6.0  |
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
        wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.version }}
        cat config-example.txt
        ```

    ???+ info "配置文件说明"
        ```vim
        # 以下设置如果为空系统会自动生成随机字符串填入
        ## 迁移请修改 SECRET_KEY 和 BOOTSTRAP_TOKEN 为原来的设置
        ## 完整参数文档 https://docs.jumpserver.org/zh/master/admin-guide/env/

        ## 安装配置, 默认使用华为云加速下载, 非中国用户可以注释掉 DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        DOCKER_IMAGE_PREFIX=swr.cn-south-1.myhuaweicloud.com
        VOLUME_DIR=/opt/jumpserver
        DOCKER_DIR=/var/lib/docker
        SECRET_KEY=
        BOOTSTRAP_TOKEN=
        LOG_LEVEL=ERROR

        ##  MySQL 配置, USE_EXTERNAL_MYSQL=1 表示使用外置数据库, 请输入正确的 MySQL 信息
        USE_EXTERNAL_MYSQL=0
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=jumpserver

        ##  Redis 配置, USE_EXTERNAL_REDIS=1 表示使用外置数据库, 请输入正确的 Redis 信息
        USE_EXTERNAL_REDIS=0
        REDIS_HOST=redis
        REDIS_PORT=6379
        REDIS_PASSWORD=

        ## Compose 项目设置, 如果 192.168.250.0/24 网段与你现有网段冲突, 请修改然后重启 JumpServer
        COMPOSE_PROJECT_NAME=jms
        COMPOSE_HTTP_TIMEOUT=3600
        DOCKER_CLIENT_TIMEOUT=3600
        DOCKER_SUBNET=192.168.250.0/24

        ## IPV6 设置, 容器是否开启 ipv6 nat, USE_IPV6=1 表示开启, 为 0 的情况下 DOCKER_SUBNET_IPV6 定义不生效
        USE_IPV6=0
        DOCKER_SUBNET_IPV6=2001:db8:10::/64

        ## Nginx 配置, USE_LB=1 表示开启, 为 0 的情况下, HTTPS_PORT 定义不生效
        HTTP_PORT=80
        SSH_PORT=2222
        RDP_PORT=3389

        USE_LB=0
        HTTPS_PORT=443

        ## Task 配置, 是否启动 jms_celery 容器, 单节点必须开启
        USE_TASK=1

        ## XPack, USE_XPACK=1 表示开启, 开源版本设置无效
        USE_XPACK=0

        # Core 配置, Session 定义, SESSION_COOKIE_AGE 表示闲置多少秒后 session 过期, SESSION_EXPIRE_AT_BROWSER_CLOSE=true 表示关闭浏览器即 session 过期
        # SESSION_COOKIE_AGE=86400
        SESSION_EXPIRE_AT_BROWSER_CLOSE=true

        # Koko Lion XRDP 组件配置
        CORE_HOST=http://core:8080

        # 额外的配置
        CURRENT_VERSION=
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
      ... 省略一堆 Applying xxx.xxx_xxx_xxx_xxx... OK
      Applying users.0031_auto_20201118_1801... OK
      # 确定这上面都是显示 ok，不能有 error
    2021-02-08 14:59:31 [cache INFO] CACHE: Send refresh task <orgs.caches.OrgResourceStatisticsCache object at 0x7fb9122ce0d0>.('nodes_amount',)
    Operations to perform:
      Apply all migrations: admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, ops, orgs, perms, sessions, settings, terminal, tickets, users
    Running migrations:
      No migrations to apply.

    - Start Flower as Task Monitor

    - Start Daphne ASGI WS Server

    # 到这里为止，如果上面都是 ok 没有 error的话，就可以重新执行 ./jmsctl.sh start 启动了

    2021-02-08 15:01:02 Check service status: gunicorn -> running at 38
    2021-02-08 15:01:02 Check service status: flower -> running at 44
    2021-02-08 15:01:02 Check service status: daphne -> running at 54
    ```
    ```sh
    # 确定上面都是 ok 的没有报错, 提示 Check service status 后就可以重新启动其他组件
    ./jmsctl.sh start
    ```

## 使用方式

- 安装目录 /opt/jumpserver-installer-{{ jumpserver.version }}
- 配置文件 /opt/jumpserver/config/config.txt

!!! tip "Install"
    ```sh
    ./jmsctl.sh install
    ```

!!! tip "Help"
    ```sh
    ./jmsctl.sh -h
    ```

后续的使用请参考 [安全建议](install_security.md) [快速入门](../../admin-guide/quick_start/)  
