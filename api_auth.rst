API 认证
==========================

Jumpserver Api 支持的认证有以下几种方式:

- Session 登录后可以直接使用session_id作为认证方式
- Token 获取一次性Token，该Token有有效期, 过期作废
- Private Token 永久Token
- Access Key签名 对Http Header进行签名


Session
------------------------

用户通过页面后登录，cookie中会存在 sessionid, 请求时同样把sessionid放到 cookie中

Token
------------------------

使用账号密码调用 Api获取token，如果启用了MFA，则需要两步验证


.. code-block:: shell

    $ curl -X POST http://localhost/api/v1/users/auth/ -H 'Content-Type: application/json' -d '{"username": "admin", "password": "admin"}'  # 获取token
    {"token":"937b38011acf499eb474e2fecb424ab3"}  # 获取到的token

    # 如果开启了 MFA, 则返回的是 seed, 需要携带 seed 和 otp_code 再次提交一次才能获取到 token
    $ curl -X POST http://localhost/api/v1/users/auth/ -H 'Content-Type: application/json' -d '{"username": "admin", "password": "admin"}'
    {"code":101, "msg":"请携带seed值, 进行MFA二次认证", "otp_url":"/api/users/v1/otp/auth/", "seed":"629ba0935a624bd9b21e31c19e0cc8cb"}
    $ curl -X POST http://localhost/api/v1/users/otp/auth/ -H 'Content-Type: application/json' -H 'cache-control: no-cache' -d '{"seed": "629ba0935a624bd9b21e31c19e0cc8cb", "otp_code": "202123"}'
    {"token":"937b38011acf499eb474e2fecb424ab3"}
    # otp_code 为动态密码

    $ curl -H 'Authorization: Bearer 937b38011acf499eb474e2fecb424ab3' -H "Content-Type:application/json" http://localhost/api/v1/users/users/
    # 使用token访问, token有效期 1小时


Private Token
------------------------

由于Private token是永久的，为了安全，页面没有生成的方式，必须通过命令行来创建

.. code-block:: shell

    $ source /opt/py3/bin/activate
    $ cd /opt/jumpserver/apps
    $ python manage.py shell
    >>> from users.models import User
    >>> u = User.objects.get(username='admin')
    >>> u.create_private_token()
    937b38011acf499eb474e2fecb424ab3

    # 如果生成报错, 表示已经存在 private_token, 直接获取即可
    >>> u.private_token
    <PrivateToken: 937b38011acf499eb474e2fecb424ab3>
    # 937b38011acf499eb474e2fecb424ab3 就是

    $ curl -H 'Authorization: Token 937b38011acf499eb474e2fecb424ab3' -H "Content-Type:application/json" http://localhost/api/v1/users/users/


Access Key 签名
--------------------
Access key 签名机制是为了安全， IETF 发布的法案 `详见 <https://tools.ietf.org/html/draft-cavage-http-signatures-08>`_

认证的原理是：

1. 用户有一个 access key, key有ID(keyId)和密钥(keySecret), 这个key是预生成的，请求者和服务器都知晓
2. 用户请求时 将请求的 地址、请求方法、时间等使用 密钥(某种对称算法)进行加密，作为签名 连同 keyId 一同放到header中发给服务器: 如

.. code-block:: shell

   Authorization: Signature keyId="Test",algorithm="rsa-sha256",
   signature="jKyvPcxB4JbmYY4mByyBY7cZfNl4OW9HpFQlG7N4YcJPteKTu4MW
   CLyk+gIr0wDgqtLWf9NLpMAMimdfsH7FSWGfbMFSrsVTHNTk0rK3usrfFnti1dx
   sM4jl0kYJCKTGI/UWkqiaxwNiKqGcdlEDrTcUhhsFsOIo8VhddmZTZ8w="


3. 服务器收到请求后，根据 keyId从数据库中取到keySecret, 解密签名，比对 签名内容和请求的字段是否一致，如果一致，认证成功，否则失败


python 使用requests请求:

.. code-block:: shell

    $ pip install requests drf-httpsig
    $ python


.. code-block:: python

    import requests
    from httpsig.requests_auth import HTTPSignatureAuth

    KEY_ID = 'su-key'
    SECRET = 'my secret string'

    signature_headers = ['(request-target)', 'accept', 'date', 'host']
    headers = {
      'Accept': 'application/json',
      'Date': "Mon, 17 Feb 2014 06:11:05 GMT"
    }

    auth = HTTPSignatureAuth(key_id=KEY_ID, secret=SECRET,
                           algorithm='hmac-sha256',
                           headers=signature_headers)
    req = requests.get('http://localhost/api/v1/users/users/',
                     auth=auth, headers=headers)
    print(req.content)





代码示例
--------------------------

.. code-block:: python

    import requests
    import json
    from pprint import pprint

    def get_token():

        url = 'https://demo.jumpserver.org/api/v1/users/auth/'

        query_args = {
            "username": "admin",
            "password": "admin"
        }

        response = requests.post(url, data=query_args)

        return json.loads(response.text)['token']

    def get_user_info():

        url = 'https://demo.jumpserver.org/api/v1/users/users/'

        token = get_token()

        header_info = { "Authorization": 'Bearer ' + token }

        response = requests.get(url, headers=header_info)

        pprint(json.loads(response.text))

    get_user_info()
