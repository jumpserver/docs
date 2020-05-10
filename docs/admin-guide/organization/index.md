# 组织管理

- 组织创建成功后 管理员 可以在 web 主页面的左上角进行组织切换
- 用户可以同时存在多个组织，管理员也可以同时管理多个组织

### 1. 控制台

```sh
source /opt/py3/bin/activate
cd /opt/jumpserver/apps
python manage.py shell
```

### 2. 添加组织

```python
from assets.models import Asset
from orgs.models import Organization
dev_org = Organization.objects.create(name='开发部')
```

### 3. 创建组织管理员

```python
from assets.models import Asset
from orgs.models import Organization
from users.models import User
dev_org = Organization.objects.get(name='开发部')
user = User.objects.create(name='用户', username='user', email='user@jumpserver.org')
user.set_password('PassWord')
user.save()
dev_org.admins.add(user)
dev_org.users.add(user)
```

!!! tip "创建一个不存在的用户并设置为组织管理员"

### 4. 添加组织管理员

```python
from assets.models import Asset
from orgs.models import Organization
from users.models import User
dev_org = Organization.objects.get(name='开发部')
user = User.objects.get(username='admin')
dev_org.admins.add(user)
```

!!! tip "添加一个已经存在的用户并设置为组织管理员"

### 5. 往组织添加用户

```python
from assets.models import Asset
from orgs.models import Organization
from users.models import User
dev_org = Organization.objects.get(name='开发部')
user = User.objects.get(username='admin')
dev_org.users.add(user)
```

!!! tip "添加一个已经存在的用户到组织"
