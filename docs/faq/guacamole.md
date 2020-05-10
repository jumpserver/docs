# Guacamole 常见问题

!!! info "请先确认下面选项"
    请在 `web` - `系统设置` - `安全设置` 里面允许 `终端注册`  
    docker 容器部署的 `JUMPSERVER_SERVER` 不可以使用 `http://127.0.0.1:8080`

### 1. guacamole 启动异常

!!! info "guacamole 组件不在线可按照下面处理"

```sh
cat /opt/jumpserver/config.yml | grep BOOTSTRAP_TOKEN
```

!!! question "docker logs -f jms_guacamole 提示 wait for jms_core ready"
    此问题一般是 JUMPSERVER_SERVER 使用了 127.0.0.1 或者修改了 firewalld iptables 导致网络故障
    ```sh
    systemctl restart jms_guacamole
    docker restart jms_guacamole
    docker logs -f jms_guacamole
    ```

    !!! tip "如果依旧提示 wait for jms_core ready"
    ```sh
    docker rm jms_guacamole
    docker run --name jms_guacamole -d
      -p 127.0.0.1:8081:8080
      -e JUMPSERVER_SERVER=http://你的core_url:8080
      -e BOOTSTRAP_TOKEN=你的token
      -e GUACAMOLE_LOG_LEVEL=ERROR
    jumpserver/jms_guacamole:1.5.8
    ```
