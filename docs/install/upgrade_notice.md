# 升级须知



!!! warning "v3 版本与 v2 版本存在一定的差异，如需 v2 版本升级至 v3 版本 [请先阅读此文档](https://kb.fit2cloud.com/?p=06638d69-f109-4333-b5bf-65b17b297ed9){:target="_blank"}"

!!! info "在进行升级或者迁移操作前，请先做好备份工作"

!!! warning ""
    - [数据库迁移请先参考此文档](old_version_upgrade/mariadb-mysql.md){:target="_blank"}
    - [升级前版本小于 1.4.4 请先按照此文档操作](old_version_upgrade/1.0.0-1.4.3.md){:target="_blank"}
    - [升级前版本小于 1.4.5 请先按照此文档操作](old_version_upgrade/1.4.4.md){:target="_blank"}
    - [未使用 installer 部署的用户请参考迁移说明迁移到最新版本](migration.md){:target="_blank"}

!!! tip "环境说明"
    - 从 v2.5 版本开始，要求 MySQL Server >= 5.7
    - 从 v2.6 版本开始，要求 Redis Server >= 6.0
    - 推荐使用外置 DB Server 和 Redis Server，方便日后扩展升级

!!! tip "外置数据库要求"
| 名称     | 版本   |
| :------ | :------ |
| MySQL   | >= 5.7  |
| MariaDB | >= 10.2 |    
| Redis   | >= 6.0  |
