# 更新日志

v4.10.19
------------------------
2026年8月20日

!!! info "新增功能 🌱"
    - feat: 新增 KOTL 组件，实现 JumpServer 自身的可视化运维
    - feat: 统一 Magnus 服务端口，并支持根据连接协议报文自动识别协议
    - feat: 文件传输支持账号策略，完善账号选择、权限校验及异常资产确认机制
    - feat: SMTP 支持使用系统 CA、自定义 CA，或关闭证书校验
    - feat: 新增剪贴板访问控制，主要适用于 RDP、VNC 等图形化连接

!!! summary "功能优化 🚀"
    - perf: 优化表单中多对多资源的选择体验与数据加载性能
    - perf: 优化资源列表顶部的搜索与筛选体验
    - perf: 优化资源批量编辑表单的交互方式及资源批量选择体验
    - perf: 优化工单相关 API 的查询性能，减少 SQL 执行次数
    - perf: 优化 API OPTIONS 响应结构，将 filters、ordering、search 等查询元数据作为独立字段返回
    - perf: 优化用户创建页面，移除名称唯一性校验，支持用户名称重复
    - perf: 升级 Chen SQL 解析器版本
    - perf: 增强 Chen 对 PostgreSQL ALTER COLUMN TYPE、SET DATA TYPE、COLLATE、USING 等字段类型变更语法的解析能力
    - perf: 用户账号过期及授权过期提醒邮件支持配置发送时间参数
    - perf: 增强 Chen 对 Oracle SQL 方言的解析能力
    - perf: 将华为云 OBS SDK 升级至 3.26.2，提升对象存储兼容性
    - perf: 新增 FusionCompute 用户类型配置，支持本地用户、域用户及接口互联用户
    - perf: 工单支持创建工单流，并可配置抄送人
    - perf: 优化自动化任务日志
    - perf: 优化自动化改密任务的推送性能
    - perf: 交换机支持“切换自”账号
    - perf: 支持全局配置个人偏好
    - perf: 增强 Koko rzsz 文件传输的稳定性
    - perf: 重置密码邮件同时展示用户姓名和登录用户名
    - perf: 优化组织删除前的依赖检查，增加账号模板依赖提示
    - perf: 将 Ansible Executor 镜像升级至 Python 3.14，并补充 AWS SDK 依赖
    - perf: 优化 NEC VNC Proxy，支持连接 Mac 资产
    - perf: 优化 Koko Web Terminal 的剪贴板访问控制
    - perf: 优化命令存储，支持 Elasticsearch 9

!!! success "问题修复 🐛"
    - fix: OAuth2 客户端授权回调过程中产生的 Grant 操作不再记录审计日志
    - fix: 修复解绑 UKey 序列号时，因空值处理异常导致报错的问题
    - fix: 修复 Chen SQL 中 – 行注释可能导致后续字段或表达式在格式化后被错误注释的问题
    - fix: 修复 Chen 无法解析 Oracle FETCH FIRST … ROW ONLY、OFFSET … ROW 等分页语法的问题
    - fix: 修复 Chen 解析 Oracle SQL 时可能将其隐式拆分为多条语句的问题，避免未使用分号分隔的 SQL 被错误拆分执行
    - fix: 修复部分 MySQL 数据库因 Public Key Retrieval 限制导致 Chen 无法连接的问题
    - fix: 修复部分禁止匿名查询的 LDAP 服务无法正常连接的问题
    - fix: 修复部分 S3 兼容对象存储配置测试或访问失败的问题
    - fix: 修复部分数据库环境下查询资源活动日志时出现字符排序规则冲突的问题
    - fix: 修复 LDAP 工作线程未正确清理数据库连接而导致连接异常的问题
    - fix: 修复清理审计命令时，空查询集导致时间戳处理异常的问题
    - fix: 修复作业中心授权节点搜索不生效的问题
    - fix: 修复 PostgreSQL Ping 模块数据库参数传递错误的问题
    - fix: 修复 Koko 登录 Ubuntu 资产时切换自账号失败的问题



