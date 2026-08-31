# Network Port Description

## 1 Network Port List

!!! tip ""
    - JumpServer, as a professional operation and maintenance security audit system conforming to 4A standards, requires opening the following network ports for normal operation. Administrators can open relevant ports on the network and host sides according to the actual deployment scheme of JumpServer components in their environment.

| Port | Function | Description |
| --- | --- | --- |
| 22 | SSH | Installation, upgrade, and management |
| 80 | Web HTTP Service | Access JumpServer frontend page via HTTP protocol |
| 443 | Web HTTPS Service | Access JumpServer frontend page via HTTPS protocol |
| 3306 | Database Service | MySQL service |
| 6379 | Database Service | Redis service |
| 3389 | Razor Service Port | RDP Client method to connect to Windows assets |
| 2222 | SSH Client | Use terminal tools like Xshell, PuTTY, MobaXterm to connect to JumpServer via SSH Client |
| 5525 | Magnus Service Port | DB Client method to connect to database assets. The system automatically assigns the corresponding port based on the type of the connected asset |
| 15900 | NEC Service Port | VNC service |

!!! tip ""
    - Starting from v4.10.19, the Magnus port has been unified to **5525**, and it no longer uses different ports for different database types. When connecting to database assets, the system automatically assigns the corresponding connection port based on the asset type (MySQL, MariaDB, PostgreSQL, Redis, Oracle, etc.).
    - The Magnus ports used in older versions (before v4.10.19) are as follows. After upgrading, please adjust the firewall rules as needed:
        - 33061: Magnus MySQL Service Port
        - 33062: Magnus MariaDB Service Port
        - 54320: Magnus PostgreSQL Service Port
        - 63790: Magnus Redis Service Port
        - 15210: Magnus Oracle Service Port

## 2 Firewall Common Commands

!!! tip ""
    - Confirm firewall status is running
    ```bash
    firewall-cmd --state
    ```

!!! tip ""
    - Temporarily open port (rule takes effect immediately, fails on reboot)
    ```bash
    firewall-cmd --zone=public --add-port=80/tcp --permanent
    ```

!!! tip ""
    - Temporarily close port (rule takes effect immediately, fails on reboot)
    ```bash
    firewall-cmd --zone=public --remove-port=80/tcp --permanent
    ```

!!! tip ""
    - Permanently allow port (requires reload to take effect)
    ```bash
    firewall-cmd --zone=public --add-port=80/tcp --permanent
    firewall-cmd --reload
    ```

!!! tip ""
    - Permanently remove port (requires reload to take effect)
    ```bash
    firewall-cmd --zone=public --remove-port=80/tcp --permanent
    firewall-cmd --reload
    ```

!!! tip ""
    - View effective port rules
    ```bash
    firewall-cmd --zone=public --list-all
    ```
