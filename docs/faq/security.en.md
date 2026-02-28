# Security Recommendations

## 1 Basic Security Requirements
!!! tip ""
    - JumpServer needs to open at least ports 80, 443, and 2222 to the outside.
    - The operating system of the server where JumpServer is located should be upgraded to the latest version.
    - The software that JumpServer depends on should be upgraded to the latest version.
    - Servers, databases, Redis and other dependent components should not use weak password credentials. 
    - It is not recommended to disable Firewalld and SELinux.
    - Only open necessary ports. If necessary, access JumpServer through VPN or SSL VPN.
    - If you must open to the external network, you should deploy a Web Application Firewall for security filtering.
    - Deploy SSL certificates and access JumpServer through HTTPS protocol.
    - JumpServer should set strong password rules in security settings and prohibit users from using weak passwords.
    - Should enable JumpServer MFA authentication to prevent security issues caused by password leaks.

!!! warning "Note"
    - If JumpServer security issues are discovered, please report to us at ibuler@fit2cloud.com

## 2 Security Configuration Recommendations
!!! tip ""
    - [Linux Common High-Risk Commands Summary](https://kb.fit2cloud.com/?p=173){:target="_blank"}
    - [Limit a Specific Asset to Only Allow Login to JumpServer from Certain IPs](https://kb.fit2cloud.com/?p=199){:target="_blank"}
    - [Use Your Own SSL Certificate to Access JumpServer](https://kb.fit2cloud.com/?p=152){:target="_blank"}
    - [Enhance User Login Security in JumpServer](https://kb.fit2cloud.com/?p=71){:target="_blank"}
    - [User Account Switching on JumpServer Login](https://kb.fit2cloud.com/?p=65){:target="_blank"}
    - [JumpServer High-Risk Command Restrictions](https://kb.fit2cloud.com/?p=63){:target="_blank"}
    - [Limit Source IP Login to JumpServer Bastion Host](https://kb.fit2cloud.com/?p=43){:target="_blank"}
    - [JumpServer Commonly Used MFA Tools](https://kb.fit2cloud.com/?p=6){:target="_blank"}
    - [Set JumpServer Session Expiration Time](https://kb.fit2cloud.com/?p=5){:target="_blank"}
