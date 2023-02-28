# Nginx 环境部署
## 1 操作过程
!!! tip ""
    - 从 [Nginx][nginx] 官方网站上获取 Nginx 的最新发行版本 [linux_packages][linux_packages]，通过命令行验证安装是否完成：

    === "Ubuntu 20.04"
        ```bash
        apt-get install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring
        echo "deb http://nginx.org/packages/ubuntu focal nginx" > /etc/apt/sources.list.d/nginx.list
        curl -o /etc/apt/trusted.gpg.d/nginx_signing.asc https://nginx.org/keys/nginx_signing.key
        apt-get update
        apt-get install -y nginx
        echo > /etc/nginx/conf.d/default.conf
        ```
    
    ```bash
    nginx -v
    ```
    `nginx version: nginx/1.20.2`


[nginx]: http://nginx.org/
[lina]: https://github.com/jumpserver/lina/
[vue]: https://cn.vuejs.org/
[element_ui]: https://element.eleme.cn/
[luna]: https://github.com/jumpserver/luna/
[angular_cli]: https://github.com/angular/angular-cli
[core]: https://github.com/jumpserver/jumpserver/
[django]: https://docs.djangoproject.com/
[gunicorn]: https://gunicorn.org/
[celery]: https://docs.celeryproject.org/
[flower]: https://github.com/mher/flower/
[daphne]: https://github.com/django/daphne/
[github]: https://github.com/
[core_release]: https://github.com/jumpserver/jumpserver/releases/tag/{{ jumpserver.tag }}
[python]: https://www.python.org/downloads/
[linux_packages]: http://nginx.org/en/linux_packages.html
[lina_release]: https://github.com/jumpserver/lina/releases/tag/{{ jumpserver.tag }}
[node]: https://nodejs.org/
[luna_release]: https://github.com/jumpserver/luna/releases/tag/{{ jumpserver.tag }}
[koko_release]: https://github.com/jumpserver/koko/releases/tag/{{ jumpserver.tag }}
[go]: https://golang.google.cn/
[koko]: https://github.com/jumpserver/koko
[koko_release]: https://github.com/jumpserver/koko/releases/tag/{{ jumpserver.tag }}
[lion]: https://github.com/jumpserver/lion-release
[lion_release]: https://github.com/jumpserver/lion-release/releases/tag/{{ jumpserver.tag }}
[guacamole]: http://guacamole.apache.org/
[apache]: http://www.apache.org/
[guacamole-server]: https://github.com/apache/guacamole-server
[building-guacamole-server]: http://guacamole.apache.org/doc/gug/installing-guacamole.html#building-guacamole-server
[guacd-1.4.0]: http://download.jumpserver.org/public/guacamole-server-1.4.0.tar.gz
[wisp]: https://github.com/jumpserver/wisp
[wisp_release]: https://github.com/jumpserver/wisp/releases/tag/{{ jumpserver.wisp }}
[magnus]: https://github.com/jumpserver/magnus-release
[magnus_release]: https://github.com/jumpserver/magnus-release/releases/tag/{{ jumpserver.tag }}
[lina-{{ jumpserver.tag }}]: https://github.com/jumpserver/lina/releases/download/{{ jumpserver.tag }}/lina-{{ jumpserver.tag }}.tar.gz
[luna-{{ jumpserver.tag }}]: https://github.com/jumpserver/luna/releases/download/{{ jumpserver.tag }}/luna-{{ jumpserver.tag }}.tar.gz
[koko-{{ jumpserver.tag }}-linux-amd64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-linux-amd64.tar.gz
[koko-{{ jumpserver.tag }}-linux-arm64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-linux-arm64.tar.gz
[koko-{{ jumpserver.tag }}-linux-loong64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-linux-loong64.tar.gz
[koko-{{ jumpserver.tag }}-darwin-amd64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-darwin-amd64.tar.gz
[koko-{{ jumpserver.tag }}-darwin-arm64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.tag }}/koko-{{ jumpserver.tag }}-darwin-arm64.tar.gz
[lion-{{ jumpserver.tag }}-linux-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-linux-amd64.tar.gz
[lion-{{ jumpserver.tag }}-linux-arm64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-linux-arm64.tar.gz
[lion-{{ jumpserver.tag }}-linux-loong64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-linux-loong64.tar.gz
[lion-{{ jumpserver.tag }}-darwin-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-darwin-amd64.tar.gz
[lion-{{ jumpserver.tag }}-windows-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.tag }}/lion-{{ jumpserver.tag }}-windows-amd64.tar.gz
[magnus-{{ jumpserver.tag }}-linux-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-amd64.tar.gz
[magnus-{{ jumpserver.tag }}-linux-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-arm64.tar.gz
[magnus-{{ jumpserver.tag }}-linux-loong64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-loong64.tar.gz
[magnus-{{ jumpserver.tag }}-darwin-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-darwin-amd64.tar.gz
[magnus-{{ jumpserver.tag }}-darwin-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-darwin-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-amd64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-arm64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-loong64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-loong64.tar.gz
[wisp-{{ jumpserver.wisp }}-darwin-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-darwin-amd64.tar.gz
[wisp-{{ jumpserver.wisp }}-darwin-arm64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-darwin-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-windows-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-windows-amd64.tar.gz