# 负载均衡

!!! info "环境说明"
    - 除 JumpServer 自身组件外, 其他组件的高可用请参考对应的官方文档进行部署
    - 按照此方式部署后, 后续只需要根据需要扩容 core web 节点然后添加节点到 nginx 即可
    - 如果已经有 HLB 或者 SLB 可以跳过 nginx 部署, 第三方 LB 要注意 session 和 websocket 问题
    - 如果已经有 云存储(* S3/Ceph/Swift/OSS/Azure) 可以跳过 MinIO 部署, MySQL Redis 也一样

| DB      | Version |    | Cache | Version |
| :------ | :------ | :- | :---- | :------ |
| MySQL   | >= 5.7  |    | Redis | >= 5.0  |
| MariaDB | >= 10.2 |    |       |         |

| Server Name   |        IP        |  Port  |     Use          |   Minimize Hardware   |   Standard Hardware    |
| ------------- | ---------------- | ------ | ---------------- | --------------------- | ---------------------- |
| MySQL         |  192.168.100.11  |  3306  |  Core            | 2Core/4GB RAM/1T  HDD | 4Core/16GB RAM/1T  SSD |  
| Redis         |  192.168.100.11  |  6379  |  Core, Koko      | 2Core/4GB RAM/60G HDD | 2Core/8GB  RAM/60G SSD |
| Nginx         |  192.168.100.100 | 80,443 |  All             | 2Core/4GB RAM/60G HDD | 4Core/8GB  RAM/60G SSD |
| Core Web 01   |  192.168.100.21  |  8080  |  Nginx           | 2Core/8GB RAM/60G HDD | 4Core/8GB  RAM/90G SSD |
| Core Web 02   |  192.168.100.22  |  8080  |  Nginx           | 2Core/8GB RAM/60G HDD | 4Core/8GB  RAM/90G SSD |
| Core Task     |  192.168.100.31  |  8080  |  Nginx           | 4Core/8GB RAM/60G HDD | 4Core/16GB RAM/90G SSD |
| MinIO         |  192.168.100.41  |  9000  |  KoKo, Guacamole | 2Core/4GB RAM/1T  HDD | 4Core/8GB  RAM/1T  SSD |

!!! warning "Core Task 目前仅支持单节点运行, 后续会优化"

## 部署 MySQL 服务

    服务器: 192.168.100.11

!!! tip "设置 Repo"
    ```sh
    yum -y localinstall http://mirrors.ustc.edu.cn/mysql-repo/mysql57-community-release-el7.rpm
    ```
    ```vim
    已加载插件：fastestmirror
    mysql57-community-release-el7.rpm                                                                                       |  25 kB  00:00:00     
    正在检查 /var/tmp/yum-root-gC5FvR/mysql57-community-release-el7.rpm: mysql57-community-release-el7-11.noarch
    /var/tmp/yum-root-gC5FvR/mysql57-community-release-el7.rpm 将被安装
    正在解决依赖关系
    --> 正在检查事务
    ---> 软件包 mysql57-community-release.noarch.0.el7-11 将被 安装
    --> 解决依赖关系完成

    依赖关系解决

    ===============================================================================================================================================
     Package                                   架构                   版本                    源                                              大小
    ===============================================================================================================================================
    正在安装:
     mysql57-community-release                 noarch                 el7-11                  /mysql57-community-release-el7                  31 k

    事务概要
    ===============================================================================================================================================
    安装  1 软件包

    总计：31 k
    安装大小：31 k
    Downloading packages:
    Running transaction check
    Running transaction test
    Transaction test succeeded
    Running transaction
      正在安装    : mysql57-community-release-el7-11.noarch                                                                                    1/1
      验证中      : mysql57-community-release-el7-11.noarch                                                                                    1/1

    已安装:
      mysql57-community-release.noarch 0:el7-11                                                                                                    

    完毕！
    ```

