# SSO 认证
!!! note "注：SSO 认证为 JumpServer 企业版功能。"

!!! tip "提示"
    - 使用 SSO 对接第三方系统。

## 1 操作过程
!!! tip ""
    - 修改 JumpServer 配置文件启用 SSO.

    ```sh
    vi /opt/jumpserver/config/config.txt
    ```
    ```vim
    AUTH_SSO=True
    ```

!!! tip ""
    - 修改完成后保存，重启 JumpServer 即可。

## 2 使用方法
!!! tip ""
    - 通过 api 获取任意管理员 token 为其他用户创建免密登录链接。
    
    ```sh
    curl -X POST https://demo.jumpserver.org/api/v1/authentication/auth/ \
      -H 'Content-Type: application/json' \
      -d '{"username": "admin", "password": "xxxxxx"}'
    ```
    ```json
    {"token":"702ec7d22ea24a749140a00a98872e40", ...}
    ```

    === "Token 使用方法"
        ```sh
        curl -X POST https://demo.jumpserver.org/api/v1/authentication/sso/login-url/ \
          -H 'Content-Type: application/json' \
          -H "Authorization: Bearer 702ec7d22ea24a749140a00a98872e40" \
          -d '{"username": "zhangsan", "next": "/luna/"}'
        ```

    === "Private Token 使用方法"
        ```sh
        curl -X POST https://demo.jumpserver.org/api/v1/authentication/sso/login-url/ \
          -H 'Content-Type: application/json' \
          -H "Authorization: Token 937b38011acf499eb474e2fecb424ab3" \
          -d '{"username": "zhangsan", "next": "/luna/"}'
        ```

    ```json
    Respons:
    {
        "login_url": "http://demo.jumpserver.org/api/v1/authentication/sso/login/?authkey=779e97cc-cd05-41a7-a3c3-0320896ba309&next=%2Fluna%2F"
    }
    # 直接访问这个链接即可使用用户的身份免密登陆 luna 页面  
    # 用户和要登陆页面设置: {"username": "zhangsan", "next": "/luna/"}  
    # 这里的 zhangsan 是 JumpServer 用户列表里面的用户 username，可以改成其他的用户
    ```
