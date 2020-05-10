# Ansible 集群部署

## Ansible-Playbook

!!! warning "本项目请先自行调优后再使用, 请勿直接在生产环境进行使用"

!!! info "说明"
    本文档需要非常专业的能力来解决一些集群问题，如集群崩溃 集群分离 集群扩展 lvs 负载均衡策略 故障排查 以及 集群组件存活检测机制等。在这些问题上你可能无法获得 JumpServer 额外的技术支持。

!!! info "部署目标机器需满足以下条件"

- 至少需要 3 实例
- nfs mariadb redis 可以处于同一主机
- core koko guacamole 可以处于同一主机
- nginx 必须位于单独的主机

!!! note "注: MariaDB Redis 未做集群, 请根据实际环境自行进行部署或者选择已经就绪的 MySQL Server 和 Redis Server"

### 1. 部署中控

- 中控机可以是部署目标机器中的某一台
- 系统要求 CentOS 7.x 操作系统
- 该机器需开放外网访问

!!! warning "需要部署中控机一台"

### 2. 安装依赖

- 以 root 用户登录中控机, 执行以下命令

```sh
yum -y install epel-release git curl sshpass
yum -y install python2-pip
```

### 3. SSH key

```sh
ssh-keygen -t rsa
```

!!! info "生成 ssh key"

### 4. 下载项目

```sh
cd /opt
git clone --depth=1 https://github.com/wojiushixiaobai/jms_ansible.git
```

### 5. 安装依赖

```sh
cd jms_ansible
mkdir ~/.pip
echo -e "[easy_install]\nindex_url = https://mirrors.aliyun.com/pypi/simple/" > ~/.pydistutils.cfg
echo -e "[global]\nindex-url = https://mirrors.aliyun.com/pypi/simple/\n\n[install]\ntrusted-host=mirrors.aliyun.com" > ~/.pip/pip.conf
pip install -r requirements/requirements.txt
```

### 6. 分配资源

```sh
vi inventory.ini
```
```vim
[nfs]
192.168.1.147  # 用作部署 nfs 服务器的 ip, 目前只能指定一台资产

[nginx]
192.168.1.146  # 用作部署 nginx 服务器的 ip, 指定一台资产即可

[mariadb]
192.168.1.147  # 用作部署 mysql 服务器的 ip, 目前只能指定一台资产
# 如果你已经有部署好的 mysql server, 可以不设置

[redis]
192.168.1.147  # 用作部署 redis 服务器的 ip, 目前只能指定一台资产
# 如果你已经有部署好的 redis server, 可以不设置

[core_master]  # 用作部署 core 主服务器的 ip, 指定一台资产即可
192.168.1.148

[core_slave]
192.168.1.148  # 用作部署 core 从服务器的 ip, 可以指定多台资产, 主从之间通过 tengine 负载均衡
# 192.168.1.xx
# 192.168.x.xx

[koko]
192.168.1.148  # 用作部署 koko 服务器的 ip, 可以指定多台资产, 通过 tengine 负载均衡
# 192.168.1.xx
# 192.168.x.xx

[guacamole]
192.168.1.148  # 用作部署 guacamole 服务器的 ip, 可以指定多台资产, 通过 tengine 负载均衡
# 192.168.1.xx
# 192.168.x.xx

[nfs:vars]
nfs_perm = 192.168.1.0/24(rw,sync,no_root_squash)  # 这里是 nfs 的策略, 根据你的实际情况进行修改, 也可以直接授权网段

[nginx:vars]
# https_port = 443  # 暂时不设置, 等待后续更新
ssh_port = 2222  # nginx 对外的 ssh 端口, 用户可以通过此端口登录到 jumpserver 跳板机

[db_info:children]
mariadb
core_master
core_slave

[db_info:vars]
db_name = jumpserver      # 为 jumpserver 创建的数据库名称
db_user = jumpserver      # 为 jumpserver 创建的连接用户
db_host = 192.168.1.147   # 请改成你的 mysql 数据库 ip
db_passwd = weakPassword  # 请更改此密码为更安全的密码
# 如果你已经有部署好的 mysql server, 在这里指定

[redis_info:children]
redis
core_master
core_slave
koko

[redis_info:vars]
redis_host = 192.168.1.147   # redis 服务器的 ip
redis_passwd = weakPassword  # redis 服务器的密码
# 如果你已经有部署好的 redis server, 在这里指定

[nfs_info:children]
nginx
core_master
core_slave

[nfs_info:vars]
nfs_server = 192.168.1.147  # 此处修改成你的 nfs 服务器 ip

[nginx_info:children]
nginx
koko

[nginx_info:vars]
http_port = 80  # nginx 对外的 http 端口, 用户通过此端口来访问 jumpserver

[core:children]
core_master
core_slave

[core:vars]
secret_key = gIQ3sUfkCQXd295d8Wwkvu3stAoeVAGvpsiblCEjRud9uwIFB0  # jumpserver 默认的加密 key, 请更改并牢记
# 丢失此 key 会导致加密的所有数据无法解密, 请保管到安全的位置

[core_info:children]
core_master
core_slave
koko
guacamole

[core_info:vars]
bootstrap_token = j6qfkdQWWrdVACcy   # koko 和 guacamole 认证时需要的 token, 请随机数生成并更改, 不需要记住
nginx_server = 192.168.1.146         # nginx 服务器的 ip 地址

[all:vars]
ansible_user = root
install_dir = /opt                   # jumpserver安装的位置, 建议默认, 修改此选项, 下面 nfs 客户端挂载的位置也需要修改
ntp_server = ntp1.aliyun.com         # ntp 需要时间同步
jms_version = 1.5.8                  # jumpserver 的版本
nfs_src_dir = /data                  # nfs 服务端挂载位置, 建议默认
nfs_dest_dir = /opt/jumpserver/data  # nfs 客户端挂载的位置, 必须指向 jumpserver 安装目录的 data 文件夹
jms_network = 192.168.1.0/24         # 设置防火墙需要, 授权整个网段, 请修改成你部署 jumpserver 的资产网段

enable_mysql = True                  # 如果你已经有部署好的 mysql server, 请修改此项为 False, 并在上面指定即可
enable_redis = True                  # 如果你已经有部署好的 redis server, 请修改此项为 False, 并在上面指定即可
enable_selinux = True                # 如果你的资产关闭了 selinux , 请修改此项为 False
enable_firewalld = True              # 如果你的资产关闭了 firewalld , 请修改此项为 False
```

!!! warning "请仔细看说明"

### 7. 配置互信

```sh
ansible-playbook deploy_user.yml -uroot -k
```

!!! tip "按提示输入部署目标机器的 root 用户密码"

### 8. 测试互信

```sh
ansible all -m shell -a 'whoami'
```

### 9. 开始部署

```sh
ansible-playbook deploy.yml
```

- 如果安装过程提示错误, 可以尝试重新执行 ansible-playbook deploy.yml  
- 暂时未集成升级功能, 暂时未集成卸载功能(等待后续更新)
