# MFA Face Recognition
!!! info "Note: Face recognition is a flagship edition feature."
> 1. Version: v4.6.0 and above </br>
> 2. Flagship edition license with 5000+ assets </br>
> 3. HTTPS access enabled

## 1 Configure Face Recognition
!!! tip ""
    **Add new parameters**
    ```sh
    vim /opt/jumpserver/config/config.txt
    #config.txt
    USE_XPACK=1
    FACE_RECOGNITION_ENABLED=true
    FACELIVE_ENABLED=1
    ```
    **Restart JumpServer**
    ```sh
    jmsctl restart
    ```

## 2 Configure MFA Face Recognition
!!! tip ""
    - Record facial information on the user detail page and enable MFA.

![image.png](../../../../img/Facelive1.png)

!!! tip ""
    - Log out and try logging in again, select face verification.
![image.png](../../../../img/Facelive2.png)

!!! tip ""
    - Complete facial verification within 30 seconds.
![image.png](../../../../img/Facelive3.png)

## 3 Asset connection face recognition and monitoring
!!! tip ""
    - Enable **Face Verification** in **Console > Access Control > Asset Connection**. The operation can be **Face Verification** or **Face Online**.
![image.png](../../../../img/Facelive4.png)

!!! tip ""
    - Face verification is required before connecting to an asset.
![image.png](../../../../img/Facelive5.png)

!!! tip ""
    - If facial recognition does not detect the user, the session will be paused.
    - During the paused session, no operations on the asset can be performed.
![image.png](../../../../img/Facelive6.png)