v4.10.18
------------------------
2026年7月28日

!!! summary "功能优化 🚀"
    - perf: 提升 Chen 对超长 SQL 语句的解析及分片处理能力
    - perf: 优化 Chen 多会话场景下的内存占用
    - perf: 优化 Luna 小助手及抽屉（Drawer）图标的视觉样式
    - perf: 优化站内信的界面样式

!!! success "问题修复 🐛"
    - fix: 修复 KoKo 监听端口配置异常的问题
    - fix: 修复 Docker 隔离模式下文件传输失败的问题
    - fix: 修复将资产授权范围从“所有账号”调整为“指定账号”时报错的问题
    - fix: 修复使用 Redis 进行会话共享时报错的问题
    - fix: 修复 Chen 部分字段类型无法正常展示的问题
    - fix: 修复 Chen 在命令收藏夹中按回车键会意外退出会话的问题
    - fix: 修复Chen 数据导出时分列异常的问题
    - fix: 修复Chen 无法查看名称中包含特殊字符的表数据的问题
    - fix: 修复Chen 部分视图无法正常查看的问题
    - fix: 修复 Lina 点击左上角 Logo 时报错的问题。
    - fix: 修复 Luna 顶部菜单偶发无法响应鼠标点击的问题



v4.10.17
------------------------
2026年7月17日

!!! info "新增功能 🌱"
    - feat: 升级 Django 至 5.2
    - feat: 升级 Python 至 3.14
    - feat: 升级 Vue 至 3.5
    - feat: 支持通过配置 “SECURITY_DISABLE_VIEW_SECRET=true” 禁止导出敏感信息
    - feat: 支持自定义用户单点登录（SSO）认证
    - feat: 支持配置真实 IP 的获取方式
    - feat: 支持用户 UKey 认证【企业版】
    - feat: 支持用户自定义资产收藏节点树

!!! summary "功能优化 🚀"
    - perf: 优化客户端，集成录像播放和录像转码功能
    - perf: 优化 Ansible 任务执行机制，每个任务运行于独立容器中，最大并发数支持 10 个
    - perf: 新增文件上传、下载限流功能，默认限制为 50 次/小时
    - perf: 对用户 Email 信息进行加密存储
    - perf: 支持单独配置管理员密码过期时间
    - perf: 优化 ACL 规则详情中属性过滤规则实例的获取方式，解决请求参数过长的问题
    - perf: 优化历史命令清理机制，支持按天分批删除
    - perf: 站内信支持弹窗提醒
    - perf: 支持自定义可选显示语言
    - perf: 支持通过排除资产类型和类别进行资产查询
    - perf: 优化用户登录 ACL 匹配逻辑，自动排除当前用户作为审批复核人的 ACL 规则
    - perf: 优化 API 文档，不再显示视图类注释信息
    - perf: LDAP 认证服务支持上传证书
    - perf: 通过客户端连接 RDP 会话时，支持开启 RDP 签名（“RDP_SIGN_ENABLED=1”）【企业版】

!!! success "问题修复 🐛"
    - fix: 修复用户登录时重复生成登录日志的问题
    - fix: 修复用户作业执行时未使用默认参数值的问题
    - fix: 修复集成应用每次更新都会重新生成密钥的问题
    - fix: 修复克隆 Playbook 时未校验 Playbook 权限的问题
    - fix: 修复网域相关自动化任务的安全问题
    - fix: 修复远程应用 DBeaver 连接方式的安全问题
    - fix: 修复账号相关自动化功能的安全问题
    - fix: 修复 Ansible Lookup 插件部分功能（如 “file、pipe、env”）未被正确禁用的问题
    - fix: 修复 Luna 页面记住密码显示的问题



v4.10.16
------------------------
2026年3月5日

!!! info "新增功能 🌱"
    - feat: 新增客户端可信 IP 校验能力

