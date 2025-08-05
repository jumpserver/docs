# 飞书认证

## 关于飞书

!!! info ""
    - **飞书** 认证是基于飞书平台的身份认证机制，允许企业和第三方应用程序通过飞书对用户进行身份认证和授权。

## 基础配置

!!! tip ""
    - 点击页面右上角的设置按钮
    - 导航到 **系统设置 > 认证设置 > 飞书**

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| 飞书 | 勾选启用飞书身份验证 | 启用/禁用 |
| App ID | 飞书 App ID，这是应用程序的唯一标识符 |  |
| App secret | 飞书应用程序密钥，类似于 API 访问的密码，用于获取调用飞书 API 的访问令牌 |   |
| 映射属性 | 用户属性映射。键表示 JumpServer 用户属性名称，值对应飞书用户属性名称 | 示例见下文 |
| 组织 | 经过身份认证和创建后，用户将被添加到所选组织中 | 默认值：`DEFAULT` |

飞书用户属性示例
!!! tip ""
    -  **映射属性** 字段用于设置用户属性映射。键表示 JumpServer 用户属性名称，值对应飞书用户属性名称。

```json
{
  "name": "nickname",
  "username": "user_id",
  "email": "email"
}
```

## 测试飞书连接
!!! tip ""
    - 点击页面右上角的设置按钮

    - 导航到 **系统设置 > 认证设置 > 飞书**

    - 滚动到页面底部。

    - 点击 **测试**。

## JumpServer 飞书 URLs
二维码登录 URL
```bash
https://jumpserver.example.com/core/auth/feishu/qr/login/
```
二维码登录成功回调 URL
```bash
https://jumpserver.example.com/core/auth/feishu/qr/login/callback/
```
