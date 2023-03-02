# 在线升级

!!! warning "v3 版本与 v2 版本存在一定的差异，如需 v2 版本升级至 v3 版本 [请先阅读此文档](https://kb.fit2cloud.com/?p=06638d69-f109-4333-b5bf-65b17b297ed9){:target="_blank"}"

!!! info "升级前请先参考 [升级或迁移须知](../upgrade_notice.md)"

!!! tip ""
    - 请先手动备份好数据库, 然后继续操作。
    - values.yaml 从 https://github.com/jumpserver/helm-charts/blob/main/charts/jumpserver/values.yaml 获取。

    ```sh
    helm repo update
    helm upgrade jms-k8s jumpserver/jumpserver -n default -f values.yaml
    ```

!!! warning ""
    - 也可以使用 --set key=value 的方式传参。