!!! summary "功能优化 🚀"
    - perf: 将 Environment 替换为 SandboxedEnvironment，增强 YAML 模板渲染的安全性

!!! success "问题修复 🐛"
    - fix: 修复对外请求时未正确进行证书校验的问题
    - fix: 修复导出资源时因字段顺序不一致导致的逻辑冲突问题



v4.10.15
------------------------
2026年1月22日

!!! info "新增功能 🌱"
    - feat: 新增 API Rate Limiting 限制机制，提升接口调用的稳定性与安全性
    - feat: 工单列表新增快速过滤能力，提升工单查询与处理效率（JumpServer EE）

!!! summary "功能优化 🚀"
    - perf: 升级 Lion 组件的基础镜像 1.5.5-trixie
    - perf: 优化申请资产工单中备注信息丢失的问题，确保信息完整保留（JumpServer EE）
    - perf: 系统工具新增对 IPv6 地址的网络测试支持
    - perf: Windows 资产账号修改密码后，校验密码时支持通过 pyfreerdp 进行验证（JumpServer EE）

!!! success "问题修复 🐛"
    - fix: 修复认证服务未正确进行证书校验的问题
    - fix: 修复 Ansible 通过 paramiko 执行任务时，启用 SSH 隧道失败的问题
    - fix: 修复通过账号模板创建账号时，privileged 权限未正确关联的问题
    - fix: 修复通过账号模板创建账号时，未同步创建对应切换子账号的问题



v4.10.14
------------------------
2025年12月18日

!!! info "新增功能 🌱"
    - feat: JumpServer Client 新增支持 OAuth 2.0 认证方式，提升客户端登录的兼容性
    - feat: 用户操作审计日志 支持导出为 CSV / Excel 文件，便于审计分析与留档
    - feat: 云同步功能新增支持 State Cloud（JumpServer EE）
    - feat: 虚拟应用支持通过本地客户端使用 VNC 协议 进行连接访问（JumpServer EE）

!!! summary "功能优化 🚀"
    - perf: 智能问答功能支持配置用户自定义模型，满足不同场景的智能交互需求
    - perf: Kubernetes 平台协议新增支持命名空间配置，用户连接时仅可访问已授权的命名空间，进一步提升访问控制精度

!!! success "问题修复 🐛"
    - fix: 修复 Razor 组件的内存泄漏问题（JumpServer EE）
    - fix: 修复按风险级别过滤查询命令时返回空结果的问题
    - fix: 修复通过不同 Endpoint 连接会话后，分享会话链接无法复制的问题



v4.10.13
------------------------
2025年11月20日

!!! info "新增功能 🌱"
    - feat: 全新 JumpServer 客户端，体积更小，操作体验更佳（V4）
    - feat: 支持 录像转码功能，可对 Lion、Razor 生成的录像进行转码（video-worker）【企业版】
    - feat: 后端数据库 PostgreSQL 已支持 SSL 加密连接

!!! summary "功能优化 🚀"
    - perf: 所有组件基础镜像已升级至 Debian 13 (trixie)
    - perf: 升级 Docker 至 28.5.1，并升级 Docker Compose 至 v2.40.3
    - perf: 资产 ACL 规则现已在 任务（Job） 中生效
    - perf: 添加账号（基于账号模版）时，支持选择多个模版及资产节点进行 批量创建
    - perf: 资产平台支持一键同步所有协议/端口至资产，支持 覆盖操作
    - perf: 支持批量导入 弱密码列表



v4.10.12
------------------------
2025年10月27日

!!! summary "功能优化 🚀"
    - perf: 优化 LDAP 服务连接测试过程中的密码使用机制和用户权限校验
    - perf: 优化 KoKo 分享会话时的用户查询逻辑，默认最多返回 10 条结果



v4.10.11
------------------------
2025年10月21日

!!! success "问题修复 🐛"
    - fix: 优化获取 SuperConnectionToken 时的权限校验逻辑



v4.10.10
------------------------
2025年10月16日