!!! tip "安装 MySQL"
    ```sh
    yum install -y mysql-community-server
    ```
    ```vim
    已加载插件：fastestmirror
    Determining fastest mirrors
     * base: mirrors.aliyun.com
     * extras: mirrors.aliyun.com
     * updates: mirrors.aliyun.com
    base                                                                                                                    | 3.6 kB  00:00:00    
    extras                                                                                                                  | 2.9 kB  00:00:00    
    mysql-connectors-community                                                                                              | 2.6 kB  00:00:00    
    mysql-tools-community                                                                                                   | 2.6 kB  00:00:00    
    mysql57-community                                                                                                       | 2.6 kB  00:00:00    
    updates                                                                                                                 | 2.9 kB  00:00:00    
    (1/7): base/7/x86_64/group_gz                                                                                           | 153 kB  00:00:00    
    (2/7): extras/7/x86_64/primary_db                                                                                       | 222 kB  00:00:00    
    (3/7): base/7/x86_64/primary_db                                                                                         | 6.1 MB  00:00:00    
    (4/7): updates/7/x86_64/primary_db                                                                                      | 4.7 MB  00:00:00    
    (5/7): mysql-tools-community/x86_64/primary_db                                                                          |  83 kB  00:00:01    
    (6/7): mysql-connectors-community/x86_64/primary_db                                                                     |  68 kB  00:00:01    
    (7/7): mysql57-community/x86_64/primary_db                                                                              | 247 kB  00:00:02    
    正在解决依赖关系
    --> 正在检查事务
    ---> 软件包 mysql-community-server.x86_64.0.5.7.32-1.el7 将被 安装
    --> 正在处理依赖关系 mysql-community-common(x86-64) = 5.7.32-1.el7，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在处理依赖关系 mysql-community-client(x86-64) >= 5.7.9，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在处理依赖关系 /usr/bin/perl，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在处理依赖关系 libaio.so.1(LIBAIO_0.1)(64bit)，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在处理依赖关系 libaio.so.1(LIBAIO_0.4)(64bit)，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在处理依赖关系 net-tools，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Getopt::Long)，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在处理依赖关系 perl(strict)，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在处理依赖关系 libaio.so.1()(64bit)，它被软件包 mysql-community-server-5.7.32-1.el7.x86_64 需要
    --> 正在检查事务
    ---> 软件包 libaio.x86_64.0.0.3.109-13.el7 将被 安装
    ---> 软件包 mysql-community-client.x86_64.0.5.7.32-1.el7 将被 安装
    --> 正在处理依赖关系 mysql-community-libs(x86-64) >= 5.7.9，它被软件包 mysql-community-client-5.7.32-1.el7.x86_64 需要
    ---> 软件包 mysql-community-common.x86_64.0.5.7.32-1.el7 将被 安装
    ---> 软件包 net-tools.x86_64.0.2.0-0.25.20131004git.el7 将被 安装
    ---> 软件包 perl.x86_64.4.5.16.3-297.el7 将被 安装
    --> 正在处理依赖关系 perl-libs = 4:5.16.3-297.el7，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Socket) >= 1.3，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Scalar::Util) >= 1.10，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl-macros，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl-libs，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(threads::shared)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(threads)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(constant)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Time::Local)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Time::HiRes)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Storable)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Socket)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Scalar::Util)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Pod::Simple::XHTML)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Pod::Simple::Search)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Filter::Util::Call)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(File::Temp)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(File::Spec::Unix)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(File::Spec::Functions)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(File::Spec)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(File::Path)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Exporter)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Cwd)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 perl(Carp)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    --> 正在处理依赖关系 libperl.so()(64bit)，它被软件包 4:perl-5.16.3-297.el7.x86_64 需要
    ---> 软件包 perl-Getopt-Long.noarch.0.2.40-3.el7 将被 安装
    --> 正在处理依赖关系 perl(Pod::Usage) >= 1.14，它被软件包 perl-Getopt-Long-2.40-3.el7.noarch 需要
    --> 正在处理依赖关系 perl(Text::ParseWords)，它被软件包 perl-Getopt-Long-2.40-3.el7.noarch 需要
    --> 正在检查事务
    ---> 软件包 mariadb-libs.x86_64.1.5.5.68-1.el7 将被 取代
    --> 正在处理依赖关系 libmysqlclient.so.18()(64bit)，它被软件包 2:postfix-2.10.1-9.el7.x86_64 需要
    --> 正在处理依赖关系 libmysqlclient.so.18(libmysqlclient_18)(64bit)，它被软件包 2:postfix-2.10.1-9.el7.x86_64 需要
    ---> 软件包 mysql-community-libs.x86_64.0.5.7.32-1.el7 将被 舍弃
    ---> 软件包 perl-Carp.noarch.0.1.26-244.el7 将被 安装
    ---> 软件包 perl-Exporter.noarch.0.5.68-3.el7 将被 安装
    ---> 软件包 perl-File-Path.noarch.0.2.09-2.el7 将被 安装
    ---> 软件包 perl-File-Temp.noarch.0.0.23.01-3.el7 将被 安装
    ---> 软件包 perl-Filter.x86_64.0.1.49-3.el7 将被 安装
    ---> 软件包 perl-PathTools.x86_64.0.3.40-5.el7 将被 安装
    ---> 软件包 perl-Pod-Simple.noarch.1.3.28-4.el7 将被 安装
    --> 正在处理依赖关系 perl(Pod::Escapes) >= 1.04，它被软件包 1:perl-Pod-Simple-3.28-4.el7.noarch 需要
    --> 正在处理依赖关系 perl(Encode)，它被软件包 1:perl-Pod-Simple-3.28-4.el7.noarch 需要
    ---> 软件包 perl-Pod-Usage.noarch.0.1.63-3.el7 将被 安装
    --> 正在处理依赖关系 perl(Pod::Text) >= 3.15，它被软件包 perl-Pod-Usage-1.63-3.el7.noarch 需要
    --> 正在处理依赖关系 perl-Pod-Perldoc，它被软件包 perl-Pod-Usage-1.63-3.el7.noarch 需要
    ---> 软件包 perl-Scalar-List-Utils.x86_64.0.1.27-248.el7 将被 安装
    ---> 软件包 perl-Socket.x86_64.0.2.010-5.el7 将被 安装
    ---> 软件包 perl-Storable.x86_64.0.2.45-3.el7 将被 安装
    ---> 软件包 perl-Text-ParseWords.noarch.0.3.29-4.el7 将被 安装
    ---> 软件包 perl-Time-HiRes.x86_64.4.1.9725-3.el7 将被 安装
    ---> 软件包 perl-Time-Local.noarch.0.1.2300-2.el7 将被 安装
    ---> 软件包 perl-constant.noarch.0.1.27-2.el7 将被 安装
    ---> 软件包 perl-libs.x86_64.4.5.16.3-297.el7 将被 安装
    ---> 软件包 perl-macros.x86_64.4.5.16.3-297.el7 将被 安装
    ---> 软件包 perl-threads.x86_64.0.1.87-4.el7 将被 安装
    ---> 软件包 perl-threads-shared.x86_64.0.1.43-6.el7 将被 安装
    --> 正在检查事务
    ---> 软件包 mysql-community-libs-compat.x86_64.0.5.7.32-1.el7 将被 舍弃
    ---> 软件包 perl-Encode.x86_64.0.2.51-7.el7 将被 安装
    ---> 软件包 perl-Pod-Escapes.noarch.1.1.04-297.el7 将被 安装
    ---> 软件包 perl-Pod-Perldoc.noarch.0.3.20-4.el7 将被 安装
    --> 正在处理依赖关系 perl(parent)，它被软件包 perl-Pod-Perldoc-3.20-4.el7.noarch 需要
    --> 正在处理依赖关系 perl(HTTP::Tiny)，它被软件包 perl-Pod-Perldoc-3.20-4.el7.noarch 需要
    ---> 软件包 perl-podlators.noarch.0.2.5.1-3.el7 将被 安装
    --> 正在检查事务
    ---> 软件包 perl-HTTP-Tiny.noarch.0.0.033-3.el7 将被 安装
    ---> 软件包 perl-parent.noarch.1.0.225-244.el7 将被 安装
    --> 解决依赖关系完成

    依赖关系解决

    ==============================================================================================================================================
     Package                                   架构                 版本                                     源                               大小
    ==============================================================================================================================================
    正在安装:
     mysql-community-libs                      x86_64               5.7.32-1.el7                             mysql57-community               2.3 M
          替换  mariadb-libs.x86_64 1:5.5.68-1.el7
     mysql-community-libs-compat               x86_64               5.7.32-1.el7                             mysql57-community               1.2 M
          替换  mariadb-libs.x86_64 1:5.5.68-1.el7
     mysql-community-server                    x86_64               5.7.32-1.el7                             mysql57-community               173 M
    为依赖而安装:
     libaio                                    x86_64               0.3.109-13.el7                           base                             24 k
     mysql-community-client                    x86_64               5.7.32-1.el7                             mysql57-community                25 M
     mysql-community-common                    x86_64               5.7.32-1.el7                             mysql57-community               308 k
     net-tools                                 x86_64               2.0-0.25.20131004git.el7                 base                            306 k
     perl                                      x86_64               4:5.16.3-297.el7                         base                            8.0 M
     perl-Carp                                 noarch               1.26-244.el7                             base                             19 k
     perl-Encode                               x86_64               2.51-7.el7                               base                            1.5 M
     perl-Exporter                             noarch               5.68-3.el7                               base                             28 k
     perl-File-Path                            noarch               2.09-2.el7                               base                             26 k
     perl-File-Temp                            noarch               0.23.01-3.el7                            base                             56 k
     perl-Filter                               x86_64               1.49-3.el7                               base                             76 k
     perl-Getopt-Long                          noarch               2.40-3.el7                               base                             56 k
     perl-HTTP-Tiny                            noarch               0.033-3.el7                              base                             38 k
     perl-PathTools                            x86_64               3.40-5.el7                               base                             82 k
     perl-Pod-Escapes                          noarch               1:1.04-297.el7                           base                             52 k
     perl-Pod-Perldoc                          noarch               3.20-4.el7                               base                             87 k
     perl-Pod-Simple                           noarch               1:3.28-4.el7                             base                            216 k
     perl-Pod-Usage                            noarch               1.63-3.el7                               base                             27 k
     perl-Scalar-List-Utils                    x86_64               1.27-248.el7                             base                             36 k
     perl-Socket                               x86_64               2.010-5.el7                              base                             49 k
     perl-Storable                             x86_64               2.45-3.el7                               base                             77 k
     perl-Text-ParseWords                      noarch               3.29-4.el7                               base                             14 k
     perl-Time-HiRes                           x86_64               4:1.9725-3.el7                           base                             45 k
     perl-Time-Local                           noarch               1.2300-2.el7                             base                             24 k
     perl-constant                             noarch               1.27-2.el7                               base                             19 k
     perl-libs                                 x86_64               4:5.16.3-297.el7                         base                            689 k
     perl-macros                               x86_64               4:5.16.3-297.el7                         base                             44 k
     perl-parent                               noarch               1:0.225-244.el7                          base                             12 k
     perl-podlators                            noarch               2.5.1-3.el7                              base                            112 k
     perl-threads                              x86_64               1.87-4.el7                               base                             49 k
     perl-threads-shared                       x86_64               1.43-6.el7                               base                             39 k

    事务概要
    ==============================================================================================================================================
    安装  3 软件包 (+31 依赖软件包)

    总下载量：214 M
    Downloading packages:
    (1/34): libaio-0.3.109-13.el7.x86_64.rpm                                                                                |  24 kB  00:00:00    
    warning: /var/cache/yum/x86_64/7/mysql57-community/packages/mysql-community-common-5.7.32-1.el7.x86_64.rpm: Header V3 DSA/SHA1 Signature, key D 5072e1f5: NOKEY
    mysql-community-common-5.7.32-1.el7.x86_64.rpm 的公钥尚未安装
    (2/34): mysql-community-common-5.7.32-1.el7.x86_64.rpm                                                                  | 308 kB  00:00:02    
    (3/34): mysql-community-libs-5.7.32-1.el7.x86_64.rpm                                                                    | 2.3 MB  00:00:02    
    (4/34): mysql-community-libs-compat-5.7.32-1.el7.x86_64.rpm                                                             | 1.2 MB  00:00:01    
    (5/34): net-tools-2.0-0.25.20131004git.el7.x86_64.rpm                                                                   | 306 kB  00:00:00    
    (6/34): perl-Carp-1.26-244.el7.noarch.rpm                                                                               |  19 kB  00:00:00    
    (7/34): perl-Encode-2.51-7.el7.x86_64.rpm                                                                               | 1.5 MB  00:00:00    
    (8/34): perl-Exporter-5.68-3.el7.noarch.rpm                                                                             |  28 kB  00:00:00    
    (9/34): perl-File-Path-2.09-2.el7.noarch.rpm                                                                            |  26 kB  00:00:00    
    (10/34): perl-File-Temp-0.23.01-3.el7.noarch.rpm                                                                        |  56 kB  00:00:00    
    (11/34): perl-Filter-1.49-3.el7.x86_64.rpm                                                                              |  76 kB  00:00:00    
    (12/34): perl-5.16.3-297.el7.x86_64.rpm                                                                                 | 8.0 MB  00:00:01    
    (13/34): perl-Getopt-Long-2.40-3.el7.noarch.rpm                                                                         |  56 kB  00:00:00    
    (14/34): perl-HTTP-Tiny-0.033-3.el7.noarch.rpm                                                                          |  38 kB  00:00:00    
    (15/34): perl-PathTools-3.40-5.el7.x86_64.rpm                                                                           |  82 kB  00:00:00    
    (16/34): perl-Pod-Escapes-1.04-297.el7.noarch.rpm                                                                       |  52 kB  00:00:00    
    (17/34): perl-Pod-Perldoc-3.20-4.el7.noarch.rpm                                                                         |  87 kB  00:00:00    
    (18/34): perl-Pod-Usage-1.63-3.el7.noarch.rpm                                                                           |  27 kB  00:00:00    
    (19/34): perl-Pod-Simple-3.28-4.el7.noarch.rpm                                                                          | 216 kB  00:00:00    
    (20/34): perl-Scalar-List-Utils-1.27-248.el7.x86_64.rpm                                                                 |  36 kB  00:00:00    
    (21/34): perl-Storable-2.45-3.el7.x86_64.rpm                                                                            |  77 kB  00:00:00    
    (22/34): perl-Socket-2.010-5.el7.x86_64.rpm                                                                             |  49 kB  00:00:00    
    (23/34): perl-Text-ParseWords-3.29-4.el7.noarch.rpm                                                                     |  14 kB  00:00:00    
    (24/34): perl-Time-HiRes-1.9725-3.el7.x86_64.rpm                                                                        |  45 kB  00:00:00    
    (25/34): perl-constant-1.27-2.el7.noarch.rpm                                                                            |  19 kB  00:00:00    
    (26/34): perl-Time-Local-1.2300-2.el7.noarch.rpm                                                                        |  24 kB  00:00:00    
    (27/34): perl-macros-5.16.3-297.el7.x86_64.rpm                                                                          |  44 kB  00:00:00    
    (28/34): perl-libs-5.16.3-297.el7.x86_64.rpm                                                                            | 689 kB  00:00:00    
    (29/34): perl-parent-0.225-244.el7.noarch.rpm                                                                           |  12 kB  00:00:00    
    (30/34): perl-podlators-2.5.1-3.el7.noarch.rpm                                                                          | 112 kB  00:00:00    
    (31/34): perl-threads-1.87-4.el7.x86_64.rpm                                                                             |  49 kB  00:00:00    
    (32/34): perl-threads-shared-1.43-6.el7.x86_64.rpm                                                                      |  39 kB  00:00:00    
    (34/34): mysql-community-server-5.7.32-1.el7.x86_64.rpm  22% [==========-                                    ] 3.2 MB/s |  49 MB  00:00:52 ETA(33/34): mysql-community-server-5.7.32-1.el7.x86_64.rpm                                                               | 173 MB  00:00:57     
    (34/34): mysql-community-client-5.7.32-1.el7.x86_64.rpm                                                               |  25 MB  00:20:48     
    ---------------------------------------------------------------------------------------------------------------------------------------------
    总计                                                                                                         176 kB/s | 214 MB  00:20:48     
    从 file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql 检索密钥
    导入 GPG key 0x5072E1F5:
     用户ID     : "MySQL Release Engineering <mysql-build@oss.oracle.com>"
     指纹       : a4a9 4068 76fc bd3c 4567 70c8 8c71 8d3b 5072 e1f5
     软件包     : mysql57-community-release-el7-11.noarch (@/mysql57-community-release-el7)
     来自       : /etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
    Running transaction check
    Running transaction test
    Transaction test succeeded
    Running transaction
      正在安装    : mysql-community-common-5.7.32-1.el7.x86_64                                                                              1/35
      正在安装    : mysql-community-libs-5.7.32-1.el7.x86_64                                                                                2/35
      正在安装    : mysql-community-client-5.7.32-1.el7.x86_64                                                                              3/35
      正在安装    : 1:perl-parent-0.225-244.el7.noarch                                                                                      4/35
      正在安装    : perl-HTTP-Tiny-0.033-3.el7.noarch                                                                                       5/35
      正在安装    : perl-podlators-2.5.1-3.el7.noarch                                                                                       6/35
      正在安装    : perl-Pod-Perldoc-3.20-4.el7.noarch                                                                                      7/35
      正在安装    : 1:perl-Pod-Escapes-1.04-297.el7.noarch                                                                                  8/35
      正在安装    : perl-Encode-2.51-7.el7.x86_64                                                                                           9/35
      正在安装    : perl-Text-ParseWords-3.29-4.el7.noarch                                                                                 10/35
      正在安装    : perl-Pod-Usage-1.63-3.el7.noarch                                                                                       11/35
      正在安装    : 4:perl-libs-5.16.3-297.el7.x86_64                                                                                      12/35
      正在安装    : perl-Storable-2.45-3.el7.x86_64                                                                                        13/35
      正在安装    : perl-Exporter-5.68-3.el7.noarch                                                                                        14/35
      正在安装    : perl-constant-1.27-2.el7.noarch                                                                                        15/35
      正在安装    : perl-Socket-2.010-5.el7.x86_64                                                                                         16/35
      正在安装    : perl-Time-Local-1.2300-2.el7.noarch                                                                                    17/35
      正在安装    : perl-Carp-1.26-244.el7.noarch                                                                                          18/35
      正在安装    : perl-PathTools-3.40-5.el7.x86_64                                                                                       19/35
      正在安装    : perl-Scalar-List-Utils-1.27-248.el7.x86_64                                                                             20/35
      正在安装    : 1:perl-Pod-Simple-3.28-4.el7.noarch                                                                                    21/35
      正在安装    : perl-File-Temp-0.23.01-3.el7.noarch                                                                                    22/35
      正在安装    : perl-File-Path-2.09-2.el7.noarch                                                                                       23/35
      正在安装    : perl-threads-shared-1.43-6.el7.x86_64                                                                                  24/35
      正在安装    : perl-threads-1.87-4.el7.x86_64                                                                                         25/35
      正在安装    : 4:perl-Time-HiRes-1.9725-3.el7.x86_64                                                                                  26/35
      正在安装    : perl-Filter-1.49-3.el7.x86_64                                                                                          27/35
      正在安装    : 4:perl-macros-5.16.3-297.el7.x86_64                                                                                    28/35
      正在安装    : perl-Getopt-Long-2.40-3.el7.noarch                                                                                     29/35
      正在安装    : 4:perl-5.16.3-297.el7.x86_64                                                                                           30/35
      正在安装    : libaio-0.3.109-13.el7.x86_64                                                                                           31/35
      正在安装    : net-tools-2.0-0.25.20131004git.el7.x86_64                                                                              32/35
      正在安装    : mysql-community-server-5.7.32-1.el7.x86_64                                                                             33/35
      正在安装    : mysql-community-libs-compat-5.7.32-1.el7.x86_64                                                                        34/35
      正在删除    : 1:mariadb-libs-5.5.68-1.el7.x86_64                                                                                     35/35
      验证中      : perl-HTTP-Tiny-0.033-3.el7.noarch                                                                                       1/35
      验证中      : perl-threads-shared-1.43-6.el7.x86_64                                                                                   2/35
      验证中      : perl-Storable-2.45-3.el7.x86_64                                                                                         3/35
      验证中      : 4:perl-libs-5.16.3-297.el7.x86_64                                                                                       4/35
      验证中      : perl-Exporter-5.68-3.el7.noarch                                                                                         5/35
      验证中      : perl-constant-1.27-2.el7.noarch                                                                                         6/35
      验证中      : perl-PathTools-3.40-5.el7.x86_64                                                                                        7/35
      验证中      : perl-Socket-2.010-5.el7.x86_64                                                                                          8/35
      验证中      : 1:perl-parent-0.225-244.el7.noarch                                                                                      9/35
      验证中      : perl-Pod-Usage-1.63-3.el7.noarch                                                                                       10/35
      验证中      : 1:perl-Pod-Escapes-1.04-297.el7.noarch                                                                                 11/35
      验证中      : perl-File-Temp-0.23.01-3.el7.noarch                                                                                    12/35
      验证中      : net-tools-2.0-0.25.20131004git.el7.x86_64                                                                              13/35
      验证中      : 1:perl-Pod-Simple-3.28-4.el7.noarch                                                                                    14/35
      验证中      : perl-Time-Local-1.2300-2.el7.noarch                                                                                    15/35
      验证中      : libaio-0.3.109-13.el7.x86_64                                                                                           16/35
      验证中      : perl-Carp-1.26-244.el7.noarch                                                                                          17/35
      验证中      : mysql-community-client-5.7.32-1.el7.x86_64                                                                             18/35
      验证中      : mysql-community-libs-5.7.32-1.el7.x86_64                                                                               19/35
      验证中      : perl-Scalar-List-Utils-1.27-248.el7.x86_64                                                                             20/35
      验证中      : mysql-community-common-5.7.32-1.el7.x86_64                                                                             21/35
      验证中      : perl-Encode-2.51-7.el7.x86_64                                                                                          22/35
      验证中      : perl-Pod-Perldoc-3.20-4.el7.noarch                                                                                     23/35
      验证中      : perl-podlators-2.5.1-3.el7.noarch                                                                                      24/35
      验证中      : mysql-community-libs-compat-5.7.32-1.el7.x86_64                                                                        25/35
      验证中      : perl-File-Path-2.09-2.el7.noarch                                                                                       26/35
      验证中      : perl-threads-1.87-4.el7.x86_64                                                                                         27/35
      验证中      : 4:perl-Time-HiRes-1.9725-3.el7.x86_64                                                                                  28/35
      验证中      : perl-Filter-1.49-3.el7.x86_64                                                                                          29/35
      验证中      : perl-Getopt-Long-2.40-3.el7.noarch                                                                                     30/35
      验证中      : perl-Text-ParseWords-3.29-4.el7.noarch                                                                                 31/35
      验证中      : mysql-community-server-5.7.32-1.el7.x86_64                                                                             32/35
      验证中      : 4:perl-5.16.3-297.el7.x86_64                                                                                           33/35
      验证中      : 4:perl-macros-5.16.3-297.el7.x86_64                                                                                    34/35
      验证中      : 1:mariadb-libs-5.5.68-1.el7.x86_64                                                                                     35/35

    已安装:
      mysql-community-libs.x86_64 0:5.7.32-1.el7 mysql-community-libs-compat.x86_64 0:5.7.32-1.el7 mysql-community-server.x86_64 0:5.7.32-1.el7

    作为依赖被安装:
      libaio.x86_64 0:0.3.109-13.el7                mysql-community-client.x86_64 0:5.7.32-1.el7  mysql-community-common.x86_64 0:5.7.32-1.el7
      net-tools.x86_64 0:2.0-0.25.20131004git.el7   perl.x86_64 4:5.16.3-297.el7                  perl-Carp.noarch 0:1.26-244.el7              
      perl-Encode.x86_64 0:2.51-7.el7               perl-Exporter.noarch 0:5.68-3.el7             perl-File-Path.noarch 0:2.09-2.el7           
      perl-File-Temp.noarch 0:0.23.01-3.el7         perl-Filter.x86_64 0:1.49-3.el7               perl-Getopt-Long.noarch 0:2.40-3.el7         
      perl-HTTP-Tiny.noarch 0:0.033-3.el7           perl-PathTools.x86_64 0:3.40-5.el7            perl-Pod-Escapes.noarch 1:1.04-297.el7       
      perl-Pod-Perldoc.noarch 0:3.20-4.el7          perl-Pod-Simple.noarch 1:3.28-4.el7           perl-Pod-Usage.noarch 0:1.63-3.el7           
      perl-Scalar-List-Utils.x86_64 0:1.27-248.el7  perl-Socket.x86_64 0:2.010-5.el7              perl-Storable.x86_64 0:2.45-3.el7            
      perl-Text-ParseWords.noarch 0:3.29-4.el7      perl-Time-HiRes.x86_64 4:1.9725-3.el7         perl-Time-Local.noarch 0:1.2300-2.el7        
      perl-constant.noarch 0:1.27-2.el7             perl-libs.x86_64 4:5.16.3-297.el7             perl-macros.x86_64 4:5.16.3-297.el7          
      perl-parent.noarch 1:0.225-244.el7            perl-podlators.noarch 0:2.5.1-3.el7           perl-threads.x86_64 0:1.87-4.el7             
      perl-threads-shared.x86_64 0:1.43-6.el7      

    替代:
      mariadb-libs.x86_64 1:5.5.68-1.el7                                                                                                         

    完毕！
    ```

