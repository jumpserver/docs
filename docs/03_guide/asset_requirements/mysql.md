# MySQL 应用要求

!!! warning "注意"
    - 注意防火墙放行相应的 MySQL 服务端口
    - MySQL Server 需要授权 Core 和 KoKo 的远程访问的权限

    ```sh
    mysql -uroot
    ```
    ```mysql
    create user 'root'@'%' identified by 'Test2020.M';
    grant all on *.* to 'root'@'%';
    flush privileges;
    ```
