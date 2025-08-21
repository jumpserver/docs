# Lark 认证

## 关于 Lark
!!! info "注: Lark 认证方式为 JumpServer 企业版功能。"
!!! tip ""
    - 进入 **系统设置**，点击 **认证设置 > Lark**，进入 Lark 配置页面。
    - **Lark** 认证是 Lark(国际版飞书)提供的一种身份认证机制，使企业和第三方应用程序能够通过 Lark 对用户进行身份认证和授权。

## 基础配置

!!! tip ""
    - 点击页面右上角的设置按钮
    - 导航到 **系统设置 > 认证设置 > Lark**

!!! tip ""
    详细参数说明：

| 参数 | 说明 | 示例 |
|------|------|------|
| Lark | 勾选启用 Lark 身份验证 | 启用/禁用 |
| App ID | Lark App ID，这是应用程序的唯一标识符 |  |
| App secret | Lark 应用程序密钥，用于获取调用 Lark API 的访问令牌 |   |
| 映射属性 | 用户属性映射。键表示 JumpServer 用户属性名称，值对应 Lark 用户属性名称 | 示例见下文 |
| 组织 | 经过身份认证和创建后，用户将被添加到所选组织中 | 默认值：`DEFAULT` |

Lark 用户属性示例
!!! tip ""
    -  **映射属性** 字段用于设置用户属性映射。键表示 JumpServer 用户属性名称，值对应 Lark 用户属性名称。

```json
{
  "name": "nickname",
  "username": "user_id",
  "email": "email"
}
```

## JumpServer Lark URL 说明

| URL 类型 | 地址 | 说明 |
|----------|------|------|
| 二维码登录 URL | `https://jumpserver.example.com/core/auth/lark/qr/login/` | Lark 二维码登录入口 |
| 二维码登录回调 URL | `https://jumpserver.example.com/core/auth/lark/qr/login/callback/` | 二维码登录成功回调地址 |