!!! tip "配置 MySQL"
    ```sh
    if [ ! "$(cat /usr/bin/mysqld_pre_systemd | grep -v ^\# | grep initialize-insecure )" ]; then
        sed -i "s@--initialize @--initialize-insecure @g" /usr/bin/mysqld_pre_systemd
    fi
    ```

!!! tip "启动 MySQL"
    ```sh
    systemctl enable mysqld
    systemctl start mysqld
    ```

!!! tip "数据库授权"
    ```sh
    mysql -uroot
    ```
    ```mysql hl_lines="13 16 19 22"
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 2
    Server version: 5.7.32 MySQL Community Server (GPL)

    Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> create database jumpserver default charset 'utf8' collate 'utf8_bin';
    Query OK, 1 row affected (0.00 sec)

    mysql> set global validate_password_policy=LOW;
    Query OK, 0 rows affected (0.00 sec)

    mysql> grant all on jumpserver.* to 'jumpserver'@'192.168.100.%' identified by 'weakPassword';
    Query OK, 0 rows affected, 1 warning (0.00 sec)

    mysql> flush privileges;
    Query OK, 0 rows affected (0.00 sec)

    mysql> exit
    Bye
    ```

!!! tip "配置防火墙"
    ```sh
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="3306" accept"
    firewall-cmd --reload
    ```

