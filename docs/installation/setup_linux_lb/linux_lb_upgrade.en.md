# Upgrade Notes

## 1 About Cluster Mode Environment Upgrades
!!! warning "Be sure to backup before upgrading"
    - Close all JumpServer nodes before upgrading.
    - Complete the upgrade operation on any one JumpServer node according to the upgrade documentation.
    - Carefully check the upgrade process of this node to ensure there are no issues.
    - Then upgrade other JumpServer nodes according to the upgrade documentation.

!!! tip ""
    - Download the latest linux/amd64 offline package from the Fei Zhi Yun community [downloads page](https://community.fit2cloud.com/#/products/jumpserver/downloads){:target="_blank"}, and upload it to the /opt directory of the deployment server.

!!! tip ""
    ```sh
    cd /opt
    tar -xf jumpserver-offline-installer-{{ jumpserver.tag }}-amd64.tar.gz
    cd jumpserver-offline-installer-{{ jumpserver.tag }}-amd64
    ```
    ```sh
    # Additional nodes can set SKIP_BACKUP_DB=1 to skip database backup. Do not skip backup for the first upgraded node.
    export SKIP_BACKUP_DB=1
    ./jmsctl.sh upgrade
    ./jmsctl.sh start
    ```
