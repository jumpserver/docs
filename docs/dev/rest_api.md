# API 文档

!!! info "API 文档默认已经集成在代码里面, 部署完成后可以通过下面的方式进行访问"

## API 访问

|  Version  |       Access method      |               example              |
| --------- | ------------------------ | ---------------------------------- |
|  < 2.0.0  |   `http://<url>/docs`    |   `http://192.168.244.144/docs`    |
|  >=2.0.0  | `http://<url>/api/docs/` | `http://192.168.244.144/api/docs/` |
|  >=2.6.0  | `http://<url>/api/docs/` | `http://192.168.244.144/api/docs/` |

!!! tip "版本小于 v2.6 需要打开 debug 模式"
    ```sh
    vi config.yml
    ```
    ```yaml
    ...
    # 如果版本更低的话，配置文件是 config.py
    # Debug = true
    DEBUG: true
    ```

![api_swagger](../img/api_swagger.jpg)

## API 认证

!!! tip "JumpServer API 支持的认证有以下几种方式"
    ```
    Session         登录后可以直接使用 session_id 作为认证方式  
    Token           获取一次性 Token，该 Token 有有效期, 过期作废  
    Private Token   永久 Token  
    Access Key      对 Http Header 进行签名
    ```

    === "Session"
        用户通过页面后登录，cookie 中会存在 sessionid, 请求时同样把 sessionid 放到 cookie 中
    === "Token"
        ```sh
        curl -X POST http://localhost/api/v1/authentication/auth/ \
             -H 'Content-Type: application/json' \
             -d '{"username": "admin", "password": "admin"}'
        ```
        ```python
        # pip install requests
        import requests, json

        jms_url = https://demo.jumpserver.org

        def get_token():
            url        = jms_url + '/api/v1/authentication/auth/'
            query_args = {
                "username": "admin",
                "password": "admin"
            }
            response = requests.post(url, data=query_args)
            return json.loads(response.text)['token']

        def get_user_info():
            url         = jms_url + '/api/v1/users/users/'
            token       = get_token()
            header_info = { "Authorization": 'Bearer ' + token }
            response    = requests.get(url, headers=header_info)
            print(json.loads(response.text))

        get_user_info()
        ```

    === "Private Token"
        ```sh
        docker exec -it jms_core /bin/bash
        cd /opt/jumpserver/apps
        python manage.py shell
        from users.models import User
        u = User.objects.get(username='admin')
        u.create_private_token()
        ```
        已经存在 private_token, 可以直接获取即可
        ```python
        u.private_token
        ```
        以 PrivateToken: 937b38011acf499eb474e2fecb424ab3 为例:
        ```sh
        curl -H 'Authorization: Token 937b38011acf499eb474e2fecb424ab3' \
             -H "Content-Type:application/json" http://demo.jumpserver.org/api/v1/users/users/
        ```
        ```python
        # pip install requests
        import requests, json

        jms_url   = https://demo.jumpserver.org
        jms_token = '937b38011acf499eb474e2fecb424ab3'

        def get_user_info():
            url         = jms_url + '/api/v1/users/users/'
            header_info = { "Authorization": 'Token ' + jms_token }
            response    = requests.get(url, headers=header_info)
            print(json.loads(response.text))

        get_user_info()
        ```

    === "Access Key"
        Access key 签名机制是为了安全， IETF 发布的法案 [详见此处](https://tools.ietf.org/html/draft-cavage-http-signatures-08)
        认证的原理是:

            用户有一个 access key, key有ID(keyId)和密钥(keySecret), 这个key是预生成的，请求者和服务器都知晓  

            用户请求时 将请求的 地址、请求方法、时间等使用 密钥(某种对称算法)进行加密，作为签名 连同 keyId 一同放到 header 中发给服务器
            Authorization: Signature keyId="Test",algorithm="rsa-sha256",
            signature="jKyvPcxB4JbmYY4mByyBY7cZfNl4OW9HpFQlG7N4YcJPteKTu4MW
            CLyk+gIr0wDgqtLWf9NLpMAMimdfsH7FSWGfbMFSrsVTHNTk0rK3usrfFnti1dx
            sM4jl0kYJCKTGI/UWkqiaxwNiKqGcdlEDrTcUhhsFsOIo8VhddmZTZ8w="

            服务器收到请求后，根据 keyId从数据库中取到keySecret, 解密签名，比对 签名内容和请求的字段是否一致，如果一致，认证成功，否则失败

        ```python
        # pip install requests drf-httpsig
        import requests, datetime
        from httpsig.requests_auth import HTTPSignatureAuth

        KEY_ID = 'AccessKeyID'
        SECRET = 'AccessKeySecret'
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

        signature_headers = ['(request-target)', 'accept', 'date']
        headers = {
            'Accept': 'application/json',
            'Date': datetime.datetime.utcnow().strftime(GMT_FORMAT)
        }

        auth = HTTPSignatureAuth(key_id=KEY_ID, secret=SECRET, algorithm='hmac-sha256', headers=signature_headers)
        req = requests.get('http://localhost/api/v1/users/users/', auth=auth, headers=headers)
        print(req.text)
        ```

## 示例

```python
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys, requests, time

class HTTP:
    server = None
    token = None

    @classmethod
    def get_token(cls, username, password):
        data              = {'username': username, 'password': password}
        url               = "/api/v1/authentication/auth/"
        res               = requests.post(cls.server + url, data)
        res_data          = res.json()
        if res.status_code in [200, 201] and res_data:
            token = res_data.get('token')
            cls.token = token
        else:
            print("获取 token 错误, 请检查输入项是否正确")
            sys.exit()

    @classmethod
    def get(cls, url, params=None, **kwargs):
        url               = cls.server + url
        headers           = {
            'Authorization': "Bearer {}".format(cls.token)
        }
        kwargs['headers'] = headers
        res               = requests.get(url, params, **kwargs)
        return res

    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        url               = cls.server + url
        headers           = {
            'Authorization': "Bearer {}".format(cls.token)
        }
        kwargs['headers'] = headers
        res               = requests.post(url, data, json, **kwargs)
        return res

class User(object):

    def __init__(self):
        self.id           = None
        self.name         = user_name
        self.username     = user_username
        self.email        = user_email

    def exist(self):
        url               = '/api/v1/users/users/'
        params            = {'username': self.username}
        res               = HTTP.get(url, params=params)
        res_data          = res.json()
        if res.status_code in [200, 201] and res_data:
            self.id       = res_data[0].get('id')
        else:
            self.create()

    def create(self):
        print("创建用户 {}".format(self.username))
        url               = '/api/v1/users/users/'
        data              = {
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'is_active': True
        }
        res               = HTTP.post(url, data)
        self.id           = res.json().get('id')

    def perform(self):
        self.exist()

class Node(object):

    def __init__(self):
        self.id           = None
        self.name         = asset_node_name

    def exist(self):
        url               = '/api/v1/assets/nodes/'
        params            = {'value': self.name}
        res               = HTTP.get(url, params=params)
        res_data          = res.json()
        if res.status_code in [200, 201] and res_data:
            self.id       = res_data[0].get('id')
        else:
            self.create()

    def create(self):
        print("创建资产节点 {}".format(self.name))
        url               = '/api/v1/assets/nodes/'
        data              = {
            'value': self.name
        }
        res               = HTTP.post(url, data)
        self.id           = res.json().get('id')

    def perform(self):
        self.exist()

class AdminUser(object):

    def __init__(self):
        self.id           = None
        self.name         = assets_admin_name
        self.username     = assets_admin_username
        self.password     = assets_admin_password

    def exist(self):
        url               = '/api/v1/assets/admin-user/'
        params            = {'username': self.name}
        res               = HTTP.get(url, params=params)
        res_data          = res.json()
        if res.status_code in [200, 201] and res_data:
            self.id       = res_data[0].get('id')
        else:
            self.create()

    def create(self):
        print("创建管理用户 {}".format(self.name))
        url               = '/api/v1/assets/admin-users/'
        data              = {
            'name': self.name,
            'username': self.username,
            'password': self.password
        }
        res               = HTTP.post(url, data)
        self.id           = res.json().get('id')

    def perform(self):
        self.exist()

class Asset(object):

    def __init__(self):
        self.id           = None
        self.name         = asset_name
        self.ip           = asset_ip
        self.platform     = asset_platform
        self.protocols    = asset_protocols
        self.admin_user   = AdminUser()
        self.node         = Node()

    def exist(self):
        url               = '/api/v1/assets/assets/'
        params            = {
            'hostname': self.name
        }
        res               = HTTP.get(url, params)
        res_data          = res.json()
        if res.status_code in [200, 201] and res_data:
            self.id       = res_data[0].get('id')
        else:
            self.create()

    def create(self):
        print("创建资产 {}".format(self.ip))
        self.admin_user.perform()
        self.node.perform()
        url               = '/api/v1/assets/assets/'
        data              = {
            'hostname': self.ip,
            'ip': self.ip,
            'platform': self.platform,
            'protocols': self.protocols,
            'admin_user': self.admin_user.id,
            'nodes': [self.node.id],
            'is_active': True
        }
        res               = HTTP.post(url, data)
        self.id           = res.json().get('id')

    def perform(self):
        self.exist()

class SystemUser(object):

    def __init__(self):
        self.id           = None
        self.name         = assets_system_name
        self.username     = assets_system_username

    def exist(self):
        url               = '/api/v1/assets/system-users/'
        params            = {'name': self.name}
        res               = HTTP.get(url, params)
        res_data          = res.json()
        if res.status_code in [200, 201] and res_data:
            self.id       = res_data[0].get('id')
        else:
            self.create()

    def create(self):
        print("创建系统用户 {}".format(self.name))
        url               = '/api/v1/assets/system-users/'
        data              = {
            'name': self.name,
            'username': self.username,
            'login_mode': 'auto',
            'protocol': 'ssh',
            'auto_push': True,
            'sudo': 'All',
            'shell': '/bin/bash',
            'auto_generate_key': True,
            'is_active': True
        }
        res               = HTTP.post(url, data)
        self.id           = res.json().get('id')

    def perform(self):
        self.exist()

class AssetPermission(object):

    def __init__(self):
        self.name         = perm_name
        self.user         = User()
        self.asset        = Asset()
        self.system_user  = SystemUser()

    def create(self):
        print("创建资产授权名称 {}".format(self.name))
        url               = '/api/v1/perms/asset-permissions/'
        data              = {
            'name': self.name,
            'users': [self.user.id],
            'assets': [self.asset.id],
            'system_users': [self.system_user.id],
            'actions': ['all'],
            'is_active': True,
            'date_start': perm_date_start,
            'date_expired': perm_date_expired
        }
        res               = HTTP.post(url, data)
        res_data          = res.json()
        if res.status_code in [200, 201] and res_data:
            print("创建资产授权规则成功: ", res_data)
        else:
            print("创建授权规则失败: ", res_data)

    def perform(self):
        self.user.perform()
        self.asset.perform()
        self.system_user.perform()
        self.create()

class APICreateAssetPermission(object):

    def __init__(self):
        self.jms_url      = jms_url
        self.username     = jms_username
        self.password     = jms_password
        self.token        = None
        self.server       = None

    def init_http(self):
        HTTP.server       = self.jms_url
        HTTP.get_token(self.username, self.password)

    def perform(self):
        self.init_http()
        self.perm         = AssetPermission()
        self.perm.perform()


if __name__ == '__main__':

    # jumpserver url 地址
    jms_url                = 'http://192.168.100.244'

    # 管理员账户
    jms_username           = 'admin'
    jms_password           = 'admin'

    # 资产节点
    asset_node_name        = 'test'

    # 资产信息
    asset_name             = '192.168.100.1'
    asset_ip               = '192.168.100.1'
    asset_platform         = 'linux'
    asset_protocols        = ['ssh/22']

    # 资产管理用户
    assets_admin_name      = 'test_root'
    assets_admin_username  = 'root'
    assets_admin_password  = 'test123456'

    # 资产系统用户
    assets_system_name     = 'test'
    assets_system_username = 'test'

    # 用户用户名
    user_name              = '测试用户'
    user_username          = 'test'
    user_email             = 'test@jumpserver.org'

    # 资产授权
    perm_name              = 'AutoPerm' +'_'+ (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    perm_date_start        = '2021-05-01 14:25:47 +0800'
    perm_date_expired      = '2021-06-01 14:25:47 +0800'

    api = APICreateAssetPermission()
    api.perform()
```
