# Radius 认证
!!! note "注：Radius 认证为 JumpServer 企业版功能。"

!!! tip "提示"
    - 使用 Radius 的用户作为 JumpServer 登录用户。

## 1 操作过程
!!! tip ""
    - 修改 JumpServer 配置文件启用 Radius 认证

    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim
    AUTH_RADIUS=True
    RADIUS_SERVER=127.0.0.1
    RADIUS_PORT=1812
    RADIUS_SECRET=radius_secret
    ```
!!! tip ""
    - 修改完成后保存，重启 JumpServer 即可。

## 2 参数说明
!!! tip ""
    - Radius 参数说明如下：

    | name            | explain                                                    |
    | --------------- | ---------------------------------------------------------- |
    | `RADIUS_SERVER` | Radius 服务器的IP地址                                       |
    | `RADIUS_PORT`   | Radius 服务器的端口                                         |
    | `RADIUS_SECRET` | Radius 服务器的预共享秘钥                                   |
    | `OTP_IN_RADIUS` | 使用动态密码认证，可以配合 ldap 使用，注意需要关闭 radius 认证 |

!!! tip ""
    - `freeradius` 的 `SECRET` 在 clients.conf 里面。
    - 思科的 `SECRET` 可以从 web 页面的 `RADIUS Authentication Settings` 里面的 `Shared Secret` 获取。
    - 华为的 `SECRET` 可以从 web 页面的 `Authentication Options` 里面的 `Shared Secret` 获取。
    - 其他厂商的请自行咨询相关厂商工作人员。

!!! tip ""
    - 例如:

    ```vim
    AUTH_RADIUS=True
    RADIUS_SERVER=47.98.186.18
    RADIUS_PORT=1812
    RADIUS_SECRET=testing123
    ```
    
    - 动态密码认证:

    ```vim
    AUTH_RADIUS=True
    RADIUS_SERVER=47.98.186.18
    RADIUS_PORT=1812
    RADIUS_SECRET=testing123
    OTP_IN_RADIUS=True
    ```
