# 存储设置
!!! tip ""
    - 通过点击页面右上角小齿轮进入 **系统设置** 页面，点击 **存储设置** ，进入存储设置页面。
    - 存储设置页面主要配置 JumpServer 录像存储、账号被封以及命令存储的设置。
  
## 1 对象存储
!!! tip ""
    - 对象存储页面可以对JumpServer连接资产的会话录像存储的位置进行自定义。目前支持的外部录像存储有亚马逊的 S3 云存储、Ceph、Swift、OSS、Azure、OBS、COS。
    - SFTP 存储仅支持作为账号备份服务器。
  
!!! info "注: 账号备份以及 SFTP 存储为企业版功能"

## 2 命令存储
!!! tip ""
    - 命令存储页面可以更改JumpServer连接资产的会话命令记录存储的位置。默认的资产会话命令记录存储在JumpServer的数据库中，目前支持的外部命令存储有Elasticsearch。
    - Elasticsearch 主机格式为 `http://es_user:es_password@es_host:es_port`。
    - 如果开启按日期建立索引，那么输入的值会作为索引前缀。