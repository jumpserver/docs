# Storage Settings

!!! tip ""
    - Click the gear icon in the top-right corner to enter the **System Settings** page, then click **Storage Settings** to open the storage settings page.
    - The storage settings page mainly configures settings for JumpServer recording storage, account backup, and command storage.
  
## 1 Object Storage

!!! tip ""
    - The object storage page allows you to customize where JumpServer stores session recordings when connecting to assets. Currently supported external recording storage includes Amazon S3 cloud storage, Ceph, Swift, OSS, Azure, OBS, COS.
    - SFTP storage only supports account backup server.
  
!!! info "Note: Account backup and SFTP storage are enterprise features"

## 2 Command Storage

!!! tip ""
    - The command storage page allows you to change where JumpServer stores session command logs when connecting to assets. By default, asset session command logs are stored in JumpServer's database. Currently supported external command storage includes Elasticsearch.
    - Elasticsearch host format: `http://es_user:es_password@es_host:es_port`.
    - If creating index by date is enabled, the input value will be used as the index prefix.
