# Online Upgrade

!!! warning "If you want to upgrade JumpServer from V3 to V4, you must first upgrade to the latest version of V3; otherwise, the upgrade will fail!"

| OS/Arch       | Architecture | Linux Kernel | Offline Name                                     |
| :------------ | :----------- | :----------- | :----------------------------------------------- |
| linux/amd64   | x86_64       | >= 4.0       | jumpserver-installer-{{ jumpserver.tag }}.tar.gz |

## 1. Upgrade Deployment

=== "Mainland China"
    !!! tip ""
        ```sh
        cd /opt
        wget https://resource.fit2cloud.com/jumpserver/installer/releases/download/{{ jumpserver.tag }}/jumpserver-installer-{{ jumpserver.tag }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.tag }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.tag }}
        ```
=== "Other Regions"
    !!! tip ""
        ```sh
        cd /opt
        wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.tag }}/jumpserver-installer-{{ jumpserver.tag }}.tar.gz
        tar -xf jumpserver-installer-{{ jumpserver.tag }}.tar.gz
        cd jumpserver-installer-{{ jumpserver.tag }}
        ```

!!! tip ""
    ```sh
    ./jmsctl.sh upgrade

    # Start JumpServer service
    ./jmsctl.sh start
    ```
