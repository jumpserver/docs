# 数据解密

=== "系统用户"
    !!! tip ""
        ```sh
        docker exec -it jms_core bash
        cd /opt/jumpserver/apps
        python manage.py shell
        ```
        ```python
        from assets.models import SystemUser
        # 81aef7ac-e432-4d1b-aaf5-a3bc37c2b230 为你要查询系统用户的 id, 在 web 页面的系统用户详情里面有该字段
        u = SystemUser.objects.get(id='81aef7ac-e432-4d1b-aaf5-a3bc37c2b230')
        ```
        ```python
        u.password
        ```
        ```nginx
        Out[4]: 'YVo87b+AvwpnAX2igWRTHdAlP0hL'
        ```
        ```python
        u.private_key
        ```
        ```nginx
        Out[6]: '-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEAxg4C1KKD5mz+3arCKETugJggR4HzEvIjAutKv+zZwAYm5SbB
        3IGXoEzdXbk/9u1btyTGbmTpKubsJh5MeGlHWExqzA2n9NsC/3hYenjwm1OP1Vhc
        bGZYnZTqbUGTiWiRhtXUCOC2yzgSdLiCLGS5XdIVEhCO3AvWZCvauhEQYu3PLlUN
        Xuc7JZBLGrZ+YVo87b+AvwpnAX2igWRTHdAlP0hL+MWoN3lzba90Jox1zJNeyZ64
        M/u1TsiMGGWs/H35SqpH9jerCl5+1Mqw5oryidYApuNOilN8ucYa6XDueweEXkHk
        oY8QxwaC8GFLZErb0Ov8lzEhlpALsCYgekiecQIDAQABAoIBAQC5W/OaPl9kES6X
        F3GPbrQo9jd/tUdhu+y4lq3m4i0JYriUTqmxTjgydr3XMcGDwLHNvkVYnGj9FhJ9
        um2nZCC5qwto3n8K1s8DegaU2QuXLX64FXKqoT8efLjKeE00lQFeSFGh3W4208uy
        Idzy33H9NNkzhvutRgboyYJ0EfRcIL/wyxc0ndMKt/bVYH8T14aWViVRF7OyiIkd
        eFx7tdnVscBSujNX027ycmjElwRf9TPNFUFwF5XGf3xwWjPmBNWr91XxPcF9VecG
        gyd9qxNd12YYGcX4SR6V0p+36Av+rZoHB0405b/ZncmevSStUCu6fTtQYwdCZj0p
        PgTradABAoGBAOVjCRleXfO9OVc4Y7sM2+1i/So5dmp66foC76j6CDKzztA2b5FX
        tduNhoObeNYdnV32WvW3/xXcFWFnbWf0Eymx2DMuxMfWlTvM0InParq0TpeVMWMP
        uxW+7YNZ9IWuuLMs3jfY1lRQBUgVlcb0zA7tjWZO/n/mKW5Fd2rItvmRAoGBAN0I
        YzFGEPoKgGqYme58KpebM1jt1XoyLtbH1ygRvaPlnLfPDBsBhrqLCyR3+oK0kFlM
        f7Neqo86hCQ/aqVC1lMu2o3htg52b1Mj2T0YUTNsPTwx+8lHciRnqJZytHRjwfFC
        4UySAzWKDDQZcIQGTAsdoXngkAZFITMBZBdRz+bhAoGAfytphvvvIEq+eGFVwQR/
        BNtFOVyEDsI35xgrn8WGN/3BYWNcdPpoYuDSOzI9So8+iDIk+WbZb1gFLmv1lpUU
        7p+fGbkK9TM8ptuEnXI1XG7Lx3O53o6BDKw95vz+98IGuabdR57aLAH0+6Kj15ot
        avU92ANhSqziOTUf4D6IWlECgYAe+kr0n+5HLOuchPCl9O7/Ongy0Xpm2tunrHBi
        JEJg0xBoznLS5h7gzBXusYYBhY7phQgsumrLEhdtARpQORa/Q8TLt8ONOVoW2+JZ
        ZqwSuevHIPY52nKL2Z9OHptd6JFI3+e1lI0wlr1pG9uiFUPZFvkHnMpypoOlo19E
        yWmK4QKBgQCVmBTLSA+M3WJqDBK2Z6lUaDCaAjwn2Q5RSq2B/lLjzaod6WYWyecY
        NASeo6CC4fxOCfMJN1DT5CLyW4XpRk3GeR4QKSfFkwD2yRqk+7opm8PppdMuLZKU
        LQMMI90AWvU3Cx9aAbl1bLSIT0qRoc5FGwmLEL12yDBZA2l3vYhnaw==
        -----END RSA PRIVATE KEY-----'
        ```

