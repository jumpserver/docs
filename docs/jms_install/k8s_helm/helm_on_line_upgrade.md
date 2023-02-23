# 在线升级

!!! warning "注意"
    - [JumpServer 在做升级或迁移操作前，请先阅读升级须知](../upgrade_notice.md)
    - 升级前做好数据库的备份工作是一个良好的习惯。

!!! tip ""
    - 请先手动备份好数据库, 然后继续操作。
    - values.yaml 从 https://github.com/jumpserver/helm-charts/blob/main/charts/jumpserver/values.yaml 获取。

    ```sh
    helm repo update
    helm upgrade jms-k8s jumpserver/jumpserver -n default -f values.yaml
    ```

!!! warning "注意"
    - 也可以使用 --set key=value 的方式传参。