## 部署 Redis 服务

    服务器: 192.168.100.11

!!! tip "设置 Repo"
    ```sh
    yum -y install epel-release https://repo.ius.io/ius-release-el7.rpm
    ```
    ```vim
    已加载插件：fastestmirror
    Determining fastest mirrors
     * base: mirrors.ustc.edu.cn
     * extras: mirrors.ustc.edu.cn
     * updates: mirrors.ustc.edu.cn
    base                                                                                                             | 3.6 kB  00:00:00     
    extras                                                                                                           | 2.9 kB  00:00:00     
    updates                                                                                                          | 2.9 kB  00:00:00     
    (1/4): base/7/x86_64/group_gz                                                                                    | 153 kB  00:00:00     
    (2/4): extras/7/x86_64/primary_db                                                                                | 222 kB  00:00:00     
    (3/4): updates/7/x86_64/primary_db                                                                               | 4.7 MB  00:00:02     
    (4/4): base/7/x86_64/primary_db                                                                                  | 6.1 MB  00:00:02     
    ius-release-el7.rpm                                                                                              | 8.2 kB  00:00:00     
    正在检查 /var/tmp/yum-root-3MSP1P/ius-release-el7.rpm: ius-release-2-1.el7.ius.noarch
    /var/tmp/yum-root-3MSP1P/ius-release-el7.rpm 将被安装
    正在解决依赖关系
    --> 正在检查事务
    ---> 软件包 epel-release.noarch.0.7-11 将被 安装
    ---> 软件包 ius-release.noarch.0.2-1.el7.ius 将被 安装
    --> 解决依赖关系完成

    依赖关系解决

    ========================================================================================================================================
     Package                          架构                       版本                            源                                    大小
    ========================================================================================================================================
    正在安装:
     epel-release                     noarch                     7-11                            extras                                15 k
     ius-release                      noarch                     2-1.el7.ius                     /ius-release-el7                     4.5 k

    事务概要
    ========================================================================================================================================
    安装  2 软件包

    总计：19 k
    总下载量：15 k
    安装大小：29 k
    Downloading packages:
    epel-release-7-11.noarch.rpm                                                                                     |  15 kB  00:00:00     
    Running transaction check
    Running transaction test
    Transaction test succeeded
    Running transaction
      正在安装    : epel-release-7-11.noarch                                                                                            1/2
      正在安装    : ius-release-2-1.el7.ius.noarch                                                                                      2/2
      验证中      : ius-release-2-1.el7.ius.noarch                                                                                      1/2
      验证中      : epel-release-7-11.noarch                                                                                            2/2

    已安装:
      epel-release.noarch 0:7-11                                      ius-release.noarch 0:2-1.el7.ius                                     

    完毕！
    ```

