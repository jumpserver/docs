# Interactive Commands

!!! warning "Improper operation will result in data loss. Please confirm carefully before operating."

## 1 Operation Method

!!! tip ""
    ```sh
    docker exec -it jms_core bash
    cd /opt/jumpserver/apps
    python manage.py shell
    ```
    ```python
    # Starting from the new version, you need to switch to the corresponding organization before operating. Default is 'Default'
    from orgs.models import *
    Organization.objects.all()
    org = Organization.objects.get(name='Default')
    org.change_to()
    ```

!!! tip ""
    - Select the interactive command object to view

    === "User"
        ```python
        from users.models import *

        # User
        User.objects.all()
        User.objects.count()  # Count

        # Query specific user
        user = User.objects.get(username = 'admin')

        # Query user email
        user.email

        # Modify user email
        user.email='test@jumpserver.org'

        # Change password
        user.reset_password('test01')

        # Save modifications
        user.save()

        # Delete user MFA key
        user.otp_secret_key=''
        user.save()

        # Create new user
        User.objects.create(name = 'Test User', username = 'test', email = 'test@jumpserver.org')

        # Test if user exists, create if not
        User.objects.get_or_create(name = 'Test User', username = 'test', email = 'test@jumpserver.org')

        user = User.objects.get(username = 'test')
        user.delete()

        # More elegant deletion method
        User.objects.all().filter(username='test').delete()
        ```
        ```python
        # User groups
        UserGroup.objects.all()
        UserGroup.objects.count()

        # Create user group
        UserGroup.objects.create(name = 'Test')
        ```
    
    === "Asset"
        ```python
        from assets.models import *

        # Asset
        Asset.objects.all()
        Asset.objects.count()

        # Query asset by name
        asset = Asset.objects.get(name='asset_name')

        # Modify asset
        asset.address='192.168.1.100'
        asset.save()

        # Delete asset
        asset.delete()
        ```


## 2 Data Decryption
!!! tip ""

    === "System User"
        ```sh
        docker exec -it jms_core python manage.py shell
        from assets.models import SystemUser
        su = SystemUser.objects.all().first()
        print(su.password)
        ```
    
    === "System Settings Fields"
        ```sh
        docker exec -it jms_core python manage.py shell
        from settings.models import Setting
        setting = Setting.objects.get(name='EMAIL_PASSWORD')
        print(setting.value)
        ```
