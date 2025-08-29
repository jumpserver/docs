# 部署 JumpServer 02 节点

## 1 准备工作
### 1.1 环境信息
!!! tip ""
    - JumpServer_Node_02 服务器信息如下: 
    ```sh
    192.168.100.22
    ```


## 2 配置 NFS
### 2.1 安装 NFS 依赖包
!!! tip ""
    ```sh
    apt -y install nfs-utils
    showmount -e 192.168.100.11
    ```

### 2.2 挂载 NFS 目录
!!! tip ""
    ```sh
    # 将 Core 持久化目录挂载到 NFS, 默认 /opt/jumpserver/core/data, 请根据实际情况修改
    # JumpServer 持久化目录定义相关参数为 VOLUME_DIR, 在安装 JumpServer 过程中会提示
    mkdir /opt/jumpserver/core/data
    mount -t nfs 192.168.100.11:/data /opt/jumpserver/core/data
    ```

### 2.3 配置 NFS 共享目录开机自动挂载
!!! tip ""
    ```sh
    # 可以写入到 /etc/fstab, 重启自动挂载. 注意: 设置后如果 nfs 损坏或者无法连接该服务器将无法启动
    echo "192.168.100.11:/data /opt/jumpserver/core/data nfs defaults 0 0" >> /etc/fstab
    ```

## 3 安装 JumpServer 
### 3.1 下载 jumpserver-install 软件包
!!! tip ""
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.tag }}/jumpserver-installer-{{ jumpserver.tag }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.tag }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.tag }}
    ```
!!! info "如果环境无法访问外网，请于 https://community.fit2cloud.com/#/products/jumpserver/downloads 下载离线版本安装包。"
### 3.2 修改临时配置文件
!!! tip ""
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="9 10"

    # 修改下面选项, 其他保持默认, 请勿直接复制此处内容。配置文件中的 bootstrap_token , SECRET_KEY 必须要和集群内其他 JumpServer 节点一致, 否则数据库数据和组件注册将受到影响。

    # 安装配置
    ### 注意持久化目录 VOLUME_DIR, 如果上面 NFS 挂载其他目录, 此处也要修改. 如: NFS 挂载到 /data/jumpserver/core/data, 则 VOLUME_DIR=/data/jumpserver
    VOLUME_DIR=/data/jumpserver

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密, 请勿直接复制下面的字符串
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW    # 与其它 JumpServer 节点一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                                 # 与其它 JumpServer 节点一致 (*)
    LOG_LEVEL=ERROR                                                  # 日志等级
    # SESSION_COOKIE_AGE=86400                                       # cookie 过期时间，单位秒，默认一天
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True                             # 关闭浏览器 session 过期

    # PostgreSQL 配置
    DB_ENGINE=postgresql
    DB_HOST=192.168.100.11
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=KXOeyNgDeTdpeu9q
    DB_NAME=jumpserver

    # Redis 配置

    REDIS_HOST=192.168.100.11
    REDIS_PORT=6379
    REDIS_PASSWORD=KXOeyNgDeTdpeu9q

    # KoKo Lion 配置
    SHARE_ROOM_TYPE=redis                                            # KoKo Lion 使用 redis 共享
    REUSE_CONNECTION=False                                           # Koko 禁用连接复用
    ```

### 3.3 执行脚本安装 JumpServer 服务
!!! tip ""
    ```sh
    ./jmsctl.sh install
    # 检查脚本默认配置是否和修改的配置文件一致，等待安装完毕即可。
    ```

### 3.4 启动 JumpServer 服务
!!! tip ""
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_lion      ... done
    Creating jms_koko      ... done
    Creating jms_magnus    ... done
    Creating jms_web       ... done
    ```

## 扩展更多节点
!!! tip ""
    - 如有更多节点扩展需求，安装和配置方式与上述节点相同。
    - 请确保各节点间配置文件中的 BOOTSTRAP_TOKEN 和 SECRET_KEY 保持一致。