!!! tip "安装 Redis"
    ```sh
    yum install -y redis5
    ```
    ```vim
    已加载插件：fastestmirror
    Loading mirror speeds from cached hostfile
    epel/x86_64/metalink                                                                                             | 6.4 kB  00:00:00     
     * base: mirrors.ustc.edu.cn
     * epel: fedora.cs.nctu.edu.tw
     * extras: mirrors.ustc.edu.cn
     * updates: mirrors.ustc.edu.cn
    base                                                                                                             | 3.6 kB  00:00:00     
    extras                                                                                                           | 2.9 kB  00:00:00     
    ius                                                                                                              | 1.3 kB  00:00:00     
    updates                                                                                                          | 2.9 kB  00:00:00     
    epel/x86_64/primary_db                                                                                           | 6.9 MB  00:00:06     
    ius                                                                                                                             584/584
    正在解决依赖关系
    --> 正在检查事务
    ---> 软件包 redis5.x86_64.0.5.0.9-1.el7.ius 将被 安装
    --> 解决依赖关系完成

    依赖关系解决

    ========================================================================================================================================
     Package                       架构                          版本                                      源                          大小
    ========================================================================================================================================
    正在安装:
     redis5                        x86_64                        5.0.9-1.el7.ius                           ius                        905 k

    事务概要
    ========================================================================================================================================
    安装  1 软件包

    总下载量：905 k
    安装大小：2.9 M
    Downloading packages:
    警告：/var/cache/yum/x86_64/7/ius/packages/redis5-5.0.9-1.el7.ius.x86_64.rpm: 头V4 RSA/SHA256 Signature, 密钥 ID 4b274df2: NOKEY:02 ETA
    redis5-5.0.9-1.el7.ius.x86_64.rpm 的公钥尚未安装
    redis5-5.0.9-1.el7.ius.x86_64.rpm                                                                                | 905 kB  00:00:02     
    从 file:///etc/pki/rpm-gpg/RPM-GPG-KEY-IUS-7 检索密钥
    导入 GPG key 0x4B274DF2:
     用户ID     : "IUS (7) <dev@ius.io>"
     指纹       : c958 7a09 a11f d706 4f0c a0f4 e558 0725 4b27 4df2
     软件包     : ius-release-2-1.el7.ius.noarch (@/ius-release-el7)
     来自       : /etc/pki/rpm-gpg/RPM-GPG-KEY-IUS-7
    Running transaction check
    Running transaction test
    Transaction test succeeded
    Running transaction
      正在安装    : redis5-5.0.9-1.el7.ius.x86_64                                                                                       1/1
      验证中      : redis5-5.0.9-1.el7.ius.x86_64                                                                                       1/1

    已安装:
      redis5.x86_64 0:5.0.9-1.el7.ius                                                                                                       

    完毕！
    ```

!!! tip "配置 Redis"
    ```sh
    sed -i "s/bind 127.0.0.1/bind 0.0.0.0/g" /etc/redis.conf
    sed -i "561i maxmemory-policy allkeys-lru" /etc/redis.conf
    sed -i "481i requirepass weakPassword" /etc/redis.conf
    ```

!!! tip "启动 Redis"
    ```sh
    systemctl enable redis
    systemctl start redis
    ```

!!! tip "配置防火墙"
    ```sh
    firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.0/24" port protocol="tcp" port="6379" accept"
    firewall-cmd --reload
    ```

