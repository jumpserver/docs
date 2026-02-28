# Data Backup and Recovery

## 1 Overview

!!! tip ""
    **JumpServer bastion host data is mainly divided into two parts:**

    - Database data: User data, asset data, account data, operation logs, command records, etc.
    - Static files: Session recordings, images, system logs, configuration files, etc.

## 2 Database Backup and Recovery

!!! warning "Note"
    - This document takes backup and recovery in the same environment as an example. For cross-environment recovery, ensure database version and type are consistent. The **BOOTSTRAP_TOKEN** and **SECRET_KEY** in the configuration file must be the same as the export source!

!!! tip ""
    === "Backup"
        - Execute the following command on any node of the bastion host to backup database information:
          ```bash
          jmsctl backup_db
          ```
        - If MySQL or MariaDB is used as the database, the file name format is jumpserver-v4.10.9-xxxx-xx-xx_xx:xx:xx.sql.
        
    === "Restore"
        - Execute the following command on any node of the bastion host to restore database information:
          ```bash
          jmsctl restore_db /path/to/backup.sql
          ```

## 3 Static File Backup

!!! warning "Note"
    - Static files mainly include session recordings, images, system logs, etc. Static files are saved in /data/jumpserver by default. If static file paths are custom, backup and recovery should be done according to the actual paths.
    - For cross-environment recovery, ensure database data and static file data sources are consistent, otherwise recordings and other data cannot be associated.
    - For multi-node environments, it is recommended to use shared storage solutions such as NFS to avoid inconsistency in static files on single nodes.

!!! tip ""
    - Static file directory structure:
    ```sh
    ├── core
    │   └── data
    │       ├── celery
    │       ├── certs
    │       ├── logs  # System logs
    │       ├── media # Session recordings, etc.
    │       ├── share
    │       ├── static
    │       ├── system
    │       └── version.txt
    ├── db_backup # Backed up database files and configuration files
    ├── koko
    │   └── data
    │       ├── certs 
    │       ├── keys # Component registration information
    │       ├── logs # koko component logs, similar for other components
    │       └── replays
    ├── nginx
    │   └── data
    │       └── logs # Nginx access logs (jms_web)
    ├── redis
    │   └── data
    └── postgresql
        └── data
    ```