!!! info "新增功能 🌱"
    - feat: 新增数据库脱敏功能【企业版】 Chen 和 KoKo 支持所有关系型数据库
    - feat: Magnus 仅支持 MySQL 数据库

!!! summary "功能优化 🚀"
    - perf: 优化 Razor 连接资产时的卡顿与高内存占用问题（已升级至 FreeRDP3）【企业版】
    - perf: 快捷命令左侧树结构优化为显示已选资产列表
    - perf: 新增匹配发布机标签名（AppletHostOnly），当发布机无效时不再随机选择其他发布机
    - perf: Luna 页面主题设置可保存至个人偏好中
    - perf: 账号推送接口新增用户组 gid 参数

!!! success "问题修复 🐛"
    - fix: 修复 ACLs 规则在选择全部资产时，全局组织中显示不准确的问题【企业版】



v4.10.9
------------------------
2025年9月24日

!!! summary "功能优化 🚀"
    - perf: Lion 文件管理支持同时上传多个文件

!!! success "问题修复 🐛"
    - fix: 修复 KoKo 内存占用过高的问题



v4.10.8
------------------------
2025年9月18日

!!! info "新增功能 🌱"
    - feat: 添加了全局资源搜索功能
    - feat: 资产授权支持反向账号授权
    - feat: 添加了越南语（Tiếng Việt）语言支持
    - feat: KoKo 支持连接到 Redis 集群
    - feat: KoKo 支持 SSL 连接到 SQL Server
    - feat: 支持配置所有邮件模板
    - feat: 支持在弹窗中显示公告

!!! summary "功能优化 🚀"
    - perf: 改进云同步以在以下情况下避免释放资产【企业版】：
        - 云账号无效
        - 在区域下没有找到资产
        - 区域已从更新任务中移除
    - perf: 改进 KoKo 直连在退出后返回正确的退出代码
    - perf: 支持自动启动 VNC 客户端连接到资产【企业版】
    - perf: 改进 RDP 真彩色（24位）显示

!!! success "问题修复 🐛"
    - fix: 修复了用户过期后访问密钥仍然有效的问题
    - fix: 修复了将用户登录规则更改为审批时的错误【企业版】
    - fix: 修复了存在多个会话标签页时，非活动会话标签页因不自动续期而断开连接的问题
    - fix: 修复了 Chen 复杂 SQL 查询结果导出失败的问题

v4.10.7
------------------------
2025年9月4日

!!! summary "功能优化 🚀"
    - perf: AccessKey 表中密钥字段的加密存储（迁移已完成）

!!! success "问题修复 🐛"
    - fix: 修复了用户 MFA 重置失败的问题

v4.10.6
------------------------
2025年8月29日

!!! success "问题修复 🐛"
    - fix: 解决了升级后所有组件离线的问题
    - fix: 解决了域用户无法登录 Windows 资产的问题
    - fix: 修复了清理会话日志的定时任务错误
    - fix: 修复了 Magnus 执行长 SQL 语句时无响应的问题
    - fix: 修复了 Nec 组件在使用仅密码认证连接 RealVNC 服务器时会卡死的问题

v4.10.5
------------------------
2025年8月22日

!!! info "新增功能 🌱"
    - feat: 添加报告功能以支持可视化数据分析和导出【企业版】
    - feat: 改进命令日志记录和过滤以提高准确性
    - feat: 云同步支持 ProxmoxVE【企业版】
    - feat: 在 KoKo 中添加字符搜索以加快信息查找

!!! summary "功能优化 🚀"
    - perf: 以加密形式存储用户 AccessKey 以提高安全性
    - perf: 当 SAFE_MODE 关闭时允许 OTP 重用以便于使用
    - perf: 当 SAFE_MODE 开启时禁用 Passkey 作为 MFA 以增强安全性

v4.10.4
------------------------
2025年7月16日

