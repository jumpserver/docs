# Product Introduction

??? warning "[Important Notice | JumpServer Vulnerability Notification and Remediation (JS-2026.08.21)]"
    In August 2026, the JumpServer open source project team received vulnerability reports from security researchers. After verification, the following vulnerability was confirmed:

    ■ **Access key disclosure caused by SQL query filtering in JumpServer (CVE-2026-xxxxx)**. Details: [GHSA-6rp5-ff2m-qfrm](https://github.com/jumpserver/jumpserver/security/advisories/GHSA-6rp5-ff2m-qfrm)

    **Affected versions:**

    <br>JumpServer V3: >= 3.7.0, < 3.10.23
    <br>JumpServer V4: >= 4.0.0, < 4.10.19

    **Fixed versions:**

    <br>JumpServer V3: >= v3.10.23
    <br>JumpServer V4: >= v4.10.19

    **Exploitation conditions:**

    An attacker with ordinary user privileges can use this API to obtain the access keys of other users, which is equivalent to having the permissions of other users, including admin.

    **Remediation:**

    Users are advised to upgrade to a secure version as soon as possible. In the secure versions, JumpServer has fixed the above issues.

    **Temporary workaround:**

    Disable this filtering parameter in the nginx configuration file:

    1. If HTTPS is enabled, modify `/opt/jumpserver/config/nginx/lb_http_server.conf`;

    2. If HTTPS is not enabled, modify `/etc/nginx/conf.d/http_server.conf` inside the jms_web container, and commit the changes after completion.

    ```
    location / {
        if ($arg__rel != "") {
            return 400;
        }
        .....
    }
    ```



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
