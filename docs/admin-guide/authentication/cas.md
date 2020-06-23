# CAS 认证

!!! info "使用 CAS 的用户作为 JumpServer 登录用户"
    修改 JumpServer 配置文件启用 CAS 认证
    ```sh
    vi /opt/jumpserver/config.yml
    ```
    ```yaml
    AUTH_CAS: True
    CAS_SERVER_URL: https://account.jumpserver.org/cas/
    CAS_ROOT_PROXIED_AS: https://demo.jumpserver.org:8443
    CAS_LOGOUT_COMPLETELY: False
    CAS_VERSION: 3
    ```

!!! question "设置参数说明"
    `AUTH_CAS`: Whether to open CAS authentication.  

    `CAS_SERVER_URL`: This is the only setting you must explicitly define. Set it to the base URL of your CAS source (e.g. https://account.example.com/cas/).  

    `CAS_ROOT_PROXIED_AS`: Useful if behind a proxy server. If host is listening on http://foo.bar:8080 but request is https://foo.bar:8443. Add CAS_ROOT_PROXIED_AS = https://foo.bar:8443 to your settings.  

    `CAS_LOGOUT_COMPLETELY`: If False, logging out of the application won’t log the user out of CAS as well.  

    `CAS_VERSION`: The CAS protocol version to use.

    !!! warning "`CAS_VERSION` 可选 `1`、`2`、`3`、`CAS_2_SAML_1_0`"
