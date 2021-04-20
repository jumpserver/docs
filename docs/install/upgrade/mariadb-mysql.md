# 数据库迁移

!!! warning "迁移前请一定要做好备份"
    - 从 v2.5 开始, 要求 MySQL >= 5.7
    - 推荐使用外置 数据库, 方便日后扩展升级

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 5.0  |
| MariaDB | >= 10.2 |    |       |         |


!!! tip "备份数据库"
    === "手动部署"
        ```sh
        cd /opt/koko
        ./koko -s stop
        # 更老的版本使用的 coco
        # cd /opt/coco
        # ./cocod stop
        ```
        ```sh
        /etc/init.d/guacd stop
        sh /config/tomcat9/bin/shutdown.sh
        ```
        ```sh
        cd /opt/jumpserver
        source /opt/py3/bin/activate
        ./jms stop
        ```
        ```sh
        cd /opt
        mv /opt/jumpserver /opt/jumpserver_bak
        ```
        ```sh
        mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
        ```

    === "组件容器化"
        ```sh
        docker stop jms_koko jms_guacamole
        docker rm jms_koko jms_guacamole
        # 更老的版本使用的 coco
        # docker stop jms_coco
        # docker rm jms_coco
        ```
        ```sh
        cd /opt/jumpserver
        source /opt/py3/bin/activate
        ./jms stop
        ```
        ```sh
        cd /opt
        mv /opt/jumpserver /opt/jumpserver_bak
        ```
        ```sh
        mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
        ```

    === "setuptools"
        ```sh
        cd /opt/setuptools
        ./jmsctl.sh stop
        docker rm jms_koko jms_guacamole
        systemctl disable jms_core
        mv /opt/jumpserver /opt/jumpserver_bak
        ```
        ```sh
        mysqldump -h127.0.0.1 -P3306 -ujumpserver -p jumpserver > /opt/jumpserver.sql
        ```

    === "docker 部署"
        ```sh
        docker cp jms_all:/opt/jumpserver /opt/jumpserver_bak
        docker exec -it jms_all env | egrep "SECRET_KEY|BOOTSTRAP_TOKEN"
        ```
        ```sh
        docker exec -it jms_all /bin/bash
        mysqldump -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASSWORD $DB_NAME > /opt/jumpserver.sql
        exit
        ```
        ```sh
        docker cp jms_all:/opt/jumpserver.sql /opt
        docker stop jms_all
        ```

    === "docker-compose"
        ```sh
        docker cp jms_core:/opt/jumpserver /opt/jumpserver_bak
        docker exec -it jms_core env | egrep "SECRET_KEY|BOOTSTRAP_TOKEN"
        ```
        ```sh
        docker exec -it jms_mysql /bin/bash
        mysqldump -uroot jumpserver > /opt/jumpserver.sql
        exit
        ```
        ```sh
        docker cp jms_mysql:/opt/jumpserver.sql /opt
        cd /opt/Dockerfile
        docker-compose stop
        ```
    === "jumpserver-installer"
        ```sh
        cd /opt/jumpserver-install-{{ jumpserver.version }}
        ./jmsctl.sh stop
        ```
        ```sh
        ./jmsctl.sh backup_db
        gunzip /opt/jumpserver/db_backup/jumpserver-2021-01-22_19:28:24.sql.gz
        mv /opt/jumpserver/db_backup/jumpserver-2021-01-22_19:28:24.sql /opt/jumpserver.sql
        ```

!!! tip "修改数据库字符集"
    ```sh
    if grep -q 'COLLATE=utf8_bin' /opt/jumpserver.sql; then
        cp /opt/jumpserver.sql /opt/jumpserver_bak.sql
        sed -i 's@COLLATE=utf8_bin@@g' /opt/jumpserver.sql
        sed -i 's@COLLATE utf8_bin@@g' /opt/jumpserver.sql
    else
        echo "备份数据库字符集正确";
    fi
    ```