## 部署 Core Web 01

    服务器: 192.168.100.21

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```

!!! tip "修改配置文件"
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="5 9-10 16"
    # 修改下面选项, 其他保持默认
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    ## Task 配置
    USE_TASK=0                                                     # 不启动 jms_celery

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW  # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                               # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # KoKo 配置
    SHARE_ROOM_TYPE=redis                                          # KoKo 使用 redis 共享
    ```
    ```sh
    ./jmsctl.sh install
    ```
    ```nginx hl_lines="26 40 44-49 53-56 69 73"

           ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
           ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
      ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
      ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
       ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

    								                             Version:  {{ jumpserver.version }}


    >>> 一、配置JumpServer
    1. 检查配置文件
    各组件使用环境变量式配置文件，而不是 yaml 格式, 配置名称与之前保持一致
    配置文件位置: /opt/jumpserver/config/config.txt
    完成

    2. 配置 Nginx 证书
    证书位置在: /opt/jumpserver/config/nginx/cert
    完成

    3. 备份配置文件
    备份至 /opt/jumpserver/config/backup/config.txt.2020-12-18_10-18-00
    完成

    4. 配置网络
    需要支持 IPv6 吗? (y/n)  (默认为n): n
    完成

    5. 自动生成加密密钥
    完成

    6. 配置持久化目录
    修改日志录像等持久化的目录，可以找个最大的磁盘，并创建目录，如 /opt/jumpserver
    注意: 安装完后不能再更改, 否则数据库可能丢失

    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.0G   49G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    设置持久化卷存储目录 (默认为/opt/jumpserver): /opt/jumpserver
    完成

    7. 配置MySQL
    是否使用外部mysql (y/n)  (默认为n): y
    请输入mysql的主机地址 (无默认值): 192.168.100.11
    请输入mysql的端口 (默认为3306): 3306
    请输入mysql的数据库(事先做好授权) (默认为jumpserver): jumpserver
    请输入mysql的用户名 (无默认值): jumpserver
    请输入mysql的密码 (无默认值): weakPassword
    完成

    8. 配置Redis
    是否使用外部redis  (y/n)  (默认为n): y
    请输入redis的主机地址 (无默认值): 192.168.100.11
    请输入redis的端口 (默认为6379): 6379
    请输入redis的密码 (无默认值): weakPassword
    完成

    >>> 二、安装配置Docker
    1. 安装Docker
    完成

    2. 配置Docker
    修改Docker镜像容器的默认存储目录，可以找个最大的磁盘, 并创建目录，如 /opt/docker
    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.2G   48G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    Docker存储目录 (默认为/opt/docker): /var/lib/docker
    完成

    3. 启动Docker
    Docker 版本发生改变 或 docker配置文件发生变化，是否要重启 (y/n)  (默认为y): y
    完成

    >>> 三、加载镜像
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

    >>> 四、安装完成了
    1. 可以使用如下命令启动, 然后访问
    ./jmsctl.sh start

    2. 其它一些管理命令
    ./jmsctl.sh stop
    ./jmsctl.sh restart
    ./jmsctl.sh backup
    ./jmsctl.sh upgrade
    更多还有一些命令，你可以 ./jmsctl.sh --help来了解

    3. 访问 Web 后台页面
    http://192.168.100.236:8080
    https://192.168.100.236:8443

    4. ssh/sftp 访问
    ssh admin@192.168.100.236 -p2222
    sftp -P2222 admin@192.168.100.236

    5. 更多信息
    我们的文档: https://docs.jumpserver.org/
    我们的官网: https://www.jumpserver.org/
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_mysql     ... done
    Creating jms_redis     ... done
    Creating jms_core      ... done
    Creating jms_luna      ... done
    Creating jms_lina      ... done
    Creating jms_guacamole ... done
    Creating jms_koko      ... done
    Creating jms_nginx     ... done
    ```    

## 部署 Core Web 02

    服务器: 192.168.100.22

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```

!!! tip "修改配置文件"
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="5 9-10 16"
    # 修改下面选项, 其他保持默认
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    ## Task 配置
    USE_TASK=0                                                     # 不启动 jms_celery

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW  # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                               # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # KoKo 配置
    SHARE_ROOM_TYPE=redis                                          # KoKo 使用 redis 共享
    ```
    ```sh
    ./jmsctl.sh install
    ```
    ```nginx hl_lines="26 40 44-49 53-56 69 73"

           ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
           ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
      ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
      ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
       ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

    								                             Version:  {{ jumpserver.version }}


    >>> 一、配置JumpServer
    1. 检查配置文件
    各组件使用环境变量式配置文件，而不是 yaml 格式, 配置名称与之前保持一致
    配置文件位置: /opt/jumpserver/config/config.txt
    完成

    2. 配置 Nginx 证书
    证书位置在: /opt/jumpserver/config/nginx/cert
    完成

    3. 备份配置文件
    备份至 /opt/jumpserver/config/backup/config.txt.2020-12-18_10-18-00
    完成

    4. 配置网络
    需要支持 IPv6 吗? (y/n)  (默认为n): n
    完成

    5. 自动生成加密密钥
    完成

    6. 配置持久化目录
    修改日志录像等持久化的目录，可以找个最大的磁盘，并创建目录，如 /opt/jumpserver
    注意: 安装完后不能再更改, 否则数据库可能丢失

    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.0G   49G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    设置持久化卷存储目录 (默认为/opt/jumpserver): /opt/jumpserver
    完成

    7. 配置MySQL
    是否使用外部mysql (y/n)  (默认为n): y
    请输入mysql的主机地址 (无默认值): 192.168.100.11
    请输入mysql的端口 (默认为3306): 3306
    请输入mysql的数据库(事先做好授权) (默认为jumpserver): jumpserver
    请输入mysql的用户名 (无默认值): jumpserver
    请输入mysql的密码 (无默认值): weakPassword
    完成

    8. 配置Redis
    是否使用外部redis  (y/n)  (默认为n): y
    请输入redis的主机地址 (无默认值): 192.168.100.11
    请输入redis的端口 (默认为6379): 6379
    请输入redis的密码 (无默认值): weakPassword
    完成

    >>> 二、安装配置Docker
    1. 安装Docker
    完成

    2. 配置Docker
    修改Docker镜像容器的默认存储目录，可以找个最大的磁盘, 并创建目录，如 /opt/docker
    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.2G   48G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    Docker存储目录 (默认为/opt/docker): /var/lib/docker
    完成

    3. 启动Docker
    Docker 版本发生改变 或 docker配置文件发生变化，是否要重启 (y/n)  (默认为y): y
    完成

    >>> 三、加载镜像
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

    >>> 四、安装完成了
    1. 可以使用如下命令启动, 然后访问
    ./jmsctl.sh start

    2. 其它一些管理命令
    ./jmsctl.sh stop
    ./jmsctl.sh restart
    ./jmsctl.sh backup
    ./jmsctl.sh upgrade
    更多还有一些命令，你可以 ./jmsctl.sh --help来了解

    3. 访问 Web 后台页面
    http://192.168.100.236:8080
    https://192.168.100.236:8443

    4. ssh/sftp 访问
    ssh admin@192.168.100.236 -p2222
    sftp -P2222 admin@192.168.100.236

    5. 更多信息
    我们的文档: https://docs.jumpserver.org/
    我们的官网: https://www.jumpserver.org/
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_mysql     ... done
    Creating jms_redis     ... done
    Creating jms_core      ... done
    Creating jms_luna      ... done
    Creating jms_lina      ... done
    Creating jms_guacamole ... done
    Creating jms_koko      ... done
    Creating jms_nginx     ... done
    ```    

## 部署 Core Task

    服务器: 192.168.100.31

!!! tip "下载 jumpserver-install"
    ```sh
    cd /opt
    yum -y install wget
    wget https://github.com/jumpserver/installer/releases/download/{{ jumpserver.version }}/jumpserver-installer-{{ jumpserver.version }}.tar.gz
    tar -xf jumpserver-installer-{{ jumpserver.version }}.tar.gz
    cd jumpserver-installer-{{ jumpserver.version }}
    ```

