# Account List
## 1 Overview
!!! tip "" 
    - Go to the Console page, click **Account Management > Account List** to open the account list page.
    - JumpServer supports managed account management for assets.

## 2 Features
### 2.1 View account information
!!! tip "" 
    - Click the asset tree or type tree on the left side of the page to select a node or asset to view the account information associated with the asset (by default, admin MFA verification is required)
![account_list_01](../../../../img/v4_account_list_01.png)
!!! tip "Hint"
    - MFA verification is required to view detailed account information such as account passwords.
    - For security, JumpServer defaults to requiring MFA verification to view passwords. To disable MFA verification, add the configuration `SECURITY_VIEW_AUTH_NEED_MFA=False` to the JumpServer configuration file (default: `/opt/jumpserver/config/config.txt`) and restart the JumpServer service.
### 2.2 Account information import/export
!!! tip "" 
    - You can bulk export account information. JumpServer supports exporting detailed information and passwords of all accounts associated with assets. Account filtering can quickly filter the account list based on account type and risk accounts.
![account_list_02](../../../../img/v4_account_list_02.png)
### 2.3 Add account
!!! tip "" 
    - JumpServer supports bulk associating one account with multiple assets (account adding feature). Click the **Add** button on the account list page, select the assets to associate with the account, fill in the account details, and bulk associate the account with the assets.
![account_list_03](../../../../img/v4_account_list_03.png)
### 2.4 Add account template
!!! tip "" 
    - Click the **Template Add** button on the account list page, select the assets to associate the account template with, choose the account template to add, and bulk associate the account template with the assets.
![account_list_04](../../../../img/v4_account_list_04.png)

## 3 Virtual accounts
!!! tip "" 
    - In certain scenarios during authorization rule creation, virtual accounts are used to log in to assets. The virtual account page supports viewing details of virtual accounts. JumpServer supports allowing AD/LDAP users to log in to assets with JumpServer user passwords when authorization rules authorize accounts with the same name.
![account_list_05](../../../../img/v4_account_list_05.png)
