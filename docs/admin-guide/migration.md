# 迁移文档

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致, 否则会导致数据库加密数据无法解密"

- 请不要跨版本迁移数据库

### 1. 备份数据库

```sh
mysqldump -uroot -p jumpserver > /opt/jumpserver.sql
```

### 2. 迁移数据

- 登录新的服务器，拷贝 jumpserver 和 jumpserver.sql 到 /opt 目录

```sh
scp -r root@jumpserver服务器ip:/opt/jumpserver /opt/
scp -r root@jumpserver服务器ip:/opt/jumpserver.sql /opt/
```

### 3. 配置新服务器

```sh
yum -y install wget gcc epel-release git
```

```sh
yum -y install mariadb mariadb-devel mariadb-server MariaDB-shared redis
```

```sh
systemctl enable redis mariadb
```

```sh
systemctl start redis mariadb
```

```sh
mysql -uroot
```

```mysql
create database jumpserver default charset 'utf8' collate 'utf8_bin';
grant all on jumpserver.* to 'jumpserver'@'127.0.0.1' identified by 'weakPassword';
use jumpserver;
source /opt/jumpserver.sql;
quit
```

!!! info "这里创建数据库应用的账户密码建议与 jumpserver/config.yml 里面的数据库信息一致"

```sh
yum -y install python36 python36-devel
```

```sh
cd /opt
python3.6 -m venv py3
source /opt/py3/bin/activate
```

```sh
cd /opt/jumpserver/requirements
yum -y install $(cat rpm_requirements.txt)
```

```sh
pip install wheel
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

```sh
cd /opt/jumpserver
./jms start
```

??? tip "可以 -d 参数在后台运行"
    ```sh
    ./jms start -d  
    ```

- 其他组件参考安装文档重新设置即可
