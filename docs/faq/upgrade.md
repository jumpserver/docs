# 升级问题

### 1. 导入数据库报错

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
# 如果变量 $MARIADB_ROOT_PASSWORD 不存在，请使用 $MYSQL_ROOT_PASSWORD
mysql -uroot -p$MARIADB_ROOT_PASSWORD
```
```mysql
drop database jumpserver;
create database jumpserver default charset 'utf8';
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

### 2. 升级过程提示错误

```sh
./jmsctl.sh upgrade
```

=== "Table '表名' already exists"
    ```vim
    Operations to perform:
      Apply all migrations: acls, admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, notifications, ops, orgs, perms, sessions, settings, terminal, tickets, users

    Running migrations:
      Applying tickets.0010_auto_20210812_1618...Traceback (most recent call last):
      File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 82, in _execute
        return self.cursor.execute(sql)
      File "/usr/local/lib/python3.8/site-packages/django/db/backends/mysql/base.py", line 73, in execute
        return self.cursor.execute(query, args)
      File "/usr/local/lib/python3.8/site-packages/MySQLdb/cursors.py", line 206, in execute
        res = self._query(query)
      File "/usr/local/lib/python3.8/site-packages/MySQLdb/cursors.py", line 319, in _query
        db.query(q)
      File "/usr/local/lib/python3.8/site-packages/MySQLdb/connections.py", line 259, in query
        _mysql.connection.query(self, query)
      MySQLdb._exceptions.OperationalError: (1050, "Table 'tickets_approvalrule' already exists")
    ```
    !!! warning ""
        此错误通常于手动导入备份数据库后启动出现，原因一般为新的数据库名称与旧数据库名称不一致或者导入数据库过程有错误导致

=== "Cannot add foreign key constraint"
    ```vim
    Operations to perform:
      Apply all migrations: acls, admin, applications, assets, audits, auth, authentication, captcha, common, contenttypes, django_cas_ng, django_celery_beat, jms_oidc_rp, notifications, ops, orgs, perms, sessions, settings, terminal, tickets, users

    Running migrations:
      Applying assets.0084_auto_20220112_1959...2022-01-24 14:38:47 Perform migrate failed, exit
        Traceback (most recent call last):
      File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 84, in _execute
        return self.cursor.execute(sql, params)
      File "/usr/local/lib/python3.8/site-packages/django/db/backends/mysql/base.py", line 73, in execute
        return self.cursor.execute(query, args)
      File "/usr/local/lib/python3.8/site-packages/MySQLdb/cursors.py", line 206, in execute
        res = self._query(query)
      File "/usr/local/lib/python3.8/site-packages/MySQLdb/cursors.py", line 319, in _query
        db.query(q)
      File "/usr/local/lib/python3.8/site-packages/MySQLdb/connections.py", line 259, in query
        _mysql.connection.query(self, query)
    MySQLdb._exceptions.IntegrityError: (1215, 'Cannot add foreign key constraint')
    ```
    !!! warning ""
        如果数据库里面包含多种不一样的排序规则依旧会报错

    ```sh
    # 通过 grep 检查 sql 文件
    mysqldump -uroot -p jumpserver > jumpserver.sql

    # 检查字符集, 如果都返回 utf8 则无问题
    grep -r "DEFAULT CHARSET=" jumpserver.sql

    # 检查排序规则，正常情况下返回都是空或者唯一
    grep -r "COLLATE=" jumpserver.sql
    grep -r "COLLATE " jumpserver.sql

    # 如果上述结果不一致，请手动修正数据库。
    ```
