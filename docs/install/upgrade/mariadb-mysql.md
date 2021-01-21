# MariaDB5.5 迁移到 MySQL5.7

!!! warning "迁移前请一定要做好备份"

!!! tip "根据自己的部署方式参考下面对应的文档"
    === "手动部署"
        ```sh
        cd /opt/jumpserver
        source /opt/py3/bin/activate
        ./jms stop
        deactivate
        ```
        ```sh
        mysqldump -uroot -p jumpserver > /opt/jumpserver.sql
        ```
        ```sh
        if grep -q 'COLLATE=utf8_bin' /opt/jumpserver.sql; then
            echo "备份数据库字符集正确";
        else
            sed -i 's@CHARSET=utf8;@CHARSET=utf8 COLLATE=utf8_bin;@g' /opt/jumpserver.sql
        fi
        ```
        ```sh
        yum -y remove mariadb-server mariadb-devel mariadb
        rm -rf /var/lib/mysql
        ```
        ```sh
        yum -y localinstall http://mirrors.ustc.edu.cn/mysql-repo/mysql57-community-release-el7.rpm
        yum -y install mysql-community-server mysql-community-devel
        sed -i "s@--initialize @--initialize-insecure @g" /usr/bin/mysqld_pre_systemd
        systemctl enable mysqld
        systemctl start mysqld
        ```
        ```sh
        mysql -uroot -e "create database jumpserver default charset 'utf8' collate 'utf8_bin';"
        mysql -uroot -e "set global validate_password_policy=LOW;grant all on jumpserver.* to 'jumpserver'@'127.0.0.1' identified by 'rBi41SrDqlX4zsx9e1L0cqTP';flush privileges;"
        ```
        ```sh
        mysql -uroot -p
        ```
        ```mysql
        use jumpserver;
        source /opt/jumpserver.sql
        exit
        ```
        ```sh
        mysql_upgrade -uroot
        ```

    === "脚本部署"
        ```sh
        cd /opt/jumpserver-installer-v2.7.0
        ./jmsctl.sh stop
        ```
        ```sh
        mysqldump -uroot jumpserver > /opt/jumpserver.sql
        ```
        ```sh
        if grep -q 'COLLATE=utf8_bin' /opt/jumpserver.sql; then
            echo "备份数据库字符集正确";
        else
            cp /opt/jumpserver.sql /opt/jumpserver_bak.sql
            sed -i 's@CHARSET=utf8;@CHARSET=utf8 COLLATE=utf8_bin;@g' /opt/jumpserver.sql
        fi
        ```
        ```sh
        ./jmsctl.sh restore_db /opt/jumpserver.sql
        ```
        ```sh
        ./jmsctl.sh start
        ```

    - 启动 Core 看 jumpserver/logs/jumpserver.log 是否有报错

!!! question "启动报错 Cannot add foreign key constraint"
    - 数据库字符集不正确
    ```
    create database jumpserver default charset 'utf8' collate 'utf8_bin';
    ```
