# Upgrade Notice

!!! warning "There are certain differences between v3 and v2 versions. If upgrading from v2 to v3 [please read this document first](https://kb.fit2cloud.com/?p=06638d69-f109-4333-b5bf-65b17b297ed9){:target="_blank\"}"

!!! warning "Versions v2.20 =< Version <= v2.23 need to upgrade to v2.28 first, then upgrade to v3, otherwise asset connection failures will occur"

!!! warning "Note"
    **v3.6 version requires mandatory DOMAINS trusted domain name configuration for normal service access; otherwise error code 400/403 will prevent page access. DOMAINS configuration is as follows:**

    - If the server is one-click installed and the old version already uses JumpServer with HTTPS enabled, no changes are needed.
    - For scenarios needing to access JumpServer using IP addresses, fill in the DOMAINS field in the config.txt configuration file according to your IP type (public IP or private IP).

    ```
      # Open config.txt configuration file and define DOMAINS field
      DOMAINS=jumpserver.example.com,192.168.1.1
      jmsctl restart
    ```

!!! info "Backup before upgrade or migration operations"

!!! warning "Note"
    - Be sure to backup before updating
    - [For upgrading from V2 to V3, refer to this document](https://kb.fit2cloud.com/?p=06638d69-f109-4333-b5bf-65b17b297ed9){:target="_blank"}
    - [For database migration, refer to this document first](previous_version_upgrade/mariadb-mysql.md){:target="_blank"}
    - [For versions smaller than 1.4.4 before upgrade, follow this document](previous_version_upgrade/1.0.0-1.4.3.md){:target="_blank"}
    - [For versions smaller than 1.4.5 before upgrade, follow this document](previous_version_upgrade/1.4.4.md){:target="_blank"}
    - [For users not using installer deployment, refer to migration instructions to migrate to the latest version](migration.md){:target="_blank"}

!!! tip "Environment Description"
    - Starting from v2.5, MySQL Server >= 5.7 is required
    - Starting from v2.6, Redis Server >= 6.0 is required
    - It is recommended to use external DB Server and Redis Server for convenient expansion and upgrade

!!! tip "External Database Requirements"

    | Component | Version |
    | --- | --- |
    | MySQL | >= 5.7 |
    | MariaDB | >= 10.3 |
    | Redis | >= 6.0 |
