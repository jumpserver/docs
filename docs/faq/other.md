# 其他问题

!!! question "下载 Docker 镜像很慢"
    默认情况下, 使用极速安装使用的默认加速源是网易的
    ```sh
    cat /etc/docker/daemon.json
    ```
    ```yaml
    {
        "registry-mirrors": ["https://hub-mirror.c.163.com", "https://bmtrgdvx.mirror.aliyuncs.com", "https://dockerhub.azk8s.cn"]
    }
    ```
    你可以使用其他的镜像源替换掉 https://hub-mirror.c.163.com, 我们推荐使用阿里云的镜像源，阿里云的镜像源速度很快且免费，登陆 https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors 申请