!!! summary "功能优化 🚀" 
    
    - perf: 在会话记录中增加了录制文件大小
    - perf: 端点规则现在支持按主机域名匹配
    - perf: 为 Elasticsearch 命令记录增加了模糊搜索支持
    - perf: 优化了下载 FTP 日志文件的操作日志
    - perf: 优化了查看录像的操作日志
    - perf: 改进了用户资产会话详情页面及后端逻辑
    - perf: 增加了工单操作审计【企业版】
    - perf: 增加了对启用或禁用 SQL Server 2008 TLS 加密的支持【企业版】
    - perf: 云同步任务现在支持切换自动更新主机信息【企业版】

v4.10.3
------------------------
2025年7月1日

!!! success "问题修复 🐛"
    - fix: 在为命令存储配置Elasticsearch后，修复了命令记录计数显示为0的问题。
    - fix: 在连接到Kubernetes时，修复“Ctrl + C”组合键正常功能。
    - fix: 在连接到资产时，修复了“记住密码”的功能。
    - fix: 修复了KoKo会话显示WebSocket断开警告的问题。

v4.10.2
------------------------
2025年6月20日

!!! info "新增功能 🌱"
    - feat: 支持用户设置个人语言偏好设置
    - feat: 添加了对Magnus中MongoDB数据库的连接支持【企业版】
    - feat: 支持在成功登录到资产后自动更改账号密码【企业版】
    - feat: 云同步现在支持SmartX云平台【企业版】
    - feat: SSO单点登录现在支持MFA【企业版】
    - feat: Chrome RemoteApp界面现在可以根据当前用户的语言自动切换显示语言
    - feat: 添加了定期清理过期连接令牌和临时令牌的支持
    - feat: 聊天AI支持基于字符会话（SSH、Telnet）上下文的智能回复和命令插入
    - feat: 支持批量删除弱密码集
    - feat: 可通过 CELERY_WORKER_COUNT 配置 Celery Workers 的数量
    - feat: 当启用了安全模式 SAFE_MODE=true 时，Adhoc 中的快捷命令将隐藏账户名称提示

!!! success "问题修复 🐛"
    - fix: 修复远程应用程序发布失败的问题
    - fix: 修复资产类型树嵌套显示异常的问题

v4.10.1
------------------------
2025年5月19日

!!! success "问题修复 🐛"
    - fix: 修复客户端下载失败的问题
    - fix: 修复 Web CLI 连接 Linux 时鼠标滚动的问题
    - fix: 修复社区版水印启用异常的问题

v4.10.0
------------------------
2025年5月15日

!!! success "重大更新 ⚡️" 

    - feat: 新特权账户管理（PAM）：增强账户管理的安全性和灵活性
    - feat: 人脸识别认证：为用户提供更安全、便捷的认证方式【企业版】
    - feat: 多语言支持：包括英语、中文（简体）、中文（繁体）、日本语、葡萄牙语（巴西）、西班牙语、俄语和韩语

!!! info "新增功能 🌱"
    - feat: 添加了支持网络设备与目录服务集成
    - feat: 添加了自定义水印显示支持
    - feat: 启用了Passkey作为多因素认证（MFA）方法
    - feat: 云同步支持阿里云RDS【企业版】
    - feat: 表格中支持列拖放重新排序
    - feat: 支持了 Web GUI 连接到虚拟应用（Linux 应用发布）的文件传输和中文字符复制功能【企业版】
    - feat: 添加了通过VNC客户端连接到虚拟应用（Linux 应用发布）的支持【企业版】
    - perf: 添加了针对新创建用户和授权的默认到期天数的单独设置
    
!!! summary "功能优化 🚀" 
    
    - perf: 添加了从资产收集CPU和GPU型号信息的支持
    - perf: 使用Passkey登录的用户不再需要再次完成MFA
    - perf: 在资产或账户连接失败时显示详细的错误消息
    - perf: 优化如果用户在过去七天内从该城市登录，则城市的登录警报不会触发的逻辑
    - perf: 为用户手动设置弱密码的选项

!!! success "问题修复 🐛"
    - fix: 修复了资产会话重新连接失败的问题。
