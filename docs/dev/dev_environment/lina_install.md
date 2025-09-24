# Lina 环境搭建
## 1 Lina 组件概述
!!! tip ""
    - [Lina][lina] 是 JumpServer 的前端 UI 项目，主要使用 [Vue][vue]，[Element UI][element_ui] 完成。

### 1.1 环境要求
!!! tip ""

    | Name    | Lina                     | Node  |
    | :------ | :----------------------- | :---- |
    | Version | {{ jumpserver.tag }}     | 20.15.1  |

### 1.2 选择搭建方式
!!! tip ""
    === "克隆源代码仓库（推荐方式）。"  
        - 从 [Github][lina] 获取源代码，通过命令行中提取该存档：

        ```bash
        cd /opt
        git clone https://github.com/jumpserver/lina.git
        cd lina
        ```

        - 安装 Node。
        - 从 [Node][node] 官方网站参考文档部署 Node.js，请根据 [环境要求](#_6)，通过命令行中判断是否安装完成：   

        === "Ubuntu 22.04"
            ```bash
            cd /opt
            wget https://nodejs.org/download/release/v20.15.1/node-v20.15.1-linux-x64.tar.xz
            tar -xf node-v20.15.1-linux-x64.tar.xz
            mv node-v20.15.1-linux-x64 /usr/local/node
            chown -R root:root /usr/local/node
            export PATH=/usr/local/node/bin:$PATH
            echo 'export PATH=/usr/local/node/bin:$PATH' >> ~/.bashrc
            ```
        ```bash
        node -v
        ```
        `v20.15.1`

        - 安装依赖。

        ```bash
        cd /opt/lina
        npm install -g yarn
        yarn install
        ```

        - 修改配置文件。

        ```bash
        sed -i "s@Version <strong>.*</strong>@Version <strong>{{ jumpserver.tag }}</strong>@g" src/layout/components/Footer/index.vue
        vi .env.development
        ```
        ```yaml
        # 全局环境变量 请勿随意改动
        ENV = 'development'

        # base api
        VUE_APP_BASE_API = ''
        VUE_APP_PUBLIC_PATH = '/ui/'

        # vue-cli uses the VUE_CLI_BABEL_TRANSPILE_MODULES environment variable,
        # to control whether the babel-plugin-dynamic-import-node plugin is enabled.
        # It only does one thing by converting all import() to require().
        # This configuration can significantly increase the speed of hot updates,
        # when you have a large number of pages.
        # Detail:  https://github.com/vuejs/vue-cli/blob/dev/packages/@vue/babel-preset-app/index.js

        VUE_CLI_BABEL_TRANSPILE_MODULES = true

        # External auth
        VUE_APP_LOGIN_PATH = '/core/auth/login/'
        VUE_APP_LOGOUT_PATH = '/core/auth/logout/'


        # Dev server for core proxy
        VUE_APP_CORE_HOST = 'http://localhost:8080'   # 修改成 Core 的 url 地址
        VUE_APP_CORE_WS = 'ws://localhost:8080'
        VUE_APP_KOKO_HOST = 'http://localhost:5000'
        VUE_APP_KOKO_WS = 'ws://localhost:5000'
        VUE_APP_ENV = 'development'
        ```

        - 运行 Lina。

        ```bash
        yarn serve
        ```


    === "下载源代码压缩包并解压"

        - 下载 Release 文件，从 [Github][lina] 网站上获取最新的 [Release][lina_release] 副本。
        - 这些版本是最新代码的稳定快照。

        | OS     | Arch  | Name                                                          |
        | :----- | :---- | :------------------------------------------------------------ |
        | All    | All   | [lina-{{ jumpserver.tag }}.tar.gz][lina-{{ jumpserver.tag }}] |

        ```bash
        cd /opt
        wget https://github.com/jumpserver/lina/releases/download/{{ jumpserver.tag }}/lina-{{ jumpserver.tag }}.tar.gz
        tar -xf lina-{{ jumpserver.tag }}.tar.gz
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