!!! tip "修改配置文件"
    ```sh
    vi config-example.txt
    ```
    ```vim hl_lines="5 9-10 16"
    # 修改下面选项, 其他保持默认
    ### 注意: SECRET_KEY 和要其他 JumpServer 服务器一致, 加密的数据将无法解密

    ## Task 配置
    USE_TASK=1                                                     # 启动 jms_celery

    # Core 配置
    ### 启动后不能再修改，否则密码等等信息无法解密
    SECRET_KEY=kWQdmdCQKjaWlHYpPhkNQDkfaRulM6YnHctsHLlSPs8287o2kW  # 要其他 JumpServer 服务器一致 (*)
    BOOTSTRAP_TOKEN=KXOeyNgDeTdpeu9q                               # 要其他 JumpServer 服务器一致 (*)
    LOG_LEVEL=ERROR
    # SESSION_COOKIE_AGE=86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE=true

    # KoKo 配置
    SHARE_ROOM_TYPE=redis                                          # KoKo 使用 redis 共享
    ```
    ```sh
    ./jmsctl.sh install
    ```
    ```nginx hl_lines="26 40 44-49 53-56 69 73"

           ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
           ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           ██║██║   ██║██╔████╔██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
      ██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
      ╚█████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
       ╚════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

    								                             Version:  {{ jumpserver.version }}


    >>> 一、配置JumpServer
    1. 检查配置文件
    各组件使用环境变量式配置文件，而不是 yaml 格式, 配置名称与之前保持一致
    配置文件位置: /opt/jumpserver/config/config.txt
    完成

    2. 配置 Nginx 证书
    证书位置在: /opt/jumpserver/config/nginx/cert
    完成

    3. 备份配置文件
    备份至 /opt/jumpserver/config/backup/config.txt.2020-12-18_10-18-00
    完成

    4. 配置网络
    需要支持 IPv6 吗? (y/n)  (默认为n): n
    完成

    5. 自动生成加密密钥
    完成

    6. 配置持久化目录
    修改日志录像等持久化的目录，可以找个最大的磁盘，并创建目录，如 /opt/jumpserver
    注意: 安装完后不能再更改, 否则数据库可能丢失

    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.0G   49G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    设置持久化卷存储目录 (默认为/opt/jumpserver): /opt/jumpserver
    完成

    7. 配置MySQL
    是否使用外部mysql (y/n)  (默认为n): y
    请输入mysql的主机地址 (无默认值): 192.168.100.11
    请输入mysql的端口 (默认为3306): 3306
    请输入mysql的数据库(事先做好授权) (默认为jumpserver): jumpserver
    请输入mysql的用户名 (无默认值): jumpserver
    请输入mysql的密码 (无默认值): weakPassword
    完成

    8. 配置Redis
    是否使用外部redis  (y/n)  (默认为n): y
    请输入redis的主机地址 (无默认值): 192.168.100.11
    请输入redis的端口 (默认为6379): 6379
    请输入redis的密码 (无默认值): weakPassword
    完成

    >>> 二、安装配置Docker
    1. 安装Docker
    完成

    2. 配置Docker
    修改Docker镜像容器的默认存储目录，可以找个最大的磁盘, 并创建目录，如 /opt/docker
    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        53G  5.2G   48G   10% /
    /dev/sda1      1014M  160M  855M   16% /boot

    Docker存储目录 (默认为/opt/docker): /var/lib/docker
    完成

    3. 启动Docker
    Docker 版本发生改变 或 docker配置文件发生变化，是否要重启 (y/n)  (默认为y): y
    完成

    >>> 三、加载镜像
    Docker: Pulling from jumpserver/core:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/koko:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/luna:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/nginx:alpine2   	[ OK ]
    Docker: Pulling from jumpserver/redis:6-alpine      [ OK ]
    Docker: Pulling from jumpserver/lina:{{ jumpserver.version }} 	    [ OK ]
    Docker: Pulling from jumpserver/mysql:5 	        [ OK ]
    Docker: Pulling from jumpserver/guacamole:{{ jumpserver.version }} 	[ OK ]

    >>> 四、安装完成了
    1. 可以使用如下命令启动, 然后访问
    ./jmsctl.sh start

    2. 其它一些管理命令
    ./jmsctl.sh stop
    ./jmsctl.sh restart
    ./jmsctl.sh backup
    ./jmsctl.sh upgrade
    更多还有一些命令，你可以 ./jmsctl.sh --help来了解

    3. 访问 Web 后台页面
    http://192.168.100.236:8080
    https://192.168.100.236:8443

    4. ssh/sftp 访问
    ssh admin@192.168.100.236 -p2222
    sftp -P2222 admin@192.168.100.236

    5. 更多信息
    我们的文档: https://docs.jumpserver.org/
    我们的官网: https://www.jumpserver.org/
    ```

!!! tip "启动 JumpServer"
    ```sh
    ./jmsctl.sh start
    ```
    ```nginx
    Creating network "jms_net" with driver "bridge"
    Creating jms_mysql     ... done
    Creating jms_redis     ... done
    Creating jms_core      ... done
    Creating jms_celery    ... done
    Creating jms_luna      ... done
    Creating jms_lina      ... done
    Creating jms_guacamole ... done
    Creating jms_koko      ... done
    Creating jms_nginx     ... done
    ```        

## 部署 Nginx 服务

    服务器: 192.168.100.100

!!! tip "配置 Repo"
    ```sh
    vi /etc/yum.repos.d/nginx.repo
    ```
    ```vim
    [nginx-stable]
    name=nginx stable repo
    baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
    gpgcheck=1
    enabled=1
    gpgkey=https://nginx.org/keys/nginx_signing.key
    module_hotfixes=true
    ```

!!! tip "安装 Nginx"
    ```sh
    yum install -y nginx
    ```
    ```vim
    已加载插件：fastestmirror
    Loading mirror speeds from cached hostfile
     * base: mirrors.aliyun.com
     * epel: mirror.lzu.edu.cn
     * extras: mirrors.ustc.edu.cn
     * updates: mirrors.ustc.edu.cn
    nginx-stable                                                                                                          | 2.9 kB  00:00:00     
    nginx-stable/7/x86_64/primary_db                                                                                      |  59 kB  00:00:00     
    正在解决依赖关系
    --> 正在检查事务
    ---> 软件包 nginx.x86_64.1.1.18.0-2.el7.ngx 将被 安装
    --> 解决依赖关系完成

    依赖关系解决

    =============================================================================================================================================
     Package                     架构                         版本                                      源                                  大小
    =============================================================================================================================================
    正在安装:
     nginx                       x86_64                       1:1.18.0-2.el7.ngx                        nginx-stable                       769 k

    事务概要
    =============================================================================================================================================
    安装  1 软件包

    总下载量：769 k
    安装大小：2.7 M
    Downloading packages:
    警告：/var/cache/yum/x86_64/7/nginx-stable/packages/nginx-1.18.0-2.el7.ngx.x86_64.rpm: 头V4 RSA/SHA1 Signature, 密钥 ID 7bd9bf62: NOKEY0 ETA
    nginx-1.18.0-2.el7.ngx.x86_64.rpm 的公钥尚未安装
    nginx-1.18.0-2.el7.ngx.x86_64.rpm                                                                                     | 769 kB  00:00:11     
    从 https://nginx.org/keys/nginx_signing.key 检索密钥
    导入 GPG key 0x7BD9BF62:
     用户ID     : "nginx signing key <signing-key@nginx.com>"
     指纹       : 573b fd6b 3d8f bc64 1079 a6ab abf5 bd82 7bd9 bf62
     来自       : https://nginx.org/keys/nginx_signing.key
    Running transaction check
    Running transaction test
    Transaction test succeeded
    Running transaction
      正在安装    : 1:nginx-1.18.0-2.el7.ngx.x86_64                                                                                          1/1
    ----------------------------------------------------------------------

    Thanks for using nginx!

    Please find the official documentation for nginx here:
    * http://nginx.org/en/docs/

    Please subscribe to nginx-announce mailing list to get
    the most important news about nginx:
    * http://nginx.org/en/support.html

    Commercial subscriptions for nginx are available on:
    * http://nginx.com/products/

    ----------------------------------------------------------------------
      验证中      : 1:nginx-1.18.0-2.el7.ngx.x86_64                                                                                          1/1

    已安装:
      nginx.x86_64 1:1.18.0-2.el7.ngx                                                                                                            

    完毕！
    ```

