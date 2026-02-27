# Product Introduction

??? warning "Important Notice | JumpServer Vulnerability Notification and Fix 2025-10-30 (CVE-2025-62712|CVE-2025-62795)"
    **In October 2025, users reported security vulnerabilities in JumpServer open source bastion machine and reported them to the JumpServer open source project team.**

    **Vulnerability Information：** 
    <br>1. [JumpServer token list for connected sessions has privilege escalation risk, CVE number CVE-2025-62712](https://nvd.nist.gov/vuln/detail/CVE-2025-62712)
    <br>2. [JumpServer LDAP configuration has unauthorized testing risk, CVE number CVE-2025-62795](https://nvd.nist.gov/vuln/detail/CVE-2025-62795)
    
    **Affected versions:** <br> JumpServer V3: <=v3.10.20 LTS
    <br> JumpServer V4: <=v4.10.11 LTS

    **Secure versions:** <br> JumpServer V3: >=v3.10.21 LTS
    <br> JumpServer V4: >=v4.10.12 LTS

    **Fix solutions:**
    <br>**Permanent fix:** Upgrade JumpServer software to the above secure versions.
    <br>**Temporary fix:** Restrict access to relevant API endpoints with minimal impact to main JumpServer functions. **Nginx configuration example:**
    
    ```nginx   
    # CVE-2025-62712
    location /api/v1/authentication/super-connection-token/  {
        return 200 '';
    }
    location /api/v1/resources/super-connection-tokens/  {
        return 200 '';
    }
    
    # CVE-2025-62795, this will disable test and import functions in ldap config
    location /ws/ldap {
        return 200 '';
    }

    ``` 
    **Special thanks to:** <br> Thanks to SolidLab for discovering and timely reporting the above vulnerabilities to the JumpServer open source community.


## 1 What is JumpServer?
!!! tip ""
    JumpServer is a popular open source bastion machine that is a professional operation and maintenance security audit system conforming to the 4A specification. JumpServer helps enterprises manage and log in to all types of assets in a more secure way, implementing pre-authorization, in-process monitoring, and post-audit to meet compliance requirements.

![index_02](https://www.jumpserver.com/images/jumpserver-arch-light.png)

!!! tip ""
    JumpServer bastion machine supports the following asset types:

    - SSH (Linux / Unix / Network devices, etc.)
    - Windows (Web access / native RDP access)
    - Database (MySQL / MariaDB / Oracle / SQL Server / PostgreSQL / ClickHouse, etc.)
    - NoSQL (Redis / MongoDB, etc.)
    - GPT (ChatGPT, etc.)
    - Cloud services (Kubernetes / VMware vSphere, etc.)
    - Web sites (Web management backends of various systems)
    - Applications (various applications accessed through Remote App)

!!! tip "Documentation Guide"

    [**Official Website**](https://jumpserver.org/) &emsp;&emsp;&emsp;&emsp;&emsp;  [**Installation and Deployment**](installation/setup_linux_standalone/requirements/) &emsp;&emsp;&emsp;&emsp;&emsp;  [**Online Demo**](https://demo.jumpserver.org/ ) &emsp;&emsp;&emsp;&emsp;&emsp;  [**Enterprise Edition Trial**](https://jinshuju.net/f/kyOYpi) &emsp;&emsp;&emsp;&emsp;&emsp;  [**Community Forum**](https://bbs.fit2cloud.com/c/js/5) &emsp;&emsp;&emsp;&emsp;&emsp; [**Video Teaching**](https://www.bilibili.com/video/BV11AsDegEo8/) &emsp;&emsp;&emsp;&emsp;&emsp; [**Technical Whitepaper**](https://whitepaper.jumpserver.org/)

## 2 Product Features
!!! tip ""
    JumpServer product features include:

    - Open source: Zero threshold, quickly obtain and install online
    - Distributed: Easily support large-scale concurrent access
    - Plugin-free: Browser only, ultimate Web Terminal experience
    - Multi-cloud support: One system managing assets across different clouds
    - Cloud storage: Audit recordings stored in cloud, never lost
    - Multi-tenant: One system for multiple subsidiaries and departments
    - Multi-application support: Database, Windows remote applications, Kubernetes

## 3 Page Display
![!Interface Display](img/dashboard.png)

## 4 Application Store
!!! tip ""
    JumpServer's remote application feature supports Chrome and DBeaver applications by default in community edition, and supports richer remote applications in enterprise edition. Click [Application Store](https://apps.fit2cloud.com/jumpserver) to get more remote applications.

## 5 Security Statement
!!! tip ""
    - JumpServer is a security product. Please follow [basic security recommendations](faq/security.md) for installation and deployment.
    - If you discover security issues, please contact us directly: support@fit2cloud.com

## 6 Commercial Products
!!! tip ""
    - [JumpServer Enterprise Edition](https://jumpserver.org/enterprise.html){:target="_blank"}
    - [JumpServer Appliance](https://jumpserver.org/hardware.html){:target="_blank"}

## 7 Learn More
!!! tip ""
    - [How to introduce JumpServer to your team?](https://www.fit2cloud.com/jumpserver/documents/introduce-jumpserver_202511.pdf)
    - [JumpServer Technical Whitepaper](https://whitepaper.jumpserver.org/){:target="_blank"}
    - [JumpServer Knowledge Base](https://kb.fit2cloud.com/categories/jumpserver){:target="_blank"}
    - [Teaching Videos](https://space.bilibili.com/510493147?spm_id_from=333.337.0.0){:target="_blank"}
