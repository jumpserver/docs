# Online Upgrade

!!! warning "If upgrading JumpServer V3 to V4, you need to upgrade to the latest version of V3 first, otherwise the upgrade will fail!"

!!! tip ""
    - Please manually backup the database first, then proceed with the operation.
    - Get values.yaml from https://github.com/jumpserver/helm-charts/blob/main/charts/jumpserver/values.yaml for the specific version configuration file.
    - If you don't want to use values.yaml, you can use the --set key=value method to pass parameters

!!! tip ""
    ```sh
    helm repo update
    helm upgrade jms-k8s jumpserver/jumpserver -n default -f values.yaml
    ```
