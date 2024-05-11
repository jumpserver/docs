# 命令行工具

## 1 命令行运维工具 - jmsctl
!!! tip ""
    - JumpServer 默认内置了命令行运维工具 - jmsctl，通过执行 jmsctl help 命令，可以查看相关的帮助文档。
    
    ```sh
    JumpServer 部署管理脚本
    
    Usage: 
      ./jmsctl.sh [COMMAND] [ARGS...]
      ./jmsctl.sh --help

    Installation Commands: 
      install           安装 JumpServer 服务

    Management Commands:
      config            配置工具，执行 jmsctl config --help，查看帮助
      start             启动 JumpServer 服务
      stop              停止 JumpServer 服务
      restart           重启 JumpServer 服务
      status            查看 JumpServer 服务运行状态
      down              脱机 JumpServer 服务
      uninstall         卸载 JumpServer 服务
    
    More Commands: 
      load_image        加载 Docker 镜像
      backup_db         备份 JumpServer 数据库
      restore_db [file] 通过数据库备份文件恢复数据
      raw               执行原始 docker compose 命令
      tail [service]    查看 Service 日志
    ```

## 2 配置工具 - jmsctl config
!!! tip ""
    - JumpServer 默认内置了配置工具 - jmsctl config，通过执行 jmsctl config help 命令，可以查看相关的帮助文档。

    ```sh
    Usage: 
      ./jmsctl.sh config [ARGS...]
      -h, --help

    Args: 
      ntp              配置 NTP 同步
      init             初始化 config 配置文件
      port             配置 JumpServer 服务端口
      ssl              配置 Web SSL 
      env              配置 JumpServer 环境变量
    ```