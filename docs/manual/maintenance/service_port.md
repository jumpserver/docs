## 1 服务端口说明

JumpServer 服务涉及到的端口分为三个部分：

- JumpServer 服务器端口；
- 数据库服务器端口；（当 PostgreSQL 与 Redis 为内置时，该模块取消）
- 被纳管的资产端口；

### 1.1 JumpServer 服务器端口

JumpServer 部署成功后，需要开放的端口如下：

| 端口 | 作用 | 说明 | 是否必须开通 |
| :--- | :--- | :--- | :--- |
| 80、443 | Web 端访问，http、https 服务端口 | http、https 服务端口 | 需要 |
| 2222 | SSH（堡垒机用户） | koko 服务组件默认端口，如果启用 SSH Client 方式访问堡垒机及登录资产，则需要开启 | 按需 |
| 3389 | Windows 资产的 RDP 方式连接端口 | Razor 服务组件默认端口，如果需要 RDP 方式访问 Windows 资产，则需要开启 | 按需 |
| 33061、33062、54320、63790、14330、15210 | Magnus 服务端口 | Magnus 服务组件默认端口，如果启用 DB 组件，则需要开启 | 按需 |

### 1.2 数据库服务器端口

如 JumpServer 与数据库服务解耦，则数据库节点需要开放的端口如下：

| 端口 | 作用 | 说明 | 需开放与否 |
| :--- | :--- | :--- | :--- |
| 3306 | 数据库服务端口（MySQL） | MySQL 服务使用，存放 JumpServer 服务数据 | 是 |
| 5432 | 数据库服务端口（PostgreSQL） | PostgreSQL 服务使用，存放 JumpServer 服务数据 | 是 |
| 6379 | Redis 服务端口 | Redis 服务使用，存放 JumpServer 缓存数据 | 是 |

### 1.3 资产端口

以下表格中的协议开放针对于 JumpServer 中纳管的资产，即需要开通 JumpServer 服务对该资产的访问端口。开放端口的操作在资产上进行。

| 协议类型 | 对应端口 | 作用 | 说明 |
| :--- | :--- | :--- | :--- |
| SSH 协议 | 默认端口为 22 | JumpServer 通过 SSH 协议连接资产时使用 | 根据资产实际使用 SSH 协议端口做规则放行 |
| RDP 协议 | 默认端口为 3389 | JumpServer 通过 RDP 协议连接资产时使用 | 根据资产实际使用 RDP 协议端口做规则放行 |
| VNC 协议 | 默认端口为 5900 | JumpServer 通过 VNC 协议连接资产时使用 | 根据资产实际使用 VNC 协议端口做规则放行 |
| Telnet 协议 | 默认端口为 23 | JumpServer 通过 telnet 协议连接资产时使用 | 根据资产实际使用 Telnet 协议端口做规则放行 |
| 其他协议 | 类似于 MySQL，默认为 3306；<br>类似于 HTTPS，默认为 443 | JumpServer 通过对应的协议连接资产时使用 | 根据资产实际使用的协议端口做规则放行 |

## 2 防火墙配置说明

在生产环境部署时，如有防火墙以及网络限制应提前开放 JumpServer 相应的访问端口。

当 JumpServer 环境运行中需要添加 JumpServer 节点服务器防火墙策略以及修改机器网络配置等，需要重启 docker 服务以及 JumpServer 服务。操作步骤如下：
1. 修改防火墙策略或修改机器网络配置；
2. 重启 docker 服务；
3. 重启 JumpServer 服务。

 ```bash
 # 修改网络相关配置（根据实际需求执行）
 # 重启 docker 服务
 systemctl restart docker
 # 重启 JumpServer 服务
 jmsctl restart
 ```