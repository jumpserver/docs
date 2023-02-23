# Lina 环境部署
## 1 Lina 组件简述
!!! tip ""
    - [Lina][lina] 是 JumpServer 的前端 UI 项目，主要使用 [Vue][vue]，[Element UI][element_ui] 完成。

### 1.1 环境要求
!!! tip ""

    | Name    | Lina                     | Node  |
    | :------ | :----------------------- | :---- |
    | Version | {{ jumpserver.version }} | 14.16 |

### 1.2 选择部署方式
!!! tip ""
    === "源代码部署"  
        - 下载源代码。
        - 从 [Github][lina] 下载 Source code.tar.gz 源代码，通过命令行中提取该存档：

        ```bash
        cd /opt
        mkdir /opt/lina-{{ jumpserver.version }}
        wget -O /opt/lina-{{ jumpserver.version }}.tar.gz https://github.com/jumpserver/lina/archive/refs/tags/{{ jumpserver.version }}.tar.gz
        tar -xf lina-{{ jumpserver.version }}.tar.gz -C /opt/lina-{{ jumpserver.version }} --strip-components 1
        ```
    
        - 安装 Node。
        - 从 [Node][node] 官方网站参考文档部署 Node.js，请根据 [环境要求](#_6)，通过命令行中判断是否安装完成：   

        === "Ubuntu 20.04"
            ```bash
            cd /opt
            wget https://nodejs.org/download/release/v14.16.1/node-v14.16.1-linux-x64.tar.xz
            tar -xf node-v14.16.1-linux-x64.tar.xz
            mv node-v14.16.1-linux-x64 /usr/local/node
            chown -R root:root /usr/local/node
            export PATH=/usr/local/node/bin:$PATH
            echo 'export PATH=/usr/local/node/bin:$PATH' >> ~/.bashrc
            ```
        ```bash
        node -v
        ```
        `v14.16.1`
    
        - 安装依赖。

        ```bash
        cd /opt/lina-{{ jumpserver.version }}
        npm install -g yarn
        yarn install
        ```
    
        - 修改配置文件。

        ```bash
        sed -i "s@Version <strong>.*</strong>@Version <strong>{{ jumpserver.version }}</strong>@g" src/layout/components/Footer/index.vue
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
        VUE_APP_CORE_HOST = 'http://localhost:8080'  # 修改成 Core 的 url 地址
        VUE_APP_CORE_WS = 'ws://localhost:8070'
        VUE_APP_ENV = 'development'
        ```
    
        - 运行 Lina。

        ```bash
        yarn serve
        ```
    
        - 构建 Lina。

        ```bash
        yarn build
        cp -rf lina lina-{{ jumpserver.version }}
        tar -czf lina-{{ jumpserver.version }}.tar.gz lina-{{ jumpserver.version }}
        ```
    
        !!! tip "构建完成后, 生成在 lina 目录下"
    
    === "使用 Release"
    
        - 下载 Release 文件，从 [Github][lina] 网站上获取最新的 [Release][lina_release] 副本。
        - 这些版本是最新代码的稳定快照。
    
        | OS     | Arch  | Name                                                                  |
        | :----- | :---- | :-------------------------------------------------------------------- |
        | All    | All   | [lina-{{ jumpserver.version }}.tar.gz][lina-{{ jumpserver.version }}] |

        ```bash
        cd /opt
        wget https://github.com/jumpserver/lina/releases/download/{{ jumpserver.version }}/lina-{{ jumpserver.version }}.tar.gz
        tar -xf lina-{{ jumpserver.version }}.tar.gz
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
[core_release]: https://github.com/jumpserver/jumpserver/releases/tag/{{ jumpserver.version }}
[python]: https://www.python.org/downloads/
[linux_packages]: http://nginx.org/en/linux_packages.html
[lina_release]: https://github.com/jumpserver/lina/releases/tag/{{ jumpserver.version }}
[node]: https://nodejs.org/
[luna_release]: https://github.com/jumpserver/luna/releases/tag/{{ jumpserver.version }}
[koko_release]: https://github.com/jumpserver/koko/releases/tag/{{ jumpserver.version }}
[go]: https://golang.google.cn/
[koko]: https://github.com/jumpserver/koko
[koko_release]: https://github.com/jumpserver/koko/releases/tag/{{ jumpserver.version }}
[lion]: https://github.com/jumpserver/lion-release
[lion_release]: https://github.com/jumpserver/lion-release/releases/tag/{{ jumpserver.version }}
[guacamole]: http://guacamole.apache.org/
[apache]: http://www.apache.org/
[guacamole-server]: https://github.com/apache/guacamole-server
[building-guacamole-server]: http://guacamole.apache.org/doc/gug/installing-guacamole.html#building-guacamole-server
[guacd-1.4.0]: http://download.jumpserver.org/public/guacamole-server-1.4.0.tar.gz
[wisp]: https://github.com/jumpserver/wisp
[wisp_release]: https://github.com/jumpserver/wisp/releases/tag/{{ jumpserver.wisp }}
[magnus]: https://github.com/jumpserver/magnus-release
[magnus_release]: https://github.com/jumpserver/magnus-release/releases/tag/{{ jumpserver.version }}
[lina-{{ jumpserver.version }}]: https://github.com/jumpserver/lina/releases/download/{{ jumpserver.version }}/lina-{{ jumpserver.version }}.tar.gz
[luna-{{ jumpserver.version }}]: https://github.com/jumpserver/luna/releases/download/{{ jumpserver.version }}/luna-{{ jumpserver.version }}.tar.gz
[koko-{{ jumpserver.version }}-linux-amd64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-linux-amd64.tar.gz
[koko-{{ jumpserver.version }}-linux-arm64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-linux-arm64.tar.gz
[koko-{{ jumpserver.version }}-linux-loong64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-linux-loong64.tar.gz
[koko-{{ jumpserver.version }}-darwin-amd64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-darwin-amd64.tar.gz
[koko-{{ jumpserver.version }}-darwin-arm64]: https://github.com/jumpserver/koko/releases/download/{{ jumpserver.version }}/koko-{{ jumpserver.version }}-darwin-arm64.tar.gz
[lion-{{ jumpserver.version }}-linux-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-linux-amd64.tar.gz
[lion-{{ jumpserver.version }}-linux-arm64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-linux-arm64.tar.gz
[lion-{{ jumpserver.version }}-linux-loong64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-linux-loong64.tar.gz
[lion-{{ jumpserver.version }}-darwin-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-darwin-amd64.tar.gz
[lion-{{ jumpserver.version }}-windows-amd64]: https://github.com/jumpserver/lion-release/releases/download/{{ jumpserver.version }}/lion-{{ jumpserver.version }}-windows-amd64.tar.gz
[magnus-{{ jumpserver.version }}-linux-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-linux-amd64.tar.gz
[magnus-{{ jumpserver.version }}-linux-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-linux-arm64.tar.gz
[magnus-{{ jumpserver.version }}-linux-loong64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-linux-loong64.tar.gz
[magnus-{{ jumpserver.version }}-darwin-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-darwin-amd64.tar.gz
[magnus-{{ jumpserver.version }}-darwin-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.version }}/magnus-{{ jumpserver.version }}-darwin-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-amd64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-arm64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-linux-loong64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-linux-loong64.tar.gz
[wisp-{{ jumpserver.wisp }}-darwin-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-darwin-amd64.tar.gz
[wisp-{{ jumpserver.wisp }}-darwin-arm64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-darwin-arm64.tar.gz
[wisp-{{ jumpserver.wisp }}-windows-amd64]: https://github.com/jumpserver/wisp/releases/download/{{ jumpserver.wisp }}/wisp-{{ jumpserver.wisp }}-windows-amd64.tar.gz