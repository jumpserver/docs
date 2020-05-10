# 其他方式升级说明

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致, 否则会导致数据库加密数据无法解密"

## 极速安装升级

```sh
cd /opt/setuptools
git pull
```

```sh
./jmsctl.sh upgrade
```

!!! info "可以使用 ./jmsctl.sh -h 查看帮助"

## docker 升级

- 请一定要先做好备份
- 如果已经做了容器持久化, 直接更新镜像然后挂载 /var/lib/mysql 和 /opt/jumpserver/data 目录启动即可

```sh
docker stop jms_all
docker rm jms_all
```

```sh
docker run --name jms_all -d \  
  -v /opt/jumpserver/data:/opt/jumpserver/data \  
  -v /opt/jumpserver/mysql:/var/lib/mysql \
  -p 80:80 \  
  -p 2222:2222 \  
  -e SECRET_KEY=xxxxxx \  
  -e BOOTSTRAP_TOKEN=xxx \  
  jumpserver/jms_all:1.5.8
```

- 如果没有做容器持久化, 需要先将文件拷出

```sh
mkdir /opt/jumpserver
docker cp jms_all:/opt/jumpserver/data /opt/jumpserver/data
docker cp jms_all:/var/lib/mysql /opt/jumpserver/mysql
```

- 然后挂载到新版本里面

```sh
docker stop jms_all
docker rm jms_all
```

```sh
docker run --name jms_all -d \  
  -v /opt/jumpserver/data:/opt/jumpserver/data \  
  -v /opt/jumpserver/mysql:/var/lib/mysql \
  -p 80:80 \  
  -p 2222:2222 \  
  -e SECRET_KEY=xxxxxx \  
  -e BOOTSTRAP_TOKEN=xxx \  
  jumpserver/jms_all:1.5.8
```

- 如果数据库已经外置, 则只需要挂载 jumpserver/data 即可

```sh
docker run --name jms_all -d \  
  -v /opt/jumpserver:/opt/jumpserver/data/media \  
  -p 80:80 \  
  -p 2222:2222 \  
  -e SECRET_KEY=xxxxxx \  
  -e BOOTSTRAP_TOKEN=xxx \  
  -e DB_HOST=192.168.x.x \  
  -e DB_PORT=3306 \  
  -e DB_USER=root \  
  -e DB_PASSWORD=xxx \  
  -e DB_NAME=jumpserver \  
  jumpserver/jms_all:1.5.8
```

## docker-compose 升级

- 容器默认已经做好了持久化

```sh
docker volume ls
```

```sh
cd /opt/Dockerfile
docker-compose down
```

```sh
git pull
```

```sh
cat docker-compose.yml
```

!!! warning "注意, 新版本更改了 jumpserver/data 挂载目录, 请自行完成替换或者还原"

```sh
docker-compose up -d
```

## ansible-playbook 升级

- 注意做好备份工作

```sh
ansible-playbook upgrade.yml
```
