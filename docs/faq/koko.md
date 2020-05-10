# Koko 常见问题

!!! info "请先确认下面选项"
    请在 `web` - `系统设置` - `安全设置` 里面允许 `终端注册`
    docker 容器部署的 `CORE_HOST` 不可以使用 `http://127.0.0.1:8080`

### 1. koko 启动异常

!!! question "启动异常"
    POST failed, get code: `403`, {"`detail`":"`身份认证信息未提供`。"}  
    POST failed, get code: `400`, {"`name`":["`名称重复`"]}  
    Connect Server error or access key is incalid, remove data/keys/.access_key run agent

    上面报错都按照下面处理

    ```sh
    cat /opt/jumpserver/config.yml | grep BOOTSTRAP_TOKEN
    ```

    !!! tip "正常部署的 koko 组件"
        在 web - 会话管理 - 终端管理 里面删除 koko 的注册 ( 在线显示红色的那个 )  
        删掉 koko/data/keys/ 下面的文件  
        修改 config.yml 里面的 BOOTSTRAP_TOKEN 为从 jumpserver/config.yml 获取的值  
        重启 koko  
        ```sh
        rm -rf data/keys/.access_key
        vi config.yml
        ./koko
        ```

    !!! tip "docker 容器部署的 koko 组件"
        在 web - 会话管理 - 终端管理 里面删除 koko 的注册 ( 在线显示红色的那个 )  
        删掉 jms_koko 容器  
        从 jumpserver/config.yml 获取 BOOTSTRAP_TOKEN  
        重新运行  
        ```sh
        docker rm jms_koko
        docker run --name jms_koko -d
          -p 2222:2222
          -p 127.0.0.1:5000:5000
          -e CORE_HOST=http://你的core_url:8080
          -e BOOTSTRAP_TOKEN=你的token
          -e LOG_LEVEL=ERROR
          --restart=always
        jumpserver/jms_koko:1.5.8
        ```

!!! question "docker logs -f jms_koko 提示 wait for jms_core ready"
    此问题一般是 CORE_HOST 使用了 127.0.0.1 或者修改了 firewalld iptables 导致网络故障
    ```sh
    systemctl restart jms_koko
    docker restart jms_koko
    docker logs -f jms_koko
    ```

    !!! tip "如果依旧提示 wait for jms_core ready"
    ```sh
    docker rm jms_koko
    docker run --name jms_koko -d
      -p 2222:2222
      -p 127.0.0.1:5000:5000
      -e CORE_HOST=http://你的core_url:8080
      -e BOOTSTRAP_TOKEN=你的token
      -e LOG_LEVEL=ERROR
      --restart=always
    jumpserver/jms_koko:1.5.8
    ```
