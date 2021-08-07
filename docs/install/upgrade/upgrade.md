# 升级文档

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致，否则会导致数据库加密数据无法解密"
    - 更新前请一定要做好备份工作
    - [数据库迁移请先参考此文档](mariadb-mysql.md)
    - [升级前版本小于 1.4.4 请先按照此文档操作](1.0.0-1.4.3.md)
    - [升级前版本小于 1.4.5 请先按照此文档操作](1.4.4.md)
    - [未使用 installer 部署的用户请参考迁移说明迁移到最新版本](../migration.md)

!!! tip "环境说明"
    - 从 v2.5 开始，要求 MySQL >= 5.7
    - 从 v2.6 开始，要求 Redis >= 6
    - 推荐使用外置 数据库 和 Redis，方便日后扩展升级

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 6.0  |
| MariaDB | >= 10.2 |    |       |         |


## 升级说明

!!! tip "要求说明"
    - jumpserver 版本 >= v2.6.0
    - jumpserver 版本 <  v2.6.0 的请先参考上面的迁移文档迁移到最新版本

## 升级步骤

!!! tip "操作步骤"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```
    ```sh
    ./jmsctl.sh upgrade
    ```
    ```nginx hl_lines="1 37 66"
    是否将版本更新至 {{ jumpserver.version }} ? (y/n)  (默认为 n): y

    1. 检查配置变更
    配置文件位置: /opt/jumpserver/config
    /opt/jumpserver/config/config.txt  [ √ ]
    /opt/jumpserver/config/core/config.yml  [ √ ]
    /opt/jumpserver/config/koko/config.yml  [ √ ]
    /opt/jumpserver/config/mariadb/mariadb.cnf  [ √ ]
    /opt/jumpserver/config/mysql/my.cnf  [ √ ]
    /opt/jumpserver/config/nginx/lb_http_server.conf  [ √ ]
    /opt/jumpserver/config/nginx/lb_rdp_server.conf  [ √ ]
    /opt/jumpserver/config/nginx/lb_ssh_server.conf  [ √ ]
    /opt/jumpserver/config/redis/redis.conf  [ √ ]
    /opt/jumpserver/config/nginx/cert/server.crt  [ √ ]
    /opt/jumpserver/config/nginx/cert/server.key  [ √ ]
    完成

    2. 检查程序文件变更
    完成

    3. 升级镜像文件
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/lion:{{ jumpserver.version }} 	    [ OK ]
    完成

    4. 备份数据库
    正在备份...
    mysqldump: [Warning] Using a password on the command line interface can be insecure.
    [SUCCESS] 备份成功! 备份文件已存放至: /opt/jumpserver/db_backup/jumpserver-2021-03-19_08:32:39.sql

    5. 进行数据库变更
    表结构变更可能需要一段时间, 请耐心等待
    检测到 JumpServer 正在运行, 是否需要关闭并继续升级? (y/n)  (默认为 n): y

    Stopping jms_core ... done
    Stopping jms_koko ... done
    Stopping jms_lion ... done
    Stopping jms_nginx ... done
    Stopping jms_celery ... done
    Removing jms_core ... done
    Removing jms_koko ... done
    Removing jms_lion ... done
    Removing jms_nginx ... done
    Removing jms_celery ... done

    2021-03-19 08:32:44 Collect static files
    2021-03-19 08:32:44 Collect static files done
    2021-03-19 08:32:44 Check database structure change ...
    2021-03-19 08:32:44 Migrate model change to database ...

    473 static files copied to '/opt/jumpserver/data/static'.
    Operations to perform:
      Apply all migrations: acls, admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, ops, orgs, perms, sessions, settings, terminal, tickets, users
    Running migrations:
      No migrations to apply.
      # 有时候是下方红色的提示，忽略即可，不需要做处理。
      Your models have changes that are not yet reflected in a migration, and so won't be applied.
      Run 'manage.py makemigrations' to make new migrations, and then re-run 'manage.py migrate' to apply them.
    完成

    6. 清理镜像
    是否需要清理旧版本镜像文件? (y/n)  (默认为 n): y
    Untagged: jumpserver/core:v2.11.3
    Untagged: jumpserver/luna:v2.11.3
    Untagged: jumpserver/lina:v2.11.3
    Untagged: jumpserver/koko:v2.11.3
    Untagged: jumpserver/lion:v2.11.3
    完成

    7. 升级成功, 可以重新启动程序了
    cd /opt/jumpserver-installer-{{ jumpserver.version }}
    ./jmsctl.sh start
    ```

    ```sh
    ./jmsctl.sh start
    ```
