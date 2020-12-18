# Koko 常见问题

!!! info "请先确认下面选项"
    请在 `web` - `系统设置` - `安全设置` 里面允许 `终端注册`  
    Docker 容器部署的 `CORE_HOST` 不可以使用 `http://127.0.0.1:8080`

### 1. koko 启动异常

!!! question "启动异常"
    - POST failed, get code: 403, {"detail":"身份认证信息未提供。"}  
    - POST failed, get code: 400, {"name":["名称重复"]}  
    - Connect Server error or access key is incalid, remove data/keys/.access_key run agent

    在 web - 会话管理 - 终端管理 里面删除 koko 的注册 ( 在线显示红色的[koko]xxx )  

    ```sh
    rm -f /opt/jumpserver/koko/data/keys/.access_key
    docker restart jms_koko
    ```

### 2. SSH 登陆异常

!!! question "设置了公钥却无法登录"
    可能是设置了其它的登录方式，而没有使用本地数据库认证方式，假如 使用LDAP登录，也设置了公钥登录，当 LDAP 中删除了用户，或设置了禁用，无法完成LDAP认证，但是用户却使用公钥登录了，这个问题就比较棘手，所以除了数据库认证，都关闭了设置公钥和使用公钥登录
