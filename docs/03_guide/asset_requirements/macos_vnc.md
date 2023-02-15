# macOS VNC 资产要求

## 1 屏幕共享
!!! tip ""
    - 在 Mac 端配置 `系统偏好设置`-`共享`-`屏幕共享` 功能开启
    - 默认的端口为 `5900`

## 2 RealVNC
!!! tip ""
    - 如果不使用自带的 vnc，可以单独安装 `RealVNC Server`  
    - 正常安装好 `RealVNC Server`，注意安装过程中允许放行防火墙  
    - 在 `RealVNC Server`-`Options`-`Security` 选项里面设置 `Encryption` 为 `Prefer off`  
    - 在 `RealVNC Server`-`Options`-`Security` 选项里面选择 `Authentication` 为 `VNC password`  
    - 点击保存，然后会提示输入 vnc 密码，这个密码就是用来连接 vnc server

!!! tip ""
    - 默认的端口是 `5900` 可以在 vnc server 主页上查看，用户名为空

!!! warning "注意"
    - RealVNC 不支持使用系统自带的身份认证，只能使用 `vnc password` 进行连接
