# 卸载文档

!!! warning "此操作不可逆, 请确认已经备份好数据库"

- 确保已经停止 jms koko guacamole 进程
- 确定数据已经处理完毕
- 请自行替换文中相关路径为你的实际环境路径

### 1. 正常部署卸载

```sh
rm -rf /opt/jumpserver
rm -rf /opt/koko /opt/kokodir
rm -rf /opt/docker-guacamole
rm -rf /opt/py3
rm -rf /config
rm -rf /etc/nginx/conf.d/jumpserver.conf
```

### 2. 脚本部署卸载

```sh
cd /opt/setuptools
./jmsctl.sh uninstall
```

### 3. docker 组件部署卸载

```sh
rm -rf /opt/jumpserver
rm -rf /opt/py3
rm -rf /etc/nginx/conf.d/jumpserver.conf
docker rm jms_koko
docker rm jms_guacamole
docker rmi jumpserver/jms_koko:1.5.8
docker rmi jumpserver/jms_guacamole:1.5.8
rm -rf /usr/lib/systemd/system/jms.service
rm -rf /opt/start_jms.sh
rm -rf /opt/stop_jms.sh
```

### 4. docker-compose 部署卸载

```sh
cd /opt/Dockerfile
docker-compose down
docker volume prune
docker rmi jumpserver/jms_core:1.5.8
docker rmi jumpserver/jms_koko:1.5.8
docker rmi jumpserver/jms_guacamole:1.5.8
docker rmi jumpserver/jms_nginx:1.5.8
docker rmi jumpserver/jms_redis:1.5.8
docker rmi jumpserver/jms_mysql:1.5.8
rm -rf /opt/Dockerfile
```

### 5. ansible-playbook 部署卸载

```sh
ansible-playbook uninstall.yml
```

- 删除数据库

```sh
mysql -uroot
```

```mysql
drop database jumpserver;
exit
```

- 清空 redis

```sh
redis-cli -h 127.0.0.1
```

```redis
flushall
exit
```
