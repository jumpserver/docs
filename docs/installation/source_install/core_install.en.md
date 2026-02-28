# Core Environment Deployment

## 1 Core Component Overview

!!! tip ""
    - [Core][core] is the core component of JumpServer, developed based on [Django][django], with built-in [Gunicorn][gunicorn], [Celery][celery], Beat, [Flower][flower], and [Daphne][daphne] services.

### 1.1 Environment Requirements

!!! tip ""
    | Component | Version | Python Version |
    | --- | --- | --- |
    | Core | v4.10.9 | 3.9+ |

### 1.2 Download Source Code

!!! tip ""
    - Download the latest [Release][core_release] from the [Github][core] website. These versions are stable snapshots of the latest code. Downloaded sources are in .tar.gz archive format; extract using:

    ```bash
    cd /opt
    wget https://github.com/jumpserver/jumpserver/releases/download/v4.10.9/jumpserver-v4.10.9.tar.gz
    tar xf jumpserver-v4.10.9.tar.gz
    cd jumpserver-v4.10.9
    ```

### 1.3 Install Python3

!!! tip ""
    - Get Python3 deployment methods from the [Python][python] website. Verify installation completion according to [environment requirements](#_3) by:

    ```bash
    python3 --version
    # Python 3.9.0
    ```

### 1.4 Install Python Dependencies

!!! tip ""
    - Create a dedicated Python virtual environment for the JumpServer project:

    ```bash
    python3 -m venv /opt/py3
    source /opt/py3/bin/activate
    pip install -r requirements/requirements.txt
    ```

### 1.5 Start Core

!!! tip ""
    - To run in background, add -d: `./jms start -d`

    ```bash
    cd /opt/jumpserver-v4.10.9
    ./jms start
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
[python]: https://www.python.org/downloads/
[core_release]: https://github.com/jumpserver/jumpserver/releases/tag/v4.10.9
