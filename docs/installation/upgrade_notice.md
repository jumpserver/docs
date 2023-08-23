# 升级须知
!!! warning "v3 版本与 v2 版本存在一定的差异，如需 v2 版本升级至 v3 版本 [请先阅读此文档](https://kb.fit2cloud.com/?p=06638d69-f109-4333-b5bf-65b17b297ed9){:target="_blank"}"

!!! warning "注意"
    **v3.6 版本为了安全，要求强制填写 DOMAINS 可信任域名才能正常访问服务，否则会提示错误码 400/403 导致无法无法访问页面，DOMAINS 配置如下。**

    - 如果服务器是一键安装并且旧版本就已经使用 JumpServer 开启了 HTTPS，则不需要进行任何更改。
    - 需要使用 IP 地址来访问 JumpServer 的场景，可以根据自己的 IP 类型来填写 config.txt 配置文件中 DOMAINS 字段为公网 IP 还是内网 IP。

    ```
      # 打开config.txt 配置文件，定义 DOMAINS 字段
      vim /opt/jumpserver/config/config.txt 

      # 可信任 DOMAINS 定义,
      # 定义可信任的访问 IP, 请根据实际情况修改, 如果是公网 IP 请改成对应的公网 IP。
      # DOMAINS="demo.jumpserver.org"    # 使用域名访问
      # DOMAINS="172.17.200.191"         # 使用 IP 访问
      # DOMAINS="demo.jumpserver.org,172.17.200.191"    # 使用 IP 和 域名一起访问
      DOMAINS=

      # 重启 JumpServer 服务生效
      jmsctl restart
    ```

!!! info "在进行升级或者迁移操作前，请先做好备份工作"

!!! warning "注意"
    - 更新前请一定要做好备份工作
    - [V2版本升级至V3版本请参考此文档](https://kb.fit2cloud.com/?p=06638d69-f109-4333-b5bf-65b17b297ed9){:target="_blank"}
    - [数据库迁移请先参考此文档](previous_version_upgrade/mariadb-mysql.md){:target="_blank"}
    - [升级前版本小于 1.4.4 请先按照此文档操作](previous_version_upgrade/1.0.0-1.4.3.md){:target="_blank"}
    - [升级前版本小于 1.4.5 请先按照此文档操作](previous_version_upgrade/1.4.4.md){:target="_blank"}
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
