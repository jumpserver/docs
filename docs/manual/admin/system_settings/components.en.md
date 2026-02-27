# Component Settings
!!! tip ""
    - Click the settings icon in the top right corner of the page to enter the **System Settings** page, then click **Component Settings** to access the component settings page.
    - The component settings page mainly configures JumpServer component information.

## 1 Basic Settings
!!! info "Note: Razor component and Magnus component are enterprise edition features"

!!! tip ""
    - Detailed parameters:

| Parameter Name         | Description                                                                 | Example or Default |
|------------------|----------------------------------------------------------------------|--------------|
| Component Registration         | Select the component registration method. Auto registration (valid 5 mins after JumpServer startup), enable, or disable. When deploying remote application publishing or extending JumpServer nodes, select enable to ensure component registration succeeds.                              | Enable         |
| Client Connection       | Allow connecting to KoKo component through SSH client                                 | Enable         |
| Password             | Allow users to log in to KoKo component through password authentication                                 | Enable         |
| SSH Public Key         | Allow users to log in to KoKo component through public key authentication                             | Enable         |
| Asset List Sorting     | Select asset list sorting method, sort by name or address                             | Name         |
| Assets Per Page | Set the number of assets displayed per page in the client connection command line type asset list                                     | 10           |
| Razor            | Enable Razor component for RDP client connection                               | Enable         |
| Magnus          | Enable Magnus component for database local client connection (e.g., Navicat, DBeaver, etc.)                             | Enable         |



## 2 Component List
!!! tip ""
    - The component list page allows you to view and manage all component registration information for JumpServer.
    - Click the **button** of a component to update the component's commands, storage, and recording storage. Session recordings are stored locally on the server by default; session commands are stored in the database by default. Here you can change session recording and session command storage to external storage. If you select **null**, no storage will be performed.

## 3 Component Monitoring
!!! tip ""
    - The component monitoring page allows you to view the load status and session count of all JumpServer components.

## 4 Service Endpoints

!!! tip ""
    - The service endpoints page mainly contains settings for access entry points. Service endpoints are the addresses (ports) for users to access services. When users connect to assets, they select service endpoints based on endpoint rules and asset tags as access entry points to establish connections, achieving distributed asset connection.
    
## 5 Endpoint Rules
!!! tip ""
    - For service endpoint selection strategy, currently two methods are supported: 1. Specify endpoints based on endpoint rules (current page); 2. Select endpoints through asset tags, with the fixed tag name being "endpoint" and the value being the endpoint name. The two methods prioritize tag matching first, since IP ranges may conflict. The tag method serves as a supplement to the rules. In endpoint rules, you set which IP ranges correspond to which service endpoints, and it also supports matching by domain.