!!! tip "迁移到新服务器"
    - 将导出的 /opt/jumpserver.sql 拷贝要新的服务器上面
    - 下面以迁移到其他 CentOS7 服务器为例, 实际操作过程中请自行替换对应的命令

    === "迁移到 MariaDB 10.5"
        ```sh
        vi /etc/yum.repos.d/MariaDB.repo
        ```
        ```vim
        [mariadb]
        name = MariaDB
        baseurl = http://mirrors.ustc.edu.cn/mariadb/yum/10.5/centos7-amd64
        gpgkey=http://mirrors.ustc.edu.cn/mariadb/yum/RPM-GPG-KEY-MariaDB
        gpgcheck=1
        ```
        ```sh
        yum clean all
        ```
        ```sh
        yum -y install MariaDB-server
        systemctl enable mariadb
        systemctl start mariadb
        ```
        ```sh
        mysql -uroot
        ```
        ```mysql
        create database jumpserver default charset 'utf8';
        create user 'jumpserver'@'%' identified by 'rBi41SrDqlX4zsx9e1L0cqTP';
        grant all on jumpserver.* to 'jumpserver'@'%';
        flush privileges;
        use jumpserver;
        source /opt/jumpserver.sql;
        exit;
        ```

    === "迁移到 MySQL 5.7"
        ```sh
        yum -y localinstall http://mirrors.ustc.edu.cn/mysql-repo/mysql57-community-release-el7.rpm
        yum -y install mysql-community-server mysql-community-devel
        ```
        ```sh
        sed -i "s@--initialize @--initialize-insecure @g" /usr/bin/mysqld_pre_systemd
        systemctl enable mysqld
        systemctl start mysqld
        ```
        ```sh
        mysql -uroot
        ```
        ```mysql
        create database jumpserver default charset 'utf8';
        set global validate_password_policy=LOW;
        create user 'jumpserver'@'%' identified by 'rBi41SrDqlX4zsx9e1L0cqTP';
        grant all on jumpserver.* to 'jumpserver'@'%';
        flush privileges;
        use jumpserver;
        source /opt/jumpserver.sql;
        exit;
        ```

    === "迁移到 MySQL 8.0"
        ```bash
        yum -y localinstall http://mirrors.ustc.edu.cn/mysql-repo/mysql80-community-release-el7.rpm
        yum -y install mysql-community-server mysql-community-devel
        ```
        ```sh
        sed -i "s@--initialize @--initialize-insecure @g" /usr/bin/mysqld_pre_systemd
        systemctl enable mysqld
        systemctl start mysqld
        ```
        ```sh
        mysql -uroot
        ```
        ```mysql
        create database jumpserver default charset 'utf8';
        set global validate_password.policy=LOW;
        create user 'jumpserver'@'%' identified by 'rBi41SrDqlX4zsx9e1L0cqTP';
        grant all on jumpserver.* to 'jumpserver'@'%';
        flush privileges;
        use jumpserver;
        source /opt/jumpserver.sql;
        exit;
        ```

    === "迁移到 Docker 容器"
        ```sh
        vi /opt/jumpserver/config/config.txt
        ```
        ```vim
        ## 是否使用外部MYSQL和REDIS
        USE_EXTERNAL_MYSQL=1

        ## MySQL数据库配置
        DB_ENGINE=mysql
        DB_HOST=mysql
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=rBi41SrDqlX4zsx9e1L0cqTP
        DB_NAME=jumpserver

        # MySQL 容器配置
        MYSQL_ROOT_PASSWORD=rBi41SrDqlX4zsx9e1L0cqTP
        MYSQL_DATABASE=jumpserver
        ```
        ```sh
        cd /opt/jumpserver-installer-{{ jumpserver.version }}
        ./jmsctl.sh start
        ```
        ```sh
        ./jmsctl.sh stop
        ```
        ```sh
        ./jmsctl.sh restore_db /opt/jumpserver.sql
        ```

    - 启动 jms_core 看 jumpserver.log 是否有报错

!!! question "启动报错 Cannot add foreign key constraint"
    ```sh
    if grep -q 'COLLATE=utf8_bin' /opt/jumpserver.sql; then
        cp /opt/jumpserver.sql /opt/jumpserver_bak.sql
        sed -i 's@COLLATE=utf8_bin@@g' /opt/jumpserver.sql
        sed -i 's@COLLATE utf8_bin@@g' /opt/jumpserver.sql
    else
        echo "备份数据库字符集正确";
    fi
    ```
    ```sh
    drop database jumpserver;
    create database jumpserver default charset 'utf8';
    source /opt/jumpserver.sql;
    ```
