# 在线升级

!!! warning "升级到 v4 前需要先升级到 v3 最新版本，否则升级将会直接失败"

!!! tip ""
    - 请先手动备份好数据库, 然后继续操作。
    - values.yaml 从 https://github.com/jumpserver/helm-charts/blob/main/charts/jumpserver/values.yaml 获取指定版本的配置文件。
    - 不想使用 values.yaml 可以使用 --set key=value 的方式传参

!!! tip ""
    ```sh
    helm repo update
    helm upgrade jms-k8s jumpserver/jumpserver -n default -f values.yaml
    ```