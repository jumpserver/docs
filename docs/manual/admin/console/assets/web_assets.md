# 创建 Web 资产
!!! tip ""
    - Web 资产是 JumpServer 支持的一种资源，旨在通过远程应用程序访问 Web 系统。它们适用于集中管理内部系统、SaaS 服务或其他基于 Web 的应用程序。
    - Web 资产依赖于远程应用程序发布者，这些发布者可以部署在 Windows 或 Linux 系统上。
    - 当用户连接到 Web 资产时，系统会自动调用发布者以启动访问目标系统的预配置浏览器。这种方法可以实现安全和受控的访问，有效防止用户直接访问目标地址。

## 创建 Web 资产
!!! tip ""
	- 在页面左上角，选择 ，然后单击 **控制台**。

	- 在左侧菜单中单机 **资产**

	- 在右侧页面上单击 **web**

	- 在表格上方， 单击 **创建** 其右侧的 下拉按钮。

	- 选择网站平台

	- 键入网站的名称

	- 键入网站 URL， 如果端口号不是 80 或 443 ， 请包括端口号

	- 选择一个或多个节点

	- 选择自动填充方法。有关详细信息，请参阅[关于自动填充](https://www.jumpserver.com/docs/assets/create-web#about-autofill)(需要用到Xpath定位器等定位方式)。

	- （可选）手动添加帐户或从模板添加帐户。

	- （可选）仅选择一个区域。

	- （可选）选择一个或多个标记。

	- （可选）键入网站的描述。

	- 单击 **“提交”** 或 **“保存并继续**”。

## 关于自动填充
!!! tip ""
	- 自动填充功能主要用于需要用户身份验证的网站。在用户访问此类网站之前，JumpServer 会自动在登录页面填写预定义的用户名和密码以完成身份验证。此过程对用户是透明的，无需手动输入凭据。

### 禁用
!!! tip ""
	- 此禁用方法适用于不需要身份验证的网站。

### 基本
!!! tip ""
	- 基本方法适用于用户名、密码和登录按钮都在同一页面上的网站。JumpServer 会自动填写凭据并提交表单以对用户进行身份验证。

	- 自动填充信息时，**需要在网页上定位元素**。支持的选择器类型包括名称选择器、ID 选择器、类选择器、CSS 选择器和 XPath 选择器。有关更多信息，请参阅[Selenium Python：定位元素](https://selenium-python.readthedocs.io/locating-elements.html).

### 脚本
!!! tip ""
	- 此脚本方法适用于具有复杂登录程序的网站。它支持高级自动化，包括多步骤身份验证和与动态页面元素的交互。

### 脚本结构
!!! tip ""
	- 这里的脚本是一个数组，其中每个元素都是一个字典，代表脚本中的一个步骤。

	- 每个步骤都包含以下键：
| Key     | Description                                                  |
| :------ | :----------------------------------------------------------- |
| step    | 必填。<br/>整数。<br/>指示脚本的执行顺序，从 1 开始，依次递增。 |
| value   | 必填。<br/>字符串。<br/>支持的内置变量：{USERNAME}、{SECRET}。<br/>如果命令不是类型，请将值保留为空字符串。 |
| target  | 必填。<br/>字符串。<br/>要作的目标元素，可以是选择器或 XPath 表达式。 |
| command | 必填。<br/>字符串。要执行<br/>的命令，可以是以下命令之一：单击、键入、睡眠select_frame。 |

| Command      | Description                                                  |
| :----------- | :----------------------------------------------------------- |
| click        | 单击目标元素。                                               |
| type         | 在目标元素中键入值。                                         |
| sleep        | 暂停脚本指定的持续时间，通常是为了允许在导航期间加载页面。持续时间<br/>由目标指定，以秒为单位。 |
| select_frame | 切换到指定的iframe进行作。<br/>目标支持 id=iframe_id、name=iframe_name 或 index=1 等选项（如果 index < 0，则切换回默认/主 iframe）。 |

### 脚本示例

```
[  // 切换到 id=iframe_id 的 iframe。
	{      
		"step": 1,      
		"command": "select_frame",      
		"target": "id=iframe_id",      
		"value": ""  
	},  
	// 在输入字段中输入用户名，name=username。
	// 执行脚本时，{USERNAME} 变量将替换为实际的用户名。
	{      
		"step": 2,      
		"command": "type",      
		"target": "name=username",      
		"value": "{USERNAME}"  
	},  
	// 单击下一步按钮继续登录过程的下一步。
	{      
		"step": 3,      
		"command": "click",      
		"target": "id=next_button",      
		"value": ""  
	},  
	// 暂停脚本 5 秒钟以允许加载下一页。
	{      
		"step": 4,      
		"command": "sleep",      
		"target": "5",      
		"value": ""  
	},  
	// 在输入字段中输入密码，name=password。
	// 执行脚本时，{SECRET} 变量将替换为实际密码。
	{      
		"step": 5,      
		"command": "type",      
		"target": "name=password",      
		"value": "{SECRET}"  
	},  
	// 单击提交按钮以完成登录过程。
	{      
		"step": 6,      
		"command": "click",      
		"target": "id=submit_button",      
		"value": ""  
	}
]
```