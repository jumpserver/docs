# Luna 环境部署
## 1 Luna 组件简述
!!! tip ""
    [Luna][luna] 是 JumpServer 的前端 UI 项目，主要使用 [Angular CLI][angular_cli] 完成。

### 1.1 环境要求
!!! tip ""

    | Name    | Luna                     | Node  |
    | :------ | :----------------------- | :---- |
    | Version | {{ jumpserver.tag }}     | 16.5 |

### 1.2 选择部署方式
!!! tip ""
    === "源代码部署"

        - 下载源代码。
        - 可以从 [Github][luna] 网站上获取最新的 [Release][core_release] 副本。这些版本是最新代码的稳定快照，从项目网站下载 Source code.tar.gz 源代码，通过命令行中提取该存档：

        ```bash
        cd /opt
        mkdir /opt/luna-{{ jumpserver.tag }}
        wget -O /opt/luna-{{ jumpserver.tag }}.tar.gz https://github.com/jumpserver/luna/archive/refs/tags/{{ jumpserver.tag }}.tar.gz
        tar -xf luna-{{ jumpserver.tag }}.tar.gz -C /opt/luna-{{ jumpserver.tag }} --strip-components 1
        ```

        - 安装 Node。
        - 从 [Node][node] 官方网站参考文档部署 Node.js，请根据 [环境要求](#_10)，通过命令行中判断是否安装完成：

        ```bash
        node -v
        ```
        `v16.5`

        - 安装依赖。

        ```bash
        cd /opt/luna-{{ jumpserver.tag }}
        yarn install
        ```

        - 修改配置文件。

        ```bash
        sed -i "s@[0-9].[0-9].[0-9]@{{ jumpserver.tag }}@g" src/environments/environment.prod.ts
        vi proxy.conf.json
        ```
        ```yaml
        {
          "/koko": {
            "target": "http://localhost:5000",  # KoKo 地址
            "secure": false,
            "ws": true
          },
          "/media/": {
            "target": "http://localhost:8080",  # Core 地址
            "secure": false,
            "changeOrigin": true
          },
          "/api/": {
            "target": "http://localhost:8080",  # Core 地址
            "secure": false,                    # https ssl 需要开启
            "changeOrigin": true
          },
          "/core": {
            "target": "http://localhost:8080",  # Core 地址
            "secure": false,
            "changeOrigin": true
          },
          "/static": {
            "target": "http://localhost:8080",  # Core 地址
            "secure": false,
            "changeOrigin": true
          },
          "/lion": {
            "target": "http://localhost:9529",  # Lion 地址
            "secure": false,
            "pathRewrite": {
              "^/lion/monitor": "/monitor"
            },
            "ws": true,
            "changeOrigin": true
          },
          "/omnidb": {
            "target": "http://localhost:8082",
            "secure": false,
            "ws": true,
            "changeOrigin": true
          }
        }
        ```

        - 运行 Luna。

        ```bash
        ./node_modules/.bin/ng serve
        ```

        - 构建 Luna。

        ```bash
        yarn build
        cp -R src/assets/i18n luna/
        cp -rf luna luna-{{ jumpserver.tag }}
        tar -czf luna-{{ jumpserver.tag }}.tar.gz luna-{{ jumpserver.tag }}
        ```

        !!! tip "构建完成后, 生成在 luna 目录下"

    === "使用 Release"

        - 下载 Release 文件，从 [Github][luna] 网站上获取最新的 [Release][luna_release] 副本。
        - 这些版本是最新代码的稳定快照。

        | OS     | Arch  | Name                                                          |
        | :----- | :---- | :------------------------------------------------------------ |
        | All    | All   | [luna-{{ jumpserver.tag }}.tar.gz][luna-{{ jumpserver.tag }}] |

        ```bash
        cd /opt
        wget https://github.com/jumpserver/luna/releases/download/{{ jumpserver.tag }}/luna-{{ jumpserver.tag }}.tar.gz
        tar -xf luna-{{ jumpserver.tag }}.tar.gz
        ```


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
