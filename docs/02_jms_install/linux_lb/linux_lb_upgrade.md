# 注意事项
## 1 关于 LB 模式的环境升级
!!! warning "更新前请一定要做好备份工作"
    - 升级前请关闭所有 JumpServer 节点。
    - 在任意一个 JumpServer 节点按照升级文档完成升级操作。
    - 仔细检查该节点升级过程确保无异常。
    - 然后按照升级文档对其他 JumpServer 节点升级即可。

    ```sh
    cd /opt
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```
    ```sh
    # 额外节点可以设置 SKIP_BACKUP_DB=1 跳过数据库备份, 第一个升级节点不要跳过备份
    export SKIP_BACKUP_DB=1
    ./jmsctl.sh upgrade
    ```