=== "指定资产的系统用户"
    !!! tip ""
        ```sh
        docker exec -it jms_core bash
        cd /opt/jumpserver/apps
        python manage.py shell
        ```
        ```python
        from assets.models import SystemUser, Asset
        # 81aef7ac-e432-4d1b-aaf5-a3bc37c2b230 为你要查询系统用户的 id, 在 web 页面的系统用户详情里面有该字段
        user = SystemUser.objects.get(id='81aef7ac-e432-4d1b-aaf5-a3bc37c2b230')

        # 5ae0c750-91e3-4a32-81d3-6576068b74f3 为要查询资产的 id, 资产列表的资产详情里面有
        asset = Asset.objects.get(id='5ae0c750-91e3-4a32-81d3-6576068b74f3')

        # 切换到系统用户的组织
        user.org.change_to()
        u = user.get_asset_user(asset)
        ```
        ```python
        u.password
        ```
        ```nginx
        Out[7]: 'YVo87b+AvwpnAX2igWRTHdAlP0hL'
        ```
        ```python
        u.private_key
        ```
        ```nginx
        Out[9]: '-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEAxg4C1KKD5mz+3arCKETugJggR4HzEvIjAutKv+zZwAYm5SbB
        3IGXoEzdXbk/9u1btyTGbmTpKubsJh5MeGlHWExqzA2n9NsC/3hYenjwm1OP1Vhc
        bGZYnZTqbUGTiWiRhtXUCOC2yzgSdLiCLGS5XdIVEhCO3AvWZCvauhEQYu3PLlUN
        Xuc7JZBLGrZ+YVo87b+AvwpnAX2igWRTHdAlP0hL+MWoN3lzba90Jox1zJNeyZ64
        M/u1TsiMGGWs/H35SqpH9jerCl5+1Mqw5oryidYApuNOilN8ucYa6XDueweEXkHk
        oY8QxwaC8GFLZErb0Ov8lzEhlpALsCYgekiecQIDAQABAoIBAQC5W/OaPl9kES6X
        F3GPbrQo9jd/tUdhu+y4lq3m4i0JYriUTqmxTjgydr3XMcGDwLHNvkVYnGj9FhJ9
        um2nZCC5qwto3n8K1s8DegaU2QuXLX64FXKqoT8efLjKeE00lQFeSFGh3W4208uy
        Idzy33H9NNkzhvutRgboyYJ0EfRcIL/wyxc0ndMKt/bVYH8T14aWViVRF7OyiIkd
        eFx7tdnVscBSujNX027ycmjElwRf9TPNFUFwF5XGf3xwWjPmBNWr91XxPcF9VecG
        gyd9qxNd12YYGcX4SR6V0p+36Av+rZoHB0405b/ZncmevSStUCu6fTtQYwdCZj0p
        PgTradABAoGBAOVjCRleXfO9OVc4Y7sM2+1i/So5dmp66foC76j6CDKzztA2b5FX
        tduNhoObeNYdnV32WvW3/xXcFWFnbWf0Eymx2DMuxMfWlTvM0InParq0TpeVMWMP
        uxW+7YNZ9IWuuLMs3jfY1lRQBUgVlcb0zA7tjWZO/n/mKW5Fd2rItvmRAoGBAN0I
        YzFGEPoKgGqYme58KpebM1jt1XoyLtbH1ygRvaPlnLfPDBsBhrqLCyR3+oK0kFlM
        f7Neqo86hCQ/aqVC1lMu2o3htg52b1Mj2T0YUTNsPTwx+8lHciRnqJZytHRjwfFC
        4UySAzWKDDQZcIQGTAsdoXngkAZFITMBZBdRz+bhAoGAfytphvvvIEq+eGFVwQR/
        BNtFOVyEDsI35xgrn8WGN/3BYWNcdPpoYuDSOzI9So8+iDIk+WbZb1gFLmv1lpUU
        7p+fGbkK9TM8ptuEnXI1XG7Lx3O53o6BDKw95vz+98IGuabdR57aLAH0+6Kj15ot
        avU92ANhSqziOTUf4D6IWlECgYAe+kr0n+5HLOuchPCl9O7/Ongy0Xpm2tunrHBi
        JEJg0xBoznLS5h7gzBXusYYBhY7phQgsumrLEhdtARpQORa/Q8TLt8ONOVoW2+JZ
        ZqwSuevHIPY52nKL2Z9OHptd6JFI3+e1lI0wlr1pG9uiFUPZFvkHnMpypoOlo19E
        yWmK4QKBgQCVmBTLSA+M3WJqDBK2Z6lUaDCaAjwn2Q5RSq2B/lLjzaod6WYWyecY
        NASeo6CC4fxOCfMJN1DT5CLyW4XpRk3GeR4QKSfFkwD2yRqk+7opm8PppdMuLZKU
        LQMMI90AWvU3Cx9aAbl1bLSIT0qRoc5FGwmLEL12yDBZA2l3vYhnaw==
        -----END RSA PRIVATE KEY-----'
        ```