!!! tip "配置 Nginx"
    ```sh
    vi /etc/nginx/nginx.conf
    ```
    ```nginx
    user  nginx;
    worker_processes  auto;

    error_log  /var/log/nginx/error.log warn;
    pid        /var/run/nginx.pid;


    events {
        worker_connections  1024;
    }

    stream {
        log_format  proxy  '$remote_addr [$time_local] '
                           '$protocol $status $bytes_sent $bytes_received '
                           '$session_time "$upstream_addr" '
                           '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';

        access_log /var/log/nginx/tcp-access.log  proxy;
        open_log_file_cache off;

        upstream kokossh {
            # core web 节点
            server 192.168.100.21:2222;
            server 192.168.100.22:2222;
            least_conn;
        }

        server {
            listen 2222;
            proxy_pass kokossh;
            proxy_protocol on;
            proxy_connect_timeout 1s;
        }
    }

    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';

        access_log  /var/log/nginx/access.log  main;

        sendfile        on;
        #tcp_nopush     on;

        keepalive_timeout  65;

        #gzip  on;

        include /etc/nginx/conf.d/*.conf;
    }
    ```
    ```sh
    echo > /etc/nginx/conf.d/default.conf
    vi /etc/nginx/conf.d/jumpserver.conf
    ```
    ```nginx
    upstream core_web {
        # 用户连接时使用 ip_hash 负载
        server 192.168.100.21:8080;
        server 192.168.100.22:8080;
        ip_hash;
    }

    upstream core_media {
        # 获取录像失败时自动到对应的 server 取
        server 192.168.100.21:8080 max_fails=2 fail_timeout=2s;
        server 192.168.100.22:8080 max_fails=2 fail_timeout=2s;
        server 192.168.100.31:8080 max_fails=2 fail_timeout=2s;
    }

    upstream core_task {
        # use_task = 1 的任务服务器, 目前只能单任务运行
        server 192.168.100.31:8080;
    }

    server {
        listen 80;
        server_name demo.jumpserver.org;  # 自行修改成你的域名
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name          demo.jumpserver.org;  # 自行修改成你的域名
        ssl_certificate      /etc/nginx/sslkey/1_jumpserver.org.crt;  # 自行设置证书
        ssl_certificate_key  /etc/nginx/sslkey/2_jumpserver.org.key;  # 自行设置证书
        ssl_session_timeout  5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;

        client_max_body_size 4096m;  # 录像上传大小限制

        location ~ /(ops|task|tasks|flower|ws)/ {
            proxy_pass http://core_task;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location ~ /replay/ {
            proxy_pass http://core_media;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504 http_404;
            proxy_next_upstream_tries 5;
        }

        location / {
            proxy_pass http://core_web;
            proxy_buffering  off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log off;
        }
    }
    ```
    ```sh
    nginx -t
    ```

!!! tip "启动 Nginx"
    ```sh
    systemctl enable nginx
    systemctl start nginx
    ```

!!! tip "配置防火墙"
    ```sh
    firewall-cmd --permanent --zone=public --add-port=80/tcp
    firewall-cmd --permanent --zone=public --add-port=443/tcp
    firewall-cmd --permanent --zone=public --add-port=2222/tcp
    firewall-cmd --reload
    ```

## 部署 MinIO 服务

    服务器: 192.168.100.41

!!! tip "安装 Docker"
    ```sh
    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
    yum makecache fast
    yum -y install docker-ce
    ```

!!! tip "配置 Docker"
    ```sh
    mkdir /etc/docker/
    vi /etc/docker/daemon.json
    ```
    ```vim
    {
      "live-restore": true,
      "registry-mirrors": ["https://hub-mirror.c.163.com", "https://bmtrgdvx.mirror.aliyuncs.com", "http://f1361db2.m.daocloud.io"],
      "log-driver": "json-file",
      "log-opts": {"max-file": "3", "max-size": "10m"}
    }
    ```

!!! tip "下载 MinIO 镜像"
    ```sh
    docker pull minio/minio:latest
    ```
    ```vim
    latest: Pulling from minio/minio
    a591faa84ab0: Pull complete
    76b9354adec6: Pull complete
    f9d8746550a4: Pull complete
    890b1dd95baa: Pull complete
    3a8518c890dc: Pull complete
    8053f0501aed: Pull complete
    506c41cb8532: Pull complete
    Digest: sha256:e7a725edb521dd2af07879dad88ee1dfebd359e57ad8d98104359ccfbdb92024
    Status: Downloaded newer image for minio/minio:latest
    docker.io/minio/minio:latest
    ```

!!! tip "持久化数据目录"
    ```sh
    mkdir -p /opt/jumpserver/minio/data /opt/jumpserver/minio/config
    ```

!!! tip "启动 MinIO"
    ```vim
    ## 请自行修改账号密码并牢记, 丢失后可以删掉容器后重新用新密码创建, 数据不会丢失
    # 9000                                  # 访问端口
    # MINIO_ROOT_USER=minio                 # minip 账号
    # MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q  # minio 密码
    ```
    ```sh
    docker run --name jms_minio -d -p 9000:9000 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=KXOeyNgDeTdpeu9q -v /opt/jumpserver/minio/data:/data -v /opt/jumpserver/minio/config:/root/.minio minio/minio:latest server /data
    ```

!!! tip "设置 MinIO"
    - 访问 http://192.168.100.41:9000, 输入刚才设置的 MinIO 账号密码登录
    - 点击右下角的 + 号, 选择 Create bucket 创建桶, Bucket Name 输入 jumpserver 回车确认

!!! tip "设置 JumpServer"
    - 访问 JumpServer Web 页面并使用管理员账号进行登录
    - 点击左侧菜单栏的 [终端管理], 在页面的上方选择 [存储配置], 在 [录像存储] 下方选择 [创建] 选择 [Ceph]
    - 根据下方的说明进行填写, 保存后在 [终端管理] 页面对所有组件进行 [更新], 录像存储选择 [jms-mino], 提交

| 选项            | 参考值                      | 说明                |
| :-------------  | :------------------------- | :------------------ |
| 名称 (Name)     | jms-minio                  | 标识, 不可重复       |
| 类型 (Type)     | Ceph                       | 固定, 不可更改       |
| 桶名称 (Bucket) | jumpserver                 | Bucket Name         |
| Access key      | minio                      | MINIO_ROOT_USER     |
| Secret key      | KXOeyNgDeTdpeu9q           | MINIO_ROOT_PASSWORD |
| 端点 (Endpoint) | http://192.168.184.41:9000 | minio 服务访问地址   |
