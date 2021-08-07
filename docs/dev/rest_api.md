# API 文档

!!! info "API 文档默认已经集成在代码里面，部署完成后可以通过下面的方式进行访问"

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
        用户通过页面后登录，cookie 中会存在 sessionid，请求时同样把 sessionid 放到 cookie 中

    === "Token"
        ```sh
        curl -X POST http://localhost/api/v1/authentication/auth/ \
             -H 'Content-Type: application/json' \
             -d '{"username": "admin", "password": "admin"}'
        ```
        === "Python"
            ```python
            # Python 示例
            # pip install requests
            import requests, json

            def get_token(jms_url, username, password):
                url = jms_url + '/api/v1/authentication/auth/'
                query_args = {
                    "username": username,
                    "password": password
                }
                response = requests.post(url, data=query_args)
                return json.loads(response.text)['token']

            def get_user_info(jms_url, token):
                url = jms_url + '/api/v1/users/users/'
                headers = {
                    "Authorization": 'Bearer ' + token,
                    'X-JMS-ORG': '00000000-0000-0000-0000-000000000002'
                }
                response = requests.get(url, headers=headers)
                print(json.loads(response.text))

            if __name__ == '__main__':
                jms_url = 'https://demo.jumpserver.org'
                username = 'admin'
                password = 'admin'
                token = get_token(jms_url, username, password)
                get_user_info(jms_url, token)
            ```

        === "Golang"
            ```go
            // Golang 示例
            package main

            import (
                "encoding/json"
                "fmt"
                "io/ioutil"
                "log"
                "net/http"
                "strings"
            )

            func GetToken(jms_url, username, password string) (string, error) {
                url := jms_url + "/api/v1/authentication/auth/"
                query_args := strings.NewReader(`{
                    "username": "`+username+`",
                    "password": "`+password+`"
                }`)
                client := &http.Client{}
                req, err := http.NewRequest("POST", url, query_args)
                req.Header.Add("Content-Type", "application/json")
                resp, err := client.Do(req)
                if err != nil {
                    log.Fatal(err)
                }
                defer resp.Body.Close()
                body, err := ioutil.ReadAll(resp.Body)
                if err != nil {
                    log.Fatal(err)
                }
                response := map[string]interface{}{}
                json.Unmarshal(body, &response)
                return response["token"].(string), nil
            }

            func GetUserInfo(jms_url, token string) {
                url := jms_url + "/api/v1/users/users/"
                client := &http.Client{}
                req, err := http.NewRequest("GET", url, nil)
                req.Header.Add("Authorization", "Bearer "+token)
                req.Header.Add("X-JMS-ORG", "00000000-0000-0000-0000-000000000002")
                resp, err := client.Do(req)
                if err != nil {
                    log.Fatal(err)
                }
                defer resp.Body.Close()
                body, err := ioutil.ReadAll(resp.Body)
                if err != nil {
                    log.Fatal(err)
                }
                fmt.Println(string(body))
            }

            func main() {
                jms_url := "https://demo.jumpserver.org"
                username := "admin"
                password := "admin"
                token, err := GetToken(jms_url, username, password)
                if err != nil {
                    log.Fatal(err)
                }
                GetUserInfo(jms_url, token)
            }
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
        已经存在 private_token，可以直接获取即可
        ```python
        u.private_token
        ```
        以 PrivateToken: 937b38011acf499eb474e2fecb424ab3 为例:
        ```sh
        curl -H 'Authorization: Token 937b38011acf499eb474e2fecb424ab3' \
             -H "Content-Type:application/json" http://demo.jumpserver.org/api/v1/users/users/
        ```
        === "Python"
            ```python
            # Python 示例
            # pip install requests
            import requests, json

            def get_user_info(jms_url, token):
                url = jms_url + '/api/v1/users/users/'
                headers = {
                    "Authorization": 'Token ' + token,
                    'X-JMS-ORG': '00000000-0000-0000-0000-000000000002'
                }
                response = requests.get(url, headers=headers)
                print(json.loads(response.text))

            if __name__ == '__main__':
                jms_url = 'https://demo.jumpserver.org'
                token = '937b38011acf499eb474e2fecb424ab3'
                get_user_info(jms_url, token)
            ```

        === "Golang"
            ```go
            // Golang 示例
            package main

            import (
                "encoding/json"
                "fmt"
                "io/ioutil"
                "log"
                "net/http"
                "strings"
            )

            func GetUserInfo(jms_url, token string) {
                url := jms_url + "/api/v1/users/users/"
                client := &http.Client{}
                req, err := http.NewRequest("GET", url, nil)
                req.Header.Add("Authorization", "Token "+token)
                req.Header.Add("X-JMS-ORG", "00000000-0000-0000-0000-000000000002")
                resp, err := client.Do(req)
                if err != nil {
                    log.Fatal(err)
                }
                defer resp.Body.Close()
                body, err := ioutil.ReadAll(resp.Body)
                if err != nil {
                    log.Fatal(err)
                }
                fmt.Println(string(body))
            }

            func main() {
                jms_url := "https://demo.jumpserver.org"
                token := "937b38011acf499eb474e2fecb424ab3"
                GetUserInfo(jms_url, token)
            }
            ```

    === "Access Key"
        在 Web 页面 API Key 列表创建或获取 AccessKeyID AccessKeySecret
        === "Python"
            ```python
            # Python 示例
            # pip install requests drf-httpsig
            import requests, datetime, json
            from httpsig.requests_auth import HTTPSignatureAuth

            def get_auth(KeyID, SecretID):
                signature_headers = ['(request-target)', 'accept', 'date']
                auth = HTTPSignatureAuth(key_id=KeyID, secret=SecretID, algorithm='hmac-sha256', headers=signature_headers)
                return auth

            def get_user_info(jms_url, auth):
                url = jms_url + '/api/v1/users/users/'
                gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
                headers = {
                    'Accept': 'application/json',
                    'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
                    'Date': datetime.datetime.utcnow().strftime(gmt_form)
                }

                response = requests.get(url, auth=auth, headers=headers)
                print(json.loads(response.text))

            if __name__ == '__main__':
                jms_url = 'https://demo.jumpserver.org'
                KeyID = 'AccessKeyID'
                SecretID = 'AccessKeySecret'
                auth = get_auth(KeyID, SecretID)
                get_user_info(jms_url, auth)
            ```

        === "Golang"
            ```go
            // Golang 示例
            package main

            import (
                "fmt"
                "io/ioutil"
                "log"
                "net/http"
                "time"
                "gopkg.in/twindagger/httpsig.v1"
            )

            type SigAuth string {
                KeyID    string
                SecretID string
            }

            func (auth *SigAuth) Sign(r *http.Request) error {
                headers := []string{"(request-target)", "date"}
                signer, err := httpsig.NewRequestSigner(auth.KeyID, auth.SecretID, "hmac-sha256")
                if err != nil {
                    return err
                }
                return signer.SignRequest(r, headers, nil)
            }

            func GetUserInfo(jms_url string, auth *SigAuth) {
                url := jms_url + "/api/v1/users/users/"
                gmt_fmt := "Mon, 02 Jan 2006 15:04:05 GMT"
                client := &http.Client{}
                req, err := http.NewRequest("GET", url, nil)
                req.Header.Add("Date", time.Now().Format(gmt_fmt))
                req.Header.Add("Accept", "application/json")
                req.Header.Add("X-JMS-ORG", "00000000-0000-0000-0000-000000000002")
                if err != nil {
                    log.Fatal(err)
                }
                if err := auth.Sign(req); err != nil {
                    log.Fatal(err)
                }
                resp, err := client.Do(req)
                if err != nil {
                    log.Fatal(err)
                }
                defer resp.Body.Close()
                body, err := ioutil.ReadAll(resp.Body)
                if err != nil {
                    log.Fatal(err)
                }
                fmt.Println(string(body))
            }

            func main() {
                jms_url := "https://demo.jumpserver.org"
                auth := SigAuth{
                    KeyID:    "AccessKeyID",
                    SecretID: "AccessKeySecret",
                }
                GetUserInfo(jms_url, &auth)
            }
            ```


## 示例

=== "Token"
    ```python
    #!/usr/bin/env python3
    # -*- coding:utf-8 -*-

    import sys, requests, time

    class HTTP:
        server = None
        token  = None

        @classmethod
        def get_token(cls, username, password):
            data              = {'username': username, 'password': password}
            url               = "/api/v1/authentication/auth/"
            res               = requests.post(cls.server + url, data)
            res_data          = res.json()
            if res.status_code in [200, 201] and res_data:
                token         = res_data.get('token')
                cls.token     = token
            else:
                print("获取 token 错误, 请检查输入项是否正确")
                sys.exit()

        @classmethod
        def get(cls, url, params=None, **kwargs):
            url               = cls.server + url
            headers           = {
                'Authorization': "Bearer {}".format(cls.token),
                'X-JMS-ORG': '00000000-0000-0000-0000-000000000002'
            }
            kwargs['headers'] = headers
            res               = requests.get(url, params, **kwargs)
            return res

        @classmethod
        def post(cls, url, data=None, json=None, **kwargs):
            url               = cls.server + url
            headers           = {
                'Authorization': "Bearer {}".format(cls.token),
                'X-JMS-ORG': '00000000-0000-0000-0000-000000000002'
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
        asset_platform         = 'Linux'
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

=== "Access Key"
    ```python
    #!/usr/bin/env python3
    # -*- coding:utf-8 -*-

    import sys, requests, time, datetime
    from httpsig.requests_auth import HTTPSignatureAuth

    class HTTP:
        server = None
        auth   = None

        @classmethod
        def get_auth(cls, accesskeyid, accesskeysecret):
            signature_headers = ['(request-target)', 'accept', 'date']
            auth              = HTTPSignatureAuth(key_id=accesskeyid, secret=accesskeysecret, algorithm='hmac-sha256', headers=signature_headers)
            cls.auth          = auth

        @classmethod
        def get(cls, url, params=None, **kwargs):
            url               = cls.server + url
            GMT_FORMAT        = '%a, %d %b %Y %H:%M:%S GMT'
            headers           = {
                'Accept': 'application/json',
                'Date': datetime.datetime.utcnow().strftime(GMT_FORMAT)
            }
            kwargs['auth']    = cls.auth
            kwargs['headers'] = headers
            res               = requests.get(url, params, **kwargs)
            return res

        @classmethod
        def post(cls, url, data=None, json=None, **kwargs):
            url               = cls.server + url
            GMT_FORMAT        = '%a, %d %b %Y %H:%M:%S GMT'
            headers           = {
                'Accept': 'application/json',
                'Date': datetime.datetime.utcnow().strftime(GMT_FORMAT)
            }
            kwargs['auth']    = cls.auth
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            res               = HTTP.post(url, json=data)
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
            self.jms_url         = jms_url
            self.accesskeyid     = jms_accesskeyid
            self.accesskeysecret = jms_accesskeysecret
            self.auth            = None
            self.server          = None

        def init_http(self):
            HTTP.server          = self.jms_url
            HTTP.get_auth(self.accesskeyid, self.accesskeysecret)

        def perform(self):
            self.init_http()
            self.perm            = AssetPermission()
            self.perm.perform()


    if __name__ == '__main__':

        # jumpserver url 地址
        jms_url                = 'http://192.168.100.244'

        # 管理员 AK SK
        jms_accesskeyid        = ''
        jms_accesskeysecret    = ''

        # 资产节点
        asset_node_name        = 'test'

        # 资产信息
        asset_name             = '192.168.100.1'
        asset_ip               = '192.168.100.1'
        asset_platform         = 'Linux'
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
