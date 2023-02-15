# 命令行工具

## 1 命令行运维工具 - jmsctl
!!! tip ""
    - JumpServer 默认内置了命令行运维工具 - jmsctl，通过执行 jmsctl help 命令，可以查看相关的帮助文档。
    
    ```sh
    JumpServer部署管理脚本
    
    Usage: 
      ./jmsctl.sh [COMMAND] [ARGS...]
      ./jmsctl.sh --help

    Installation Commands: 
      install           安装 JumpServer 服务
      upgrade [version] 升级 JumpServer 服务
      check_update      检查 JumpServer 更新
      reconfig          重新配置 JumpServer 服务
    
    Management Commands: 
      start             启动 JumpServer 服务
      stop              停止 JumpServer 服务
      close             关闭 JumpServer 服务
      restart           重启 JumpServer 服务
      status            查看 JumpServer 服务运行状态
      down              脱机 JumpServer 服务
      uninstall         卸载 JumpServer 服务
    
    More Commands: 
      backup_db         备份 JumpServer 数据库
      restore_db [file] 通过数据库备份文件恢复数据
    ```