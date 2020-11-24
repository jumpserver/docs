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
        rm -rf /opt/py3
        python3 -m venv /opt/py3
        source /opt/py3/bin/activate
        cd /opt/jumpserver
        pip install -r requirements/requirements.txt
        ```

    === "脚本部署"
        ```sh
        cd /opt/setuptools
        ./jmsctl.sh stop
        git pull
        ```
        ```sh
        mysqldump -uroot jumpserver > /opt/jumpserver.sql
        ```
        ```sh
        yum -y remove mariadb-server mariadb-devel mariadb
        rm -rf /var/lib/mysql
        ```
        ```sh
        sh scripts/install_mysql.sh
        ```
        ```sh
        mysql -uroot
        ```
        ```mysql
        use jumpserver;
        source /opt/jumpserver.sql
        exit
        ```
        ```sh
        rm -rf /opt/py3
        python3 -m venv /opt/py3
        source /opt/py3/bin/activate
        cd /opt/jumpserver
        pip install -r requirements/requirements.txt
        ```

    ```sh
    ./jms start  # 启动 Core 看是否有报错
    ```

!!! question "启动报错 Cannot add foreign key constraint"
    - 先停止 core 服务

    ```sh
    cp /opt/jumpserver.sql /opt/jumpserver_bak.sql
    sed -i 's@CHARSET=utf8;@CHARSET=utf8 COLLATE=utf8_bin;@' /opt/jumpserver.sql
    ```
    ```sh
    mysql -uroot
    ```
    ```mysql
    drop database jumpserver;
    create database jumpserver default charset 'utf8' collate 'utf8_bin';
    use jumpserver;
    source /opt/jumpserver.sql;
    exit
    ```
