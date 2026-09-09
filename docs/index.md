# 产品介绍

??? warning "[重要通知丨JumpServer 漏洞通知及修复方案（JS-2026.09.09）]"

    2026 年 8 月，JumpServer 开源项目组收到安全研究人员提交的漏洞报告。经验证，此次发现的漏洞包括：

    ■ **JumpServer sql 查询过滤导致 access key 泄露漏洞**。漏洞详情：[GHSA-6rp5-ff2m-qfrm](https://github.com/jumpserver/jumpserver/security/advisories/GHSA-6rp5-ff2m-qfrm)

    **漏洞利用条件：**

    任意已登录的普通用户只需在API请求中附加特定参数，便能越权获取管理员的Access Key。
    **受影响版本：**

    <br>JumpServer V3 版本：>= 3.7.0 且 <v3.10.23 LTS
    <br>JumpServer V4 版本：>= 4.0.0 且 <v4.10.19 LTS
    **安全版本：**

    <br>JumpServer V3 版本：>= v3.10.23 LTS
    <br>JumpServer V4 版本：>= v4.10.19 LTS

    **修复方案：**

    将JumpServer堡垒机（含社区版和企业版）升级至安全版本。

    **临时修复方案：**

    在 nginx 配置文件中禁用以下相关过滤参数：

    1. 如果HTTPS已启用，可以通过修改/opt/jumpserver/config/nginx/lb_http_server.conf配置文件完成；

    2.  如果HTTPS没有启用，则需要修改jms_web容器中的/etc/nginx/conf.d/http_server.conf配置文件，完成后执行容器commit保存变更。更新完成后，重启jms_web容器。

    ```
    location / {
        if ($args ~* "(^|&)(_|%5f)(r|%72)(e|%65)(l|%6c)=") {        
            return 400;    
        }    
        .....
    }
    ```
    修复后可通过以下命令进行验证：
    ```
    curl -sk -o /dev/null -w '%{http_code}\n' 'http://<地址>/api/v1/users/users/?_rel=not'    # 期望 400
    curl -sk -o /dev/null -w '%{http_code}\n' 'http://<地址>/api/v1/users/users/?%5Frel=not'  # 期望 400
    curl -sk -o /dev/null -w '%{http_code}\n' 'http://<地址>/api/v1/users/users/'             # 期望 401/403
    ```


!!! tip "[信创合规、开箱即用、全栈优化丨飞致云联合宏时数据发布 Zabbix 信创一体机！](https://fit2cloud.com/zabbix/index.html)"

## 1 JumpServer 是什么？
!!! tip ""
    JumpServer 是广受欢迎的开源堡垒机，是符合 4A 规范的专业运维安全审计系统。JumpServer 帮助企业以更安全的方式管控和登录所有类型的资产，实现事前授权、事中监察、事后审计，满足等保合规要求。

![index_02](https://www.jumpserver.com/images/jumpserver-arch-light.png)

!!! tip ""
    JumpServer 堡垒机支持的资产类型包括：

    - SSH  (Linux / Unix / 网络设备 等)
    - Windows (Web 方式连接 / 原生 RDP 连接)
    - 数据库 (MySQL / MariaDB / Oracle / SQLServer / PostgreSQL / ClickHouse 等)
    - NoSQL (Redis / MongoDB 等)
    - GPT (ChatGPT 等)
    - 云服务 (Kubernetes / VMware vSphere 等)
    - Web 站点 (各类系统的 Web 管理后台)
    - 应用 (通过 Remote App 连接各类应用)

!!! tip "文档指引"

    [**产品官网**](https://jumpserver.org/) &emsp;&emsp;&emsp;&emsp;&emsp;  [**安装部署**](installation/setup_linux_standalone/requirements/) &emsp;&emsp;&emsp;&emsp;&emsp;  [**在线体验**](https://demo.jumpserver.org/ ) &emsp;&emsp;&emsp;&emsp;&emsp;  [**企业版试用**](https://jinshuju.net/f/kyOYpi) &emsp;&emsp;&emsp;&emsp;&emsp;  [**社区论坛**](https://bbs.fit2cloud.com/c/js/5) &emsp;&emsp;&emsp;&emsp;&emsp; [**视频教学**](https://www.bilibili.com/video/BV11AsDegEo8/) &emsp;&emsp;&emsp;&emsp;&emsp; [**技术白皮书**](https://whitepaper.jumpserver.org/)

## 2 产品特色
!!! tip ""
    JumpServer 的产品特色包括：

    - 开源：零门槛，线上快速获取和安装；
    - 分布式：轻松支持大规模并发访问；
    - 无插件：仅需浏览器，极致的 Web Terminal 使用体验；
    - 多云支持：一套系统，同时管理不同云上面的资产；
    - 云端存储：审计录像云端存储，永不丢失；
    - 多租户：一套系统，多个子公司和部门同时使用；
    - 多应用支持：数据库，Windows 远程应用，Kubernetes。

## 3 页面展示
![!界面展示](img/dashboard.png)

## 4 应用商店
!!! tip ""
    JumpServer 的远程应用功能，社区版默认支持 Chrome、DBeaver 应用，企业版支持更丰富的远程应用，可点击 [应用商店](https://apps.fit2cloud.com/jumpserver) 来获取更多远程应用。

## 5 安全说明
!!! tip ""
    - JumpServer 是一款安全产品，请遵循 [基本安全建议](faq/security.md) 进行安装部署
    - 如果你发现安全问题，可以直接联系我们：support@fit2cloud.com

## 6 商业产品
!!! tip ""
    - [JumpServer 企业版](https://jumpserver.org/enterprise.html){:target="_blank"}
    - [JumpServer 一体机](https://jumpserver.org/hardware.html){:target="_blank"}

## 7 了解更多
!!! tip ""
    - [如何向团队介绍 JumpServer？](https://www.fit2cloud.com/jumpserver/documents/introduce-jumpserver_2026.pdf)
    - [JumpServer 技术白皮书](https://whitepaper.jumpserver.org/){:target="_blank"}
    - [JumpServer 知识库](https://kb.fit2cloud.com/categories/jumpserver){:target="_blank"}
    - [教学视频](https://space.bilibili.com/510493147?spm_id_from=333.337.0.0){:target="_blank"}
