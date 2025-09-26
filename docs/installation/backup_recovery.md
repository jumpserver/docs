# 数据备份以及恢复

## 1 概述

!!! tip ""
    **JumpServer 堡垒机数据主要分为两部分：**

    - 数据库数据：用户数据、资产数据、账号数据、操作日志、命令记录等。
    - 静态文件：会话录像、图片、系统日志、配置文件等。

## 2 数据库备份和恢复

!!! warning "注意"
    - 本文是以同一套环境备份恢复为例，如果是跨环境恢复，请确保数据库版本型号一致，配置文件中的 **BOOTSTRAP_TOKEN** 和 **SECRET_KEY** 需要与导出来源的一致！

!!!tip ""
    === "备份"
        - 在堡垒机任意一节点（多节点任意一节点即可）执行以下命令备份数据库信息：

          ```sh
          ./jmsctl.sh backup_db
          ```

        - 备份文件和当前配置文件会默认保存在持久化文件 /data/jumpserver/backups 目录下，文件名格式为 jumpserver-v4.10.9-ee-xxxx-xx-xx_xx:xx:xx.dump。
        - 如果使用 MySQL 或 MariaDB 作为数据库，文件名格式为 jumpserver-v4.10.9-xxxx-xx-xx_xx:xx:xx.sql。
        
    === "恢复"
        - 在堡垒机任意一节点（多节点任意一节点即可）执行以下命令恢复数据库信息：

          ```sh
          jmsctl restore_db /data/jumpserver/backups/jumpserver-v4.10.9-ee-xxxx-xx-xx_xx:xx:xx.dump
          ```

## 3 静态文件备份

!!! warning "注意"
    - 静态文件主要包括会话录像、图片、系统日志等，静态文件默认保存在 /data/jumpserver 下，如果是自定义配置静态文件路径，请根据实际路径进行备份恢复。
    - 如果是跨环境恢复需要确认其数据库数据与静态文件数据来源一致，否则录像等数据会无法关联。
    - 多节点建议采用NFS等共享存储方案，避免单节点静态文件不一致问题。

!!! tip ""
    - 静态文件目录解释：
    ```sh
    ├── core
    │   └── data
    │       ├── celery
    │       ├── certs
    │       ├── logs  # 系统日志
    │       ├── media # 会话录像等
    │       ├── share
    │       ├── static
    │       ├── system
    │       └── version.txt
    ├── db_backup # 备份的数据库文件和配置文件
    ├── koko
    │   └── data
    │       ├── certs 
    │       ├── keys # 组件注册信息
    │       ├── logs # koko 组件日志，其余组件类似
    │       └── replays
    ├── nginx
    │   └── data
    │       └── logs # Nginx 访问日志（jms_web）
    ├── redis
    │   └── data # 内置 Redis 数据文件
    ├── postgresql
    │   └── data # 内置 PostgreSQL 数据文件
    ```
    
    - 以录像备份为例：
    ```sh
    rsync -avh /data/jumpserver/core/data/media/replay/ /backup/jumpserver/replay_backup/
    # 录像文件夹以日期和会话 uuid 命名
    ```