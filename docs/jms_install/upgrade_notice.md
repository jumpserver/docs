# 升级须知
!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致，否则会导致数据库加密数据无法解密"
    - 更新前请一定要做好备份工作
    - [数据库迁移请先参考此文档](old_version_upgrade/mariadb-mysql.md){:target="_blank"}
    - [升级前版本小于 1.4.4 请先按照此文档操作](old_version_upgrade/1.0.0-1.4.3.md){:target="_blank"}
    - [升级前版本小于 1.4.5 请先按照此文档操作](old_version_upgrade/1.4.4.md){:target="_blank"}
    - [未使用 installer 部署的用户请参考迁移说明迁移到最新版本](migration.md){:target="_blank"}

!!! tip "环境说明"
    - 从 v2.5 版本开始，要求 MySQL Server >= 5.7
    - 从 v2.6 版本开始，要求 Redis Server >= 6.0
    - 推荐使用外置 DB Server 和 Redis Server，方便日后扩展升级

!!! tip ""
    - 外置数据库要求：

    | 名称     | 版本 |
    | :------ | :------ |
    | MySQL   | >= 5.7  |
    | MariaDB | >= 10.2 |    
    | Redis   | >= 6.0  |
