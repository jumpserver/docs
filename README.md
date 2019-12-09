# Jumpserver 项目规范（Draft）

## 代码风格

1. Python方面大致的风格，我们采用[pocoo的Style Guidance](http://www.pocoo.org/internal/styleguide/)，但是有些细节部分会尽量放开。
2. 前端部分(js, css, html)，采用[Google的HTML/CSS Coding Style Guidance](https://google.github.io/styleguide/htmlcssguide.xml)以及[JavaScript Coding Style](http://google.github.io/styleguide/javascriptguide.xml)
3. Google也有[Angular的Coding Style Guidance](http://google.github.io/styleguide/angularjs-google-style.html)，但该原则适用于1.x的Angular。考虑我们打算使用Angular 2，web项目负责人及开发人员请有选择地参考。
4. Google的Style指南还规范了各种写法，不光包括Coding Format，请尽量遵守，但Coding Format的原则则必须遵守。
5. Go的代码风格由@Tad指定。
6. 所有人编码前请仔细阅读相应的代码风格指导规范，编码的时候请严格遵循，相互review代码。


关于代码风格规范一些补充说明：

### 基本的代码布局

#### 缩进

1. Python严格采用4个空格的缩进，不使用tab（\t），任何python代码都都必须遵守此规定。
2. web部分代码(HTML, CSS, JavaScript)，Node.js采用2空格缩进，同样不使用tab (\t)。
之所以与Python不同，是因为js中有大量回调式的写法，2空格可以显著降低视觉上的负担。

#### 最大行长度

按PEP8规范，Python一般限制最大80个字符。但是考虑到目前大部分人使用IDE，并且拥有一个大屏显示器，这个标准放宽到120个英文字符。  

**补充说明：HTML代码不受此规范约束。**

#### 长语句缩进

Python代码参考pocoo style一致。JavaScript代码参考Google的Coding Format说明。

#### 空行

Python代码参考pocoo style一致。JavaScript代码参考Google的Coding Format说明。

### 语句和表达式

Python代码参考pocoo style一致。JavaScript代码参考Google的Coding Format说明。

### 命名约定

Python代码参考pocoo style一致。JavaScript代码参考Google的Coding Format说明。

### 文档注释(Docstring，即各方法，类的说明文档注释)

Python代码参考pocoo style一致。JavaScript代码参考Google的Coding Format说明。

### 注释(comment)

Python代码参考pocoo style一致。JavaScript代码参考Google的Coding Format说明。

## 项目骨架

## Flask项目

骨架说明如下：  

```
project_root
|-.gitignore
|-apps/
    |-common/            // 项目公共组件代码，一些基础代码，比如helper之类的可以放在这个下面。请根据具体的项目情况约定modules的命名。
    |-sub_app1/
        |-views.py       // http view handlers，必须使用Blueprint来组织子app的view，必须使用blueprint作为Blueprint对象的变量名
        |-admin.py       // Flask-Admin views，如果有的话，没有可以省略
        |-models.py      // Database Models
        |-tests.py       // 测试用例
    |-sub_app2/
        ...
    |-sub_app3/
        ...
    __init__.py          // Flask WSGI app的module，内容必须包括Flask app的创建函数create_app，以及一个app变量，表示创建好的app，具体的意义请参考core项目的dev分支下的相应文件
|-config.py              // Flask app 配置，采用Python Class定义的方式写配置，配置不要加入版本控制，可以每个项目共享一个基本的配置，交由组员根据具体的测试情况和部署情况修改。以后发布后，安装脚本要负责生成这个文件。
|-manage.py              // 项目管理脚本，负责运行项目相关的命令，比如migrate, shell, debug时的runserver等任务。该脚本必须有可执行权限。
|-README.md
|-LICENSE
```
更具体的情况请参考core项目的代码结构。

### Go项目

请@Tad负责补完。

### web项目

目录结构为

```
web
|-  api/                 // api 所有交互的API的json格式样例，命名规则 checklogin（默认返回的JSON格式），checklogin_METHOD（METHOD 为请求发送的方式，小写，内为发送的请求json样例），
|-  css/                 // css 编译完全的文件及非库文件
|-  js/                  // js 编译完全的文件,项目使用ts,故此文件夹内只有库文件的打包压缩后的文件
|-  ts/                  // ts 文件目录,遵循https://github.com/Microsoft/TypeScript/wiki/Coding-guidelines 规范
|-  fonts/               // 字体目录
|-  imgs/                // 图片文件
|-  index.html           // 默认返回的index.html文件
|-  node_modules/        // 该文件夹需使用npm install生成,默认不需要
|-  package.json         // 项目所需的node库,遵循npm规范
|-  gruntfile.js         // js, css 压缩配置文件,grunt 你懂的
\-  nginx.conf           // nginx 配置文件
```
详细编码规范后期说明

#### 项目部署

源代码下载
```
git clone -b master https://github.com/jumpserver/web.git --depth 1
```
或者 直接下载这个链接<https://github.com/jumpserver/web/archive/master.zip>

解解压进入到项目目录，将nginx.conf复制到你的nginx sites-enabled 目录下（高级的运维会放到 sites-available ，然后做软连接），修改对应路径和域名。`nginx -s relooad `


## 数据库规范

1. 原则上每个项目如果有数据库的需求，必须有独立的数据库（即便是在同一台数据库服务器上，Database name必须也是独立的）。

### 命名原则

1. Database name 采用"jumpserver\_<project\_name>"命名，比如core项目则是："jumpserver\_core"  
2. 表名以<sub\_appname>\_<model\_name>命名，比如：core项目下有user\_management子app，下面的models有User和Role,则可分别命名为:"user\_management\_user", "user\_management\_role" （SQLAlchemy请在定义Model的时候指定\_\_tablename\_\_字段）
3. 列名（使用SQLAlchemy的话，由SQLAlchemy负责生成，一般与python attribute name一致）  

### 数据交换

原则上各项目仅允许操作自己的数据库，不允许操作其他的数据库。如果项目之间有数据交换的需求，则通过其他项目提供的HTTP API调用获得数据。

**补充说明：请@董帅注意这部分的权限设计**

### API

这里仅考虑REST API的基本情况。

#### HTTP Method

1. 读操作使用GET方法，写操作使用PUT/POST/DELETE方法，其中删除记录的操作使用DELETE方法。  
2. 使用PUT方法实现的API必须是幂等的（多次执行同样操作，结果相同）。
3. POST则是实现非幂等的接口。
4. 一般性的CRUD操作，R一般使用GET方法，C使用POST，U使用PUT方法，D使用DELETE方法。

#### URL

1. 每个项目的的root path后面整合的时候回指定为项目名，这个不需要各项目组考虑。整合的方案可以采用Nginx来转发，也可以使用Werkzeug的DispatchMiddleware，后面可以详细讨论
2. 每个sub_app的blueprint在创建对象的时候提供一个url_prefix参数，规定sub_app下的url path前缀。例如：core项目的authority sub app, blueprint的url_prefix参数定义为："/authority"，下面有一个get role的接口，url为"/role/<role_id>", 则该接口的完整url path应该为："/authority/role/<role_id>"。
后面在加入了nginx转发/DispatchMiddleware的话，完整的url path应该是"/core/authority/role/<role_id>"。
3. 一般性的增删查改(CRUD)API，完全使用HTTP method加上url提供的语义，url中的可变部分（比如上面提到的<role_id>）一般用来传递该API操作的核心实体对象的唯一ID，如果有更多的参数需要提供，GET方法请使用url parameter(例如："?client_id=xxxxx&app_id=xxxxxx")，PUT/POST/DELETE方法请使用请求体传递参数。

**其他具体情况具体讨论**
