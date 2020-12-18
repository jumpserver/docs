# 其他方式升级说明

!!! warning "升级及迁移请保持 SECRET_KEY 与旧版本一致, 否则会导致数据库加密数据无法解密"
    - v2.5.0 必须使用 mysql5.7+ 作为 jumpserver 数据库, 请自行导入备份的 sql 完成迁移

## 极速安装升级

!!! tip ""
    ```sh
    cd /opt/jumpserver-installer-v2.6.0
    git pull
    ```
    ```sh
    ./jmsctl.sh upgrade
    ```

!!! info "可以使用 ./jmsctl.sh -h 查看帮助"
