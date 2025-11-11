## 1 系统组件日志

JumpServer 的默认安装地址为 `/data/jumpserver`，具体安装地址可执行以下命令查看：

```bash
cat /opt/jumpserver/config/config.txt | grep VOLUME_DIR
```

本次示例以 `/data/jumpserver/` 为例：

JumpServer 的核心日志存放在 `/data/jumpserver/core/data/logs`。

**核心日志文件详细介绍**

| 日志文件名 | 说明 |
| :--- | :--- |
| `ansible.log` | ansible 执行任务产生的日志（linux 测试资产可连接性、更新硬件信息、推送系统用户、linux 执行改密计划等） |
| `beat.log` | 定时任务的日志 |
| `celery_ansible.log` | 异步任务 ansible 队列下的任务日志 |
| `celery_default.log` | 异步任务默认队列下的任务日志 |
| `drf_exception.log` | 使用 DRF 框架抛出的异常信息 |
| `flower.log` | 作业中心的任务监控组件日志 |
| `gunicorn.log` | 用来记录请求的日志 |
| `jumpserver.log` | JumpServer 的总日志 |

**其他组件的日志文件位置**

| 组件名称 | 日志文件路径 |
| :--- | :--- |
| Celery | `/data/jumpserver/celery/data/logs` |
| Lion | `/data/jumpserver/lion/data/logs` |
| Koko | `/data/jumpserver/koko/data/logs` |
| Razor | `/data/jumpserver/razor/data/logs` |
| Xrdp | `/data/jumpserver/xrdp/data/logs` |
| Chen | `/data/jumpserver/chen/data/logs` |
| Magnus | `/data/jumpserver/magnus/data/logs` |
| Web | `/data/jumpserver/web/data/logs` |
| Facelive | `/data/jumpserver/facelive/data/logs` |
| Nec | `/data/jumpserver/nec/data/logs` |

## 2 Docker 日志查看

**示例：查看 core 容器的后 100 行日志**

```bash
docker logs -f jms_core --tail 100
```

**查看其他组件的实时日志**

```bash
# 通过容器 ID 查看
docker logs -f [Container ID]

# 通过容器名称查看
docker logs -f [Container name]
```