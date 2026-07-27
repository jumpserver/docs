# Product Introduction

??? warning "[Important Notice | JumpServer Vulnerability Notification and Remediation (JS-2026.7.29)]"
    In July 2026, the JumpServer open source project team received vulnerability reports from security researchers. After verification, the following vulnerabilities were confirmed:

    ■ **Vulnerability in the fastjson dependency of the JumpServer Chen component (CVE-2026-16723)**. Details: [Security Advisory: Remote Code Execution in fastjson 1.2.68-1.2.83](https://github.com/alibaba/fastjson2/wiki/Security-Advisory:-Remote-Code-Execution-in-fastjson-1.2.68%E2%80%931.2.83)

    ■ **Command injection in JumpServer Ansible Gateway SSH ProxyCommand (CVE-2026-XXXXX)**. Details: [GHSA-q9wr-gv6g-5gm6](https://github.com/jumpserver/jumpserver/security/advisories/GHSA-q9wr-gv6g-5gm6)

    ■ **Unsafe Lookup plugin invocation during JumpServer Ansible automation template rendering (CVE-2026-XXXXX)**. Details: [GHSA-gr5x-5c4h-867g](https://github.com/jumpserver/jumpserver/security/advisories/GHSA-gr5x-5c4h-867g)

    ■ **SFTP path traversal in JumpServer KoKo Web Terminal (CVE-2026-54336)**. Details: [GHSA-x6rg-36j6-76vr](https://github.com/jumpserver/jumpserver/security/advisories/GHSA-x6rg-36j6-76vr)

    ■ **Remote command execution through Jinja template injection during JumpServer Applet Host deployment (CVE-2026-44845)**. Details: [GHSA-22h6-pcgh-9v7q](https://github.com/jumpserver/jumpserver/security/advisories/GHSA-22h6-pcgh-9v7q)

    ■ **Privilege overwrite in JumpServer organization invitation logic (CVE-2026-44846)**. Details: [GHSA-j836-99w5-523r](https://github.com/jumpserver/jumpserver/security/advisories/GHSA-j836-99w5-523r)

    **Affected versions:**

    <br>JumpServer V3: earlier than v3.10.22 LTS
    <br>JumpServer V4: earlier than v4.10.17 LTS

    **Secure versions:**

    <br>JumpServer V3: v3.10.22 LTS or later
    <br>JumpServer V4: v4.10.17 LTS or later

    If an immediate upgrade is not possible:

    **■** Restrict administrative access to high-risk functionality such as Ansible automation, SSH gateways, and Applet Hosts, granting the relevant permissions only to trusted administrators;

    **■** Review existing SSH gateway configurations, automation task templates, Applet Host configurations, and organization role change records for suspicious content;

    **■** Limit the use of accounts that have user invitation permissions.



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
