# Luna 环境搭建
## 1 Luna 组件概述
!!! tip ""
    [Luna][luna] 是 JumpServer 的 Web 终端的前端 UI 项目，主要使用 [Angular CLI][angular_cli] 完成。

### 1.1 环境要求
!!! tip ""

    | Name    | Luna                     | Node  |
    | :------ | :----------------------- | :---- |
    | Version | {{ jumpserver.tag }}     | 20.15.1 |

### 1.2 获取源代码
!!! tip ""
    === "克隆源代码仓库"
        - 从 [Github][luna] 获取源代码：

        ```bash
        cd /opt
        git clone https://github.com/jumpserver/luna.git
        cd luna
        ```

        - 安装 Node。
        - 从 [Node][node] 官方网站参考文档部署 Node.js，并通过命令行中判断是否安装完成：

        ```bash
        node -v
        ```
        `v20.15.1`

        - 安装依赖。

        ```bash
        cd /opt/luna
        yarn install
        ```

        - 修改配置文件。

        ```bash
        sed -i "s@[0-9].[0-9].[0-9]@{{ jumpserver.tag }}@g" src/environments/environment.prod.ts
        vi proxy.conf.json
        ```
        ```yaml
        {
          "/koko/": {
            "target": "http://localhost:5050",  # KoKo 地址
            "secure": false,
            "ws": true,
            "changeOrigin": true
          },
          "/media/": {
            "target": "http://localhost:8080",  # Core 地址
            "secure": false,
            "changeOrigin": true
          },
          "/api/": {
            "target": "http://localhost:8080",  # Core 地址
            "secure": false,
            "changeOrigin": true
          },
          "/ws/": {
            "target": "ws://localhost:8080",  # Core 地址
            "secure": false,
            "changeOrigin": true,
            "ws": true
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
          "/chen": {                            # Chen 地址
            "target": "http://localhost:9523",
            "secure": false,
            "ws": true,
            "changeOrigin": true
          },
          "/facelive": {                        # facelive 地址（企业版功能）
            "target": "http://localhost:5173",
            "secure": false,
            "ws": true,
            "changeOrigin": true
          },
          "/ui/": {                              # Lina 地址
            "target": "http://localhost:9528",
            "secure": false,
            "changeOrigin": true
          }
        }
        ```

        - 运行 Luna。

        ```bash
        yarn dev
        ```
    === "下载发布包"

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


[luna]: https://github.com/jumpserver/luna/
[angular_cli]: https://github.com/angular/angular-cli
[node]: https://nodejs.org/
[luna_release]: https://github.com/jumpserver/luna/releases/tag/{{ jumpserver.tag }}
[luna-{{ jumpserver.tag }}]: https://github.com/jumpserver/luna/releases/download/{{ jumpserver.tag }}/luna-{{ jumpserver.tag }}.tar.gz
[magnus-{{ jumpserver.tag }}-linux-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-amd64.tar.gz
[magnus-{{ jumpserver.tag }}-linux-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-arm64.tar.gz
[magnus-{{ jumpserver.tag }}-linux-loong64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-linux-loong64.tar.gz
[magnus-{{ jumpserver.tag }}-darwin-amd64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-darwin-amd64.tar.gz
[magnus-{{ jumpserver.tag }}-darwin-arm64]: https://github.com/jumpserver/magnus-release/releases/download/{{ jumpserver.tag }}/magnus-{{ jumpserver.tag }}-darwin-arm64.tar.gz
