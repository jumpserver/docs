# Command-line Tools

## 1 Command-line Operations Tool - jmsctl

!!! tip ""
    - JumpServer includes a built-in command-line operations tool - jmsctl. Execute the `jmsctl help` command to view relevant help documentation.

    ```sh
    JumpServer Deployment Management Script
    
    Usage: 
      ./jmsctl.sh [COMMAND] [ARGS...]
      ./jmsctl.sh --help

    Installation Commands: 
      install           Install JumpServer service

    Management Commands:
      config            Configuration tool; execute jmsctl config --help to view help
      start             Start JumpServer service
      stop              Stop JumpServer service
      restart           Restart JumpServer service
      status            View JumpServer service running status
      down              Take JumpServer service offline
      uninstall         Uninstall JumpServer service
    
    More Commands: 
      load_image        Load Docker image
      backup_db         Backup JumpServer database
      restore_db [file] Restore data through database backup file
      raw               Execute raw docker compose command
      tail [service]    View Service logs
    ```

## 2 Configuration Tool - jmsctl config

!!! tip ""
    - JumpServer includes a built-in configuration tool - jmsctl config. Execute the `jmsctl config help` command to view relevant help documentation.

    ```sh
    Usage: 
      ./jmsctl.sh config [ARGS...]
      -h, --help

    Args: 
      ntp              Configure NTP synchronization
      init             Initialize config configuration file
      port             Configure JumpServer service port
      ssl              Configure Web SSL
      env              Configure JumpServer environment variables
    ```
