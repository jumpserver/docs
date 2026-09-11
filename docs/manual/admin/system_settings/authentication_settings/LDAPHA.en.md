# LDAP HA Authentication

## About LDAP HA

!!! info "Note: LDAP HA authentication is an enterprise feature of JumpServer."

!!! tip ""
    - Click the gear icon in the top-right corner to enter the **System Settings** page, then click **Authentication Settings > LDAP HA** to open the LDAP HA configuration page.
    - In JumpServer, LDAP HA integration typically ensures that when the primary LDAP server fails, the system automatically switches to a backup LDAP HA server, ensuring continuity of authentication services. Thus, even if the LDAP server encounters problems, JumpServer can continue processing user authentication requests without causing downtime or service interruption.

## Basic Configuration

!!! tip ""
    - Click the settings button in the top-right corner
    - Navigate to **System Settings > Authentication Settings > LDAP HA**
    - In the **Server Address** field, enter the LDAP HA server URL, such as "ldap://example.com:389" and "ldaps://example.com:636".

!!! info ""
    - To configure LDAP TLS certificates, upload `ldap_ca.pem`, `ldap_cert.pem`, and `ldap_cert.key` files to the JumpServer `/opt/jumpserver/config/certs` directory, then restart JumpServer using the command `jmsctl restart`.

!!! tip ""
    - In the **Bind DN** field, enter a user DN with at least query permissions; this permission will be used to query and filter users, for example "cn=admin,dc=example,dc=com".
    - In the **Mapped Attributes** field, enter user attribute mapping. The key represents JumpServer user attribute name (available options: name, username, email, is_active, groups, phone, comment), and the value corresponds to LDAP HA user attribute name.

```json
{
    "name": "sAMAccountName",
    "username": "cn",
    "email": "mail",
    "is_active": "useraccountcontrol",
    "phone": "telephoneNumber",
    "groups": "memberof"
}
```

## Test LDAP HA Connection

!!! tip ""
    - Click the settings button in the top-right corner
    - Navigate to **System Settings > Authentication Settings > LDAP HA**
    - Scroll to the bottom of the page
    - Click **Test Connection**

## Test LDAP Login

!!! tip ""
    - Click the settings button in the top-right corner
    - Navigate to **System Settings > Authentication Settings > LDAP HA**
    - Ensure LDAP HA configuration has been successfully completed and tested
    - Scroll to the bottom of the page
    - Click **Test Login**
    - Enter LDAP user's username and password in the popup window
    - Click **Confirm**

## Import LDAP Users

!!! tip ""
    - Click the settings button in the top-right corner
    - Navigate to **System Settings > Authentication Settings > LDAP HA**
    - Ensure LDAP HA configuration has been successfully completed and tested
    - Scroll to the bottom of the page
    - Click **User Import**
    - In the popup window, click **Sync Users** to synchronize LDAP HA users to the list
    - Select users to import and click **Import** to proceed; or click **Import All** to import all users
