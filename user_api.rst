API 文档
==========================

Api 地址说明
---------------------------

http://HOST:PORT/api/{VERSION}/{APP}/{RESOURCE}/
http://HOST:PORT/api/{VERSION}/{APP}/{RESOURCE}/{RESOURCEID}/

如:

- 资产列表

    http://localhost/api/v1/assets/assets/

- 资产详情

    http://localhost/api/v1/assets/assets/2c56fd37-db65-40ed-b787-b65a98635f12/



Api 列表
------------------------------

通过访问 http://Jumpserver的URL地址/docs 来访问(如 http://192.168.244.144/docs)

注：需要打开 debug 模式

.. code-block:: shell

    $ vi jumpserver/config.yml

    ...
    DEBUG: true


.. image:: _static/img/api_swagger.jpg

