# Kubernetes 应用要求

!!! info "集群填写的是 K8S 的集群地址"
    直接访问集群地址页面可以显示如下信息(如: https://172.16.8.8:8443)
    ```json
    {
      "kind": "Status",
      "apiVersion": "v1",
      "metadata": {

      },
      "status": "Failure",
      "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
      "reason": "Forbidden",
      "details": {

      },
      "code": 403
    }
    ```

!!! tip "获取 TOKEN 方法"
    - 下面以 ko-admin 为例
    
    ```sh
    kubectl get secret -n kube-system
    ```
    ```vim
    > kubectl get secret -n kube-system
    NAME                                             TYPE                                  DATA   AGE
    attachdetach-controller-token-qss79              kubernetes.io/service-account-token   3      44m
    bootstrap-signer-token-ftqb6                     kubernetes.io/service-account-token   3      44m
    bootstrap-token-abcdef                           bootstrap.kubernetes.io/token         5      44m
    certificate-controller-token-gm8mf               kubernetes.io/service-account-token   3      44m
    clusterrole-aggregation-controller-token-92v9j   kubernetes.io/service-account-token   3      44m
    coredns-token-mjpwp                              kubernetes.io/service-account-token   3      44m
    cronjob-controller-token-bjdn5                   kubernetes.io/service-account-token   3      44m
    daemon-set-controller-token-6wljg                kubernetes.io/service-account-token   3      44m
    default-token-9pl84                              kubernetes.io/service-account-token   3      44m
    deployment-controller-token-wbpq6                kubernetes.io/service-account-token   3      44m
    disruption-controller-token-9mrbr                kubernetes.io/service-account-token   3      44m
    endpoint-controller-token-hmgw5                  kubernetes.io/service-account-token   3      44m
    endpointslice-controller-token-pbnkw             kubernetes.io/service-account-token   3      44m
    endpointslicemirroring-controller-token-zkc6z    kubernetes.io/service-account-token   3      44m
    expand-controller-token-btlqv                    kubernetes.io/service-account-token   3      44m
    flannel-token-qc6kw                              kubernetes.io/service-account-token   3      42m
    generic-garbage-collector-token-j8c7c            kubernetes.io/service-account-token   3      44m
    horizontal-pod-autoscaler-token-v9d49            kubernetes.io/service-account-token   3      44m
    job-controller-token-9pldd                       kubernetes.io/service-account-token   3      44m
    ko-admin-token-kprl9                             kubernetes.io/service-account-token   3      40m
    kube-proxy-token-9pfd2                           kubernetes.io/service-account-token   3      44m
    metrics-server-token-cmdpk                       kubernetes.io/service-account-token   3      41m
    namespace-controller-token-k94nh                 kubernetes.io/service-account-token   3      44m
    nfs-client-provisioner-token-pb5qx               kubernetes.io/service-account-token   3      28m
    nginx-ingress-serviceaccount-token-vk8tm         kubernetes.io/service-account-token   3      41m
    node-controller-token-v5k59                      kubernetes.io/service-account-token   3      44m
    persistent-volume-binder-token-jfgm7             kubernetes.io/service-account-token   3      44m
    pod-garbage-collector-token-7lptd                kubernetes.io/service-account-token   3      44m
    pv-protection-controller-token-fpqqm             kubernetes.io/service-account-token   3      44m
    pvc-protection-controller-token-wcrmp            kubernetes.io/service-account-token   3      44m
    replicaset-controller-token-9g9s7                kubernetes.io/service-account-token   3      44m
    replication-controller-token-xg4fq               kubernetes.io/service-account-token   3      44m
    resourcequota-controller-token-lskn4             kubernetes.io/service-account-token   3      44m
    root-ca-cert-publisher-token-sdt67               kubernetes.io/service-account-token   3      44m
    service-account-controller-token-2xr8k           kubernetes.io/service-account-token   3      44m
    service-controller-token-9dghl                   kubernetes.io/service-account-token   3      44m
    statefulset-controller-token-wqm5v               kubernetes.io/service-account-token   3      44m
    token-cleaner-token-gv552                        kubernetes.io/service-account-token   3      44m
    ttl-controller-token-cgqcd                       kubernetes.io/service-account-token   3      44m
    ```
    ```sh
    kubectl describe secret ko-admin-token-kprl9 -n kube-system
    ```
    ```vim
    > kubectl describe secret ko-admin-token-kprl9 -n kube-system
    Name:         ko-admin-token-kprl9
    Namespace:    kube-system
    Labels:       <none>
    Annotations:  kubernetes.io/service-account.name: ko-admin
                  kubernetes.io/service-account.uid: 8be05ad6-83ce-483b-9324-7c3f041c6da1

    Type:  kubernetes.io/service-account-token

    Data
    ====
    ca.crt:     1038 bytes
    namespace:  11 bytes
    token:      eyJhbGciOiJSUzI1NiIsImtpZCI6ImlCVkhHTlhHem9idXNtYmtsaVpDZXRESVFMSHRFNUdsOFJWOXc0MnRZTG8ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvsA50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmAxbmV0ZXMuaW8vc6VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrby1hZG1pbi10b2tlbi1rcHJsOSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2AxdmljZS1hY2NvdW50Lm5hbQAiOiJrby1hZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFiQ291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjhiZTA1YWQ2LTgzY2UtNDgzYi05MzI0LTdjM2YwNDFjNmRhMSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprby1hZG1pbiJ9.qP04Yd6sTf5IDbQ_9lF_VdoyBEN5UCBmp1P7tvv9Fn9ibZFOGsupXjzbxCMhu3HhkGSE1pUuu1NNmcJUCUb_pFi5x5Bvo2xkF1_SfQACo40kzrUQ9ATTX8wuDzpiNw9sjf-_1l7rwnseOC4WJYNQIOs9i9FOeyRPYbKvkwsysJBVCq_XkoqvZt9xPp-LtsMUdWKHhLKUkBBM5F1NpVyahSrrsgH2lRuNsGALGb0FGIwYfMWN6KaHim2eeOaH4nqnVJ0WGCVJNx9-_PJQXfFWZtnceF_IiTUGwC7fqrA7T-5vOafPvG7c6PgjPzgMyEo4ade1bRV3fM98gHs_5v-oVw
    ```

    !!! tip "上面 token: 后面的内容就是我们需要的 token, 把这个内容填写到 JumpServer 系统用户里面即可"
