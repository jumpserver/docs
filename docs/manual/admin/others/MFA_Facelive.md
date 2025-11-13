# MFA Facelive
!!! info "注: 人脸识别为功能为旗舰版功能。"
> 1. 版本：v4.6.0 及以上 </br>
> 2. 旗舰版许可证 5000 个以上的资产 </br>
> 3. 启用 HTTPS 访问

## 1 配置 Faclive
!!! tip ""
    **新增参数**
    ```sh
    vim /opt/jumpserver/config/config.txt
    #config.txt
    USE_XPACK=1
    FACE_RECOGNITION_ENABLED=true
    FACELIVE_ENABLED=1
    ```
    **重启 JumpServer**
    ```sh
    jmsctl restart
    ```

## 2 配置 MFA 人脸识别
!!! tip ""
    - 在用户详细信息页面记录面部信息并启用 MFA。

![image.png](../../../../img/Facelive1.png)

!!! tip ""
    - 退出登录并尝试重新登录，选择人脸验证。
![image.png](../../../../img/Facelive2.png)

!!! tip ""
    - 请在30秒内完成面部验证。
![image.png](../../../../img/Facelive3.png)

## 3 资产连接面部认证与监控
!!! tip ""
    - 在 **控制台 > 访问控制 > 资产连接** 中启用**人脸验证**。操作可以是 **人脸验证** 或 **人脸在线** 。
![image.png](../../../../img/Facelive4.png)

!!! tip ""
    - 连接到资产前需要进行人脸验证。
![image.png](../../../../img/Facelive5.png)

!!! tip ""
    - 如果面部识别未检测到用户，会暂停会话。
    - 暂停会话期间将无法进行对资产的任何操作。
![image.png](../../../../img/Facelive6.png)
    