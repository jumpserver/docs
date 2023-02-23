# CAS 认证
!!! tip "阿里云 IDaaS 对接参考资料"
    - [阿里云新 IDaaS 对接](https://help.aliyun.com/document_detail/409903.html)

!!! tip "提示"
    - 使用 CAS 的用户作为 JumpServer 登录用户。

## 1 操作过程
!!! tip ""
    - 修改 JumpServer 配置文件启用 CAS 认证。

    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim
    AUTH_CAS=True
    CAS_SERVER_URL=https://account.jumpserver.org/cas/
    CAS_ROOT_PROXIED_AS=https://demo.jumpserver.org:8443
    CAS_LOGOUT_COMPLETELY=False
    CAS_VERSION=3
    CAS_USERNAME_ATTRIBUTE=uid
    CAS_APPLY_ATTRIBUTES_TO_USER=Flase
    CAS_CREATE_USER=True
    ```
!!! tip ""
    - 修改完成后保存，重启 JumpServer 即可。

## 2 参数说明
!!! tip ""
    - CAS 参数说明如下：

    | name                           | explain                                                                                                                                                                            |
    | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `AUTH_CAS`                     | Whether to open CAS authentication. |
    | `CAS_SERVER_URL`               | This is the only setting you must explicitly define. Set it to the base URL of your CAS source (e.g. https://account.example.com/cas/). |
    | `CAS_ROOT_PROXIED_AS`          | Useful if behind a proxy server. If host is listening on http://foo.bar:8080 but request is https://foo.bar:8443. Add CAS_ROOT_PROXIED_AS = https://foo.bar:8443 to your settings. |
    | `CAS_LOGOUT_COMPLETELY`        | If False, logging out of the application won’t log the user out of CAS as well. |
    | `CAS_VERSION`                  | The CAS protocol version to use. |
    | `CAS_USERNAME_ATTRIBUTE`       | The CAS user name attribute from response. If set with a value other than uid when CAS_VERSION is not 'CAS_2_SAML_1_0', this will be handled by the CASBackend, in which case if the user lacks that attribute then authentication will fail. Note that the attribute is checked before CAS_RENAME_ATTRIBUTES is applied. |
    | `CAS_APPLY_ATTRIBUTES_TO_USER` | If True any attributes returned by the CAS provider included in the ticket will be applied to the User model returned by authentication. This is useful if your provider is including details about the User which should be reflected in your model. |
    | `CAS_RENAME_ATTRIBUTES`        | 	A dict used to rename the (key of the) attributes that the CAS server may retrun. For example, if CAS_RENAME_ATTRIBUTES = {"casUserUid": "username", "casUser": "name", "casUserEmail", "email"} the ln attribute returned by the cas server will be renamed as last_name. Used with CAS_APPLY_ATTRIBUTES_TO_USER = True, this provides an easy way to fill in Django Users’ info independently from the attributes’ keys returned by the CAS server. |
    | `CAS_CREATE_USER`              | Create a user when the CAS authentication is successful. The default is True. |


!!! warning "注意"
    - `CAS_VERSION` 可选 `1`、`2`、`3`、`CAS_2_SAML_1_0`
