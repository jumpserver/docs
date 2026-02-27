# Quick Start
## 1 Install JumpServer
!!! tip ""
    - Supports mainstream Linux distributions (based on Debian / RedHat, including domestic operating systems)
    - Refer to [Linux standalone installation and deployment guide](installation/setup_linux_standalone/offline_install.md) for quick JumpServer deployment

!!! info "After successful installation, access and log in to JumpServer via browser"
    ```sh
    Address: http://<JumpServer server IP>:<service port>
    Username: admin
    Password: ChangeMe
    ```

## 2 Asset Management
### 2.1 Preparation
!!! tip ""
    - Prepare two test assets and one database to verify functionality.

!!! tip ""

    | IP Address | Hostname | Port | Operating System | Admin User | Password |
    | ---------- | -------- | ---- | ---------------- | ---------- | -------- |
    | 172.16.80.11 | test_ssh01 | 22 | Centos 7 | root | Test2020.L |
    | 172.16.80.21 | test_rdp01 | 3389 | Windows 10 | administrator | Test2020.W |
    | 172.16.80.31 | test_mysql01 | 3306 | MySQL 5 | root | Test2020.M |

!!! warning "Note"
    - Windows assets need [Windows SSH setup](guide/asset_requirements/windows_ssh.md) before executing automation tasks such as `update asset information` and `connectivity testing`; this is not required for logging in to Windows assets.
    - MySQL application requires granting `Core` and `KoKo` remote access permissions [MySQL requirements](guide/asset_requirements/mysql.md)

### 2.2 Edit Asset Tree
!!! tip ""
    - Click `Asset Management` - `Asset List` on the left side of the page. Right-click on the root node `Default` to create three nodes: `SSH Server`, `RDP Server`, and `Database`.
!!! tip ""
    - Asset tree example:

    ```
    Default
    ├─ SSH Server
    └─ RDP Server
    └─ DB Server
    ```

!!! warning "Note"
    - The root node `Default` cannot be renamed. Right-click on nodes to `add`, `delete`, and `rename` nodes, and perform asset-related operations.

### 2.3 Create Assets
!!! tip ""
    - Click `Asset Management` - `Asset List` - `Hosts` - `Create` to create a Linux server, and during asset creation, create a privileged user with the `admin user` and `password` from the table above.
    - The creation process for Windows assets is the same.

!!! tip ""
    - Example of creating a Linux asset:

!!! tip ""

    | Name | IP/Hostname | Asset Platform | Node | Protocol Group | Account List |
    | ---- | ----------- | --------------- | ---- | -------------- | ------------ |
    | test_ssh01 | 172.16.80.11 | Linux | /Default/SSH Server | ssh 22 | Add |

!!! tip ""
    - Example of adding login asset user:

!!! tip ""

    | Name | Username | Privileged User | Cipher Type | Password |
    | ---- | -------- | --------------- | ----------- | -------- |
    | 172.16.80.11_root | root | Yes | Password | Test2020.L |

!!! warning "Note"
    - `Name` must be unique. Either `password` or `key` is required; some assets may not allow password authentication and can use key authentication instead.
    - `Privileged user` only supports `SSH` protocol, used for asset `connectivity testing`, `user push`, `batch password change` and other automation tasks.
    - If assets cannot connect normally, verify the privileged user's `username` and `password` are correct and the `privileged user` can SSH from `JumpServer` host to the asset host.

### 2.4 Create Database Application
!!! tip ""
    - Click `Asset Management` - `Asset List` - `Create` - `Database` and select `MySQL Database`.

!!! tip ""
    - Example of creating a MySQL database application:

!!! tip ""

    | Name | IP/Hostname | Node | Username | Database | Account List |
    | ---- | ----------- | ---- | -------- | -------- | ------------ |
    | test_mysql01 | 172.16.80.31 | /Default/DB Server | test | mysql:3306 | Add |

!!! tip ""
    - Example of adding database login user:

!!! tip ""

    | Name | Username | Password | Cipher Type | Password |
    | ---- | -------- | -------- | ----------- | -------- |
    | 172.16.80.23_root | root | root | Password | Test2020.M |

!!! warning "Note"
    - Name, hostname, and database are required fields.

## 3 Create Authorization Rules
!!! tip ""
    - Click `Permission Management` - `Asset Authorization` - `Create` to create an authorization.
    - The authorization process for Windows assets and MySQL databases is the same as below.

!!! tip ""
    - Example of creating a login authorization rule (e.g., Linux asset):

!!! tip ""

    | Name | User | User Group | Asset | Node | Account | Action |
    | ---- | ---- | ---------- | ----- | ---- | ------- | ------ |
    | admin_ssh01 | Administrator(admin) | - | test_ssh01(172.16.80.11) | - | All accounts | ✓ All |

!!! warning "Note"
    - `Name`: The authorization name, must be unique.
    - `User (Group)` and `Asset (Node)` have a one-to-one relationship, so when you have different asset types like `Linux` and `Windows`, you should create separate `authorization rules` for each.

## 4 User Login
!!! tip ""
    - Click `Web Terminal` in the top-right corner to connect to assets.

!!! warning "Note"
    - Users can only see assets they have been authorized by administrators. If no assets appear after login, please contact your administrator.

## 5 System Settings
!!! tip ""
    - Click `System Settings` in the top-right corner to configure.

### 5.1 Basic Settings
!!! tip ""

    | Item | Default | Description |
    | ---- | ------- | ----------- |
    | Forgotten password URL | | Customize if using external authentication systems like LDAP, OpenID |

### 5.2 Email Settings
!!! tip ""
    - We support integrating email configuration through `SMTP` or `EXCHANGE`.

=== "SMTP"
    !!! tip ""


## 6 Common Feature Operations
!!! tip ""
    - **[Upload and download via SFTP][Upload and download via SFTP]**
    - **[Manage Redis databases][Manage Redis databases]**


[Upload and download via SFTP]: https://kb.fit2cloud.com/?p=115
[Windows Upload and Download]: https://kb.fit2cloud.com/?p=87
[Restrict IP Login]: https://kb.fit2cloud.com/?p=199
[Manage Redis databases]: https://kb.fit2cloud.com/?p=91
[Manage Database Applications]: https://kb.fit2cloud.com/?p=79
