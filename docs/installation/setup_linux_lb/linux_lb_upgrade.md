# 注意事项
## 1 关于集群模式的环境升级
!!! warning "更新前请一定要做好备份工作"
    - 升级前请关闭所有 JumpServer 节点。
    - 在任意一个 JumpServer 节点按照升级文档完成升级操作。
    - 仔细检查该节点升级过程确保无异常。
    - 然后按照升级文档对其他 JumpServer 节点升级即可。

!!! tip ""
    - 从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录。

!!! tip ""
    ```sh
    cd /opt
    tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-amd64.tar.gz
    cd jumpserver-offline-installer-{{ jumpserver.tag }}-amd64
    ```
    ```sh
    # 额外节点可以设置 SKIP_BACKUP_DB=1 跳过数据库备份, 第一个升级节点不要跳过备份
    export SKIP_BACKUP_DB=1
    ./jmsctl.sh upgrade
    ./jmsctl.sh start
    ```