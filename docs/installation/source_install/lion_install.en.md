# Lion Environment Deployment

## 1 Lion Component Overview

!!! tip ""
    [Lion][lion] uses the open-source project [Guacamole][guacamole] from the [Apache][apache] Software Foundation. JumpServer reconstructed Guacamole using Golang and Vue to implement RDP/VNC protocol bastion machine functionality.

### 1.1 Environment Requirements

!!! tip ""
    - Ubuntu 20.04 LTS or later
    - Guacd compiled from source

### 1.2 Build Guacd

!!! tip ""
    ```bash
    cd /opt
    git clone https://github.com/apache/guacamole-server
    cd guacamole-server
    ./configure
    make
    make install
    ```
    - To use systemd management: `./configure --with-systemd-dir=/etc/systemd/system/`

### 1.3 Download Lion

!!! tip ""
    - Download the latest [Release][lion_release] from [Github][lion].

    | Platform | Architecture | Download Link |
    | --- | --- | --- |
    | Linux | amd64 | [lion-v4.10.9-linux-amd64.tar.gz][lion_release] |
    | Windows | amd64 | [lion-v4.10.9-windows-amd64.tar.gz][lion_release] |

### 1.4 Modify Configuration File

!!! tip ""
    ```bash
    cd /opt/lion
    vi config.toml
    ```
    Configure server, database, Redis settings as needed.

### 1.5 Start Guacd

!!! tip ""
    ```bash
    guacd -d
    ```

### 1.6 Start Lion

!!! tip ""
    ```bash
    cd /opt/lion
    ./lion
    ```

[nginx]: http://nginx.org/
[lina]: https://github.com/jumpserver/lina/
[luna]: https://github.com/jumpserver/luna/
[angular_cli]: https://github.com/angular/angular-cli
[core]: https://github.com/jumpserver/jumpserver/
[lion]: https://github.com/jumpserver/lion
[lion_release]: https://github.com/jumpserver/lion/releases
[apache]: https://www.apache.org/
[guacamole]: https://guacamole.apache.org/
