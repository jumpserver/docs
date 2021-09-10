# 升级文档

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致，否则会导致数据库加密数据无法解密"
    - 更新前请一定要做好备份工作
    - [数据库迁移请先参考此文档](mariadb-mysql.md){:target="_blank"}
    - [升级前版本小于 1.4.4 请先按照此文档操作](1.0.0-1.4.3.md){:target="_blank"}
    - [升级前版本小于 1.4.5 请先按照此文档操作](1.4.4.md){:target="_blank"}
    - [未使用 installer 部署的用户请参考迁移说明迁移到最新版本](../migration.md){:target="_blank"}

!!! tip "环境说明"
    - 从 v2.5 开始，要求 MySQL >= 5.7
    - 从 v2.6 开始，要求 Redis >= 6
    - 推荐使用外置 数据库 和 Redis，方便日后扩展升级

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 6.0  |
| MariaDB | >= 10.2 |    |       |         |

## 升级说明

!!! tip "要求说明"
    - [未使用 installer 部署的用户请参考迁移说明迁移到最新版本](../migration.md){:target="_blank"}

## 升级步骤

=== "在线升级"
    !!! tip ""
        ```sh
        cd /opt
        yum -y install wget
        wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.version }}
        ```
        ```sh
        ./jmsctl.sh upgrade
        ./jmsctl.sh start
        ```

=== "离线升级(amd64)"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/amd64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        # 获取离线包: https://community.fit2cloud.com/#/products/jumpserver/downloads
        cd /opt
        unzip jumpserver-offline-installer-{{ jumpserver.version }}-amd64-{{ installer.amd64 }}.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.version }}-amd64-{{ installer.amd64 }}
        ```
        ```sh
        ./jmsctl.sh upgrade
        ./jmsctl.sh start
        ```

=== "离线升级(arm64)"
    !!! tip ""
        从飞致云社区 [下载最新的 linux/arm64 离线包](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, 并上传到部署服务器的 /opt 目录

    !!! tip ""
        ```sh
        cd /opt
        unzip jumpserver-offline-installer-{{ jumpserver.version }}-arm64-{{ installer.arm64 }}.tar.gz
        cd jumpserver-offline-installer-{{ jumpserver.version }}-arm64-{{ installer.arm64 }}
        ```
        ```sh
        ./jmsctl.sh upgrade
        ./jmsctl.sh start
        ```

=== "Helm 升级"
    !!! tip ""
        ```sh
        # 请先手动备份好数据库, 然后继续操作
        cd /opt/helm
        cp values.yaml values.yaml.bak
        ```
        ```sh
        # 获取最新代码
        git pull
        ```
        ```sh
        # 修改配置文件, 将设置还原
        vi values.yaml
        ```
        ```sh
        # 执行升级操作
        helm upgrade --install jumpserver ./ -n default
        ```
