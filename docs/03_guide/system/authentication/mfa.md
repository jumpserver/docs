# MFA 认证

!!! tip "提示"
    - MFA：多因子认证。

## 1 开启 MFA
!!! tip ""
    - `启用`的情况，在 创建用户 或者 更新用户 时可以指定 启用多因子认证。
    - `强制用户开启`的情况，在 web - 用户管理 - 用户列表 点击用户详情，可强制启用多因子认证。
    - `全局启用`的情况，在 web - 系统设置 - 安全设置 勾选 多因子认证（开启后所有用户都会强制启用 MFA 认证，用户无法手动关闭）

!!! warning "推荐设置"
    - 所有管理员都应该强制启用多因子认证。
    - 在实际生产环境中应该开启全局 MFA 以增加安全性。

### 2. 关闭 MFA
!!! tip ""
    - 正常启用的 MFA 用户可以自行关闭。
    - 强制启用的 MFA 需要管理员关闭。
    - 全局启用 MFA 无法关闭，必须先在 系统设置 - 安全设置 关闭全局 MFA。

### 3. 重置 MFA
!!! tip ""
    - 管理员可以在其他用户详情里面重置该用户的多因子认证，web - 用户列表 点击用户的 名称，即可看到用户详情。

!!! tip ""
    - 如果是管理员忘记了 MFA，可以通过控制台重置。

    ```sh
    docker exec -it jms_core /bin/bash
    cd /opt/jumpserver/apps
    python manage.py shell
    ```
    ```python
    from users.models import User
    u = User.objects.get(username='admin')
    u.mfa_level='0'
    u.otp_secret_key=''
    u.save()
    ```
