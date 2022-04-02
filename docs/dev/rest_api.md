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

            const (
                JmsServerURL = "https://demo.jumpserver.org"
                UserName = "admin"
                Password = "password"
            )

            func GetToken(jmsurl, username, password string) (string, error) {
                url := jmsurl + "/api/v1/authentication/auth/"
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

            func GetUserInfo(jmsurl, token string) {
                url := jmsurl + "/api/v1/users/users/"
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
                token, err := GetToken(JmsServerURL, UserName, Password)
                if err != nil {
                    log.Fatal(err)
                }
                GetUserInfo(JmsServerURL, token)
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
        curl http://demo.jumpserver.org/api/v1/users/users/ \
             -H 'Authorization: Token 937b38011acf499eb474e2fecb424ab3' \
             -H 'Content-Type: application/json' \
             -H 'X-JMS-ORG: 00000000-0000-0000-0000-000000000002'
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

            const (
                JmsServerURL = "https://demo.jumpserver.org"
                JMSToken = "adminToken"
            )

            func GetUserInfo(jmsurl, token string) {
                url := jmsurl + "/api/v1/users/users/"
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
                GetUserInfo(JmsServerURL, JMSToken)
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

            const (
                JmsServerURL = "https://demo.jumpserver.org"
                AccessKeyID = "f7373851-ea61-47bb-8357-xxxxxxxxxxx"
                AccessKeySecret = "d6ed1a06-66f7-4584-af18-xxxxxxxxxxxx"
            )

            type SigAuth struct {
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

            func GetUserInfo(jmsurl string, auth *SigAuth) {
                url := jmsurl + "/api/v1/users/users/"
                gmtFmt := "Mon, 02 Jan 2006 15:04:05 GMT"
                client := &http.Client{}
                req, err := http.NewRequest("GET", url, nil)
                req.Header.Add("Date", time.Now().Format(gmtFmt))
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
                json.MarshalIndent(body, "", "    ")
                fmt.Println(string(body))
            }

            func main() {
                auth := SigAuth{
                    KeyID:    AccessKeyID,
                    SecretID: AccessKeySecret,
                }
                GetUserInfo(JmsServerURL, &auth)
            }
            ```
