# MySQL 应用要求

!!! warning "MySQL Server 需要授权 Core 和 KoKo 的远程访问的权限"
    ```sh
    mysql -uroot
    ```
    ```mysql
    grant all on *.* to 'root'@'%' identified by 'Test2020.M';
    flush privileges;
    ```

!!! warning "注意防火墙放行相应的 MySQL 服务端口"
