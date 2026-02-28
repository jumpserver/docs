# Web Assets
## 1 Overview
!!! tip ""
	- Web assets are a type of resource supported by JumpServer, designed to access web systems through remote applications. They are suitable for centralized management of internal systems, SaaS services, or other web-based applications.
	- Web assets depend on remote application publishers, which can be deployed on Windows or Linux systems.
	- When a user connects to a web asset, the system automatically invokes the publisher to launch a preconfigured browser for accessing the target system. This approach enables secure and controlled access, effectively preventing users from directly accessing the target address.


## 2 Create a web asset

!!! warning ""
    Before using Web-type assets, you must configure a remote application publisher. See [Remote Applications](../../system_settings/remote_apps.md) for detailed configuration.

!!! tip ""
    - Go to the **Console** page, click **Asset Management > Asset List** to open the asset list page.
    - Click the **Create** button in the top-left corner of the page, select **Web** type asset to open the asset creation page, and fill in the asset details.

!!! tip ""
    - Detailed parameter descriptions:

| Parameter | Description |
|-----------|-------------|
| Name | Required. The asset name in JumpServer, unrelated to the computer name; must be unique |
| IP/Hostname | Required. The real address of the web page, supporting domain names and IP addresses. Duplicates are allowed. If the port is not 80 or 443, include the port number. |
| Asset Platform | Default. The asset platform for Web-type assets |
| Node | Required. The node to which the asset belongs |
| Selector | Required. Select the auto-fill mode. See [Auto-fill](#3) in this document for detailed configuration |
| Protocol | Default. Default HTTP/HTTPS protocol |
| Account List | Optional. Accounts used to log in to the asset; multiple accounts can be created. Accounts are bound to assets. |
| Domain | Optional. For assets across network segments, access through a network gateway as a proxy is required. **Web assets do not support gateways by default; this option only serves to annotate gateway machine information** |
| Label | Optional. Add labels to the asset for easier management. Web assets also support specifying specific remote app publishers through labels. |
| Active | Required. Whether the asset is available for use |
| Note | Optional. Description of the asset information |

## 3 Auto-fill

!!! tip ""
	- The auto-fill feature is mainly used for websites that require user authentication. Before users access such websites, JumpServer automatically fills in predefined usernames and passwords on the login page to complete authentication. This process is transparent to users without requiring manual credential entry.

### 3.1 Disable auto-fill

!!! tip ""
	- This method applies to websites that do not require authentication.

### 3.2 Basic auto-fill

!!! tip ""
	- This method applies to websites where the username, password, and login button are all on the same page. JumpServer automatically fills in the credentials and submits the form to authenticate the user.

	- When filling in information automatically, **you need to locate elements on the web page**. Supported selector types include name selectors, ID selectors, class selectors, CSS selectors, and XPath selectors. For more information, see [Selenium Python: Locating Elements](https://selenium-python.readthedocs.io/locating-elements.html).

### 3.3 Script auto-fill
!!! tip ""
	- This script method applies to websites with complex login procedures. It supports advanced automation, including multi-step authentication and interaction with dynamic page elements.

### 3.3.1 Script structure
!!! tip ""
	- The script is an array where each element is a dictionary representing a step in the script.

	- Syntax explanation:
	
| Step | Description |
| :------ | :----------------------------------------------------------- |
| step | Required.<br/>Integer.<br/>Indicates the execution order of the script, starting from 1 and incrementing |
| value | Required.<br/>String.<br/>Supported built-in variables: {USERNAME}, {SECRET}.<br/>If the command is not of type, leave the value empty |
| target | Required.<br/>String.<br/>The target element to act on, can be a selector or XPath expression |
| command | Required.<br/>String.<br/>The command to execute, can be one of: click, type, sleep, select_frame |

| Action | Description |
| :----------- | :----------------------------------------------------------- |
| click | Click the target element |
| type | Type the value in the target element |
| sleep | Pause the script for a specified duration, usually to allow page loading during navigation. Duration is specified by the target, in seconds |
| select_frame | Switch to the specified iframe for action.<br/>Target supports options like id=iframe_id, name=iframe_name, or index=1 (if index < 0, switch back to the default/main iframe) |

### 3.3.2 Script example

```json
[  
	// Switch to the iframe with id=iframe_id.
	{      
		"step": 1,      
		"command": "select_frame",      
		"target": "id=iframe_id",      
		"value": ""  
	},  
	// Type username in the input field name=username.
	// When the script is executed, the {USERNAME} variable will be replaced with the actual username.
	{      
		"step": 2,      
		"command": "type",      
		"target": "name=username",      
		"value": "{USERNAME}"  
	},  
	// Click the next button to proceed to the next step of the login process.
	{      
		"step": 3,      
		"command": "click",      
		"target": "id=next_button",      
		"value": ""  
	},  
	// Pause the script for 5 seconds to allow the next page to load.
	{      
		"step": 4,      
		"command": "sleep",      
		"target": "5",      
		"value": ""  
	},  
	// Type password in the input field name=password.
	// When the script is executed, the {SECRET} variable will be replaced with the actual password.
	{      
		"step": 5,      
		"command": "type",      
		"target": "name=password",      
		"value": "{SECRET}"  
	},  
	// Click the submit button to complete the login process.
	{      
		"step": 6,      
		"command": "click",      
		"target": "id=submit_button",      
		"value": ""  
	}
]
```
