# Guacamole 常见问题

!!! info "请先确认下面选项"
    请在 `web` - `系统设置` - `安全设置` 里面允许 `终端注册`  
    Docker 容器部署的 `JUMPSERVER_SERVER` 不可以使用 `http://127.0.0.1:8080`

### 1. guacamole 启动异常

!!! question "启动异常"
    ERROR o.a.g.a.j.r.JumpserverRegisterService 121 - 注册终端失败

    上面报错都按照下面处理

    ```sh
    cat /opt/jumpserver/config.yml | grep BOOTSTRAP_TOKEN
    ```

    !!! info "guacamole 组件不在线可按照下面处理"

    !!! tip "正常部署的 guacamole 组件"
        在 web - 会话管理 - 终端管理 里面删除 [Gua] 开头的注册 ( 在线显示红色的那个 )  
        删掉 guacamole/data/keys/ 下面的文件(旧版本可能在 /config/guacamole/keys)  
        ```sh
        rm -f /config/guacamole/data/keys/jumpserver.key
        env | grep $BOOTSTRAP_TOKEN  # 确定 token 和上面查询的一致
        sh /config/tomcat9/bin/shutdown.sh

        /etc/init.d/guacd restart
        sh /config/tomcat9/bin/startup.sh
        ```

    !!! tip "docker 容器部署的 guacamole 组件"
        在 web - 会话管理 - 终端管理 里面删除 [Gua] 开头的注册 ( 在线显示红色的那个 )  
        删掉 jms_guacamole 容器  
        从 jumpserver/config.yml 获取 BOOTSTRAP_TOKEN  
        重新运行  
        ```sh
        docker rm jms_guacamole
        docker run --name jms_guacamole -d \
          -p 127.0.0.1:8081:8080 \
          -e JUMPSERVER_SERVER=http://你的core_url:8080 \
          -e BOOTSTRAP_TOKEN=你的token \
          -e GUACAMOLE_LOG_LEVEL=ERROR \
          jumpserver/jms_guacamole:v2.3.1
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
    docker stop jms_guacamole
    docker rm jms_guacamole
    docker run --name jms_guacamole -d
      -p 127.0.0.1:8081:8080
      -e JUMPSERVER_SERVER=http://你的core_url:8080
      -e BOOTSTRAP_TOKEN=你的token
      -e GUACAMOLE_LOG_LEVEL=ERROR
    jumpserver/jms_guacamole:v2.3.1
    ```
