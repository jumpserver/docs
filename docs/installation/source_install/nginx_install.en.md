# Nginx Environment Deployment

## 1 Operation Process

!!! tip ""
    - Get the latest Nginx release from [Nginx][nginx] official website [linux_packages][linux_packages]. Verify installation completion via:
    ```bash
    nginx -v
    # nginx version: nginx/1.20.2
    ```

!!! tip ""
    - For CentOS/RHEL systems:
    ```bash
    yum install -y nginx
    systemctl start nginx
    systemctl enable nginx
    ```

!!! tip ""
    - For Ubuntu/Debian systems:
    ```bash
    apt-get update
    apt-get install -y nginx
    systemctl start nginx
    systemctl enable nginx
    ```

[nginx]: http://nginx.org/
[lina]: https://github.com/jumpserver/lina/
[linux_packages]: http://nginx.org/en/linux_packages.html
