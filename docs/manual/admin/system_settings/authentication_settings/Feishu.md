# 飞书认证

## 关于飞书

!!! info "注: 飞书认证方式为 JumpServer 企业版功能。"
!!! tip ""
    - 进入 **系统设置** 页面，点击 **认证设置 > 飞书**，进入飞书配置页面。
    - **飞书认证** 是基于飞书平台的身份认证方法，JumpServer 支持二维码登录和企业身份绑定。

## 基础配置

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
!!! tip "属性映射示例"

```json
{
  "name": "nickname",
  "username": "user_id",
  "email": "email"
}
```

## JumpServer 飞书 URL 说明

| URL 类型 | 地址 | 说明 |
|----------|------|------|
| 二维码登录 URL | `https://jumpserver.example.com/core/auth/feishu/qr/login/` | 飞书二维码登录入口 |
| 二维码登录回调 URL | `https://jumpserver.example.com/core/auth/feishu/qr/login/callback/` | 二维码登录成功回调地址 |
