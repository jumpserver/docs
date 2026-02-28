# KoKo Environment Deployment

## 1 KoKo Component Overview

!!! tip ""
    KoKo is the Go version of coco, which reconstructed coco's SSH/SFTP service and Web Terminal service.

### 1.1 Environment Requirements

!!! tip ""
    | Component | Version | Go Version | Node Version | Redis Version |
    | --- | --- | --- | --- | --- |
    | KoKo | v4.10.9 | 1.18+ | 16.5+ | >= 6.0 |

### 1.2 Select Deployment Method

!!! tip ""
    === "Source Code Deployment"
        - Download from [GitHub][koko] releases
        - Extract and configure

### 1.3 Modify Configuration File

!!! tip ""
    ```bash
    cd /opt/koko
    vi config.yml
    ```
    Configure database, Redis, and other settings as needed.

### 1.4 Start KoKo

!!! tip ""
    ```bash
    cd /opt/koko
    ./koko
    ```

[nginx]: http://nginx.org/
[lina]: https://github.com/jumpserver/lina/
[vue]: https://cn.vuejs.org/
[element_ui]: https://element.eleme.cn/
[luna]: https://github.com/jumpserver/luna/
[angular_cli]: https://github.com/angular/angular-cli
[core]: https://github.com/jumpserver/jumpserver/
[koko]: https://github.com/jumpserver/koko
[django]: https://docs.djangoproject.com/
[gunicorn]: https://gunicorn.org/
[celery]: https://docs.celeryproject.org/
[flower]: https://github.com/mher/flower/
[daphne]: https://github.com/django/daphne/
[go]: https://golang.google.cn/
