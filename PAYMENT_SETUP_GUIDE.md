# 支付接口集成配置指南

## 概述

本系统已成功集成了微信支付和支付宝的官方接口，支持真实的在线支付功能。

## 当前状态

### ✅ 已完成
- 安装了官方支付SDK (`wechatpy`, `python-alipay-sdk`)
- 创建了支付配置管理类 (`payment_config.py`)
- 重构了支付处理逻辑，使用真实API
- 实现了支付回调处理机制
- 支持微信扫码支付和支付宝网页支付
- 添加了支付状态查询功能
- 创建了支付处理页面，支持二维码展示

### 📝 配置文件
- `.env` - 包含所有支付配置参数
- `payment_config.py` - 支付处理核心类
- `templates/user/payment_process.html` - 支付处理页面

## 生产环境配置步骤

### 1. 微信支付配置

```bash
# 在 .env 文件中配置真实参数
WECHAT_APP_ID=wx1234567890abcdef          # 微信公众号/小程序AppID
WECHAT_MCH_ID=1234567890                   # 商户号
WECHAT_MCH_KEY=your32digitmerchantkey      # 商户密钥
WECHAT_NOTIFY_URL=https://yourdomain.com/payment/wechat/notify  # 回调地址
WECHAT_RETURN_URL=https://yourdomain.com/payment/success        # 返回地址
WECHAT_SANDBOX=false                       # 生产环境设为false
```

### 2. 支付宝配置

```bash
# 在 .env 文件中配置真实参数
ALIPAY_APP_ID=2021000000000000            # 支付宝应用ID
ALIPAY_NOTIFY_URL=https://yourdomain.com/payment/alipay/notify  # 回调地址
ALIPAY_RETURN_URL=https://yourdomain.com/payment/success        # 返回地址
ALIPAY_SANDBOX=false                      # 生产环境设为false

# 密钥配置（需要替换为真实密钥）
ALIPAY_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...
-----END PRIVATE KEY-----

ALIPAY_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----
```

## 支付流程说明

### 微信支付流程
1. 用户点击"微信支付"按钮
2. 系统调用微信支付API创建订单
3. 生成支付二维码展示给用户
4. 用户扫码支付
5. 微信异步通知支付结果
6. 系统更新订单状态

### 支付宝支付流程
1. 用户点击"支付宝支付"按钮
2. 系统调用支付宝API创建订单
3. 直接跳转到支付宝支付页面
4. 用户完成支付
5. 支付宝异步通知支付结果
6. 系统更新订单状态

## 回调地址配置

### 重要提醒
- 回调地址必须是外网可访问的HTTPS地址
- 本地开发可以使用内网穿透工具（如ngrok）
- 生产环境必须配置真实的域名

### 内网穿透示例（开发环境）
```bash
# 使用ngrok创建隧道
ngrok http 5000

# 获得临时域名后，更新.env文件
WECHAT_NOTIFY_URL=https://abcd1234.ngrok.io/payment/wechat/notify
ALIPAY_NOTIFY_URL=https://abcd1234.ngrok.io/payment/alipay/notify
```

## 测试验证

### 开发环境测试
- 当前配置为沙箱模式，不会真实扣款
- 可以使用测试账号进行支付测试
- 所有交易都是虚拟的

### 生产环境验证
1. 小额测试：先进行小金额真实支付测试
2. 回调验证：确保支付回调正常处理
3. 状态同步：验证订单状态正确更新
4. 错误处理：测试各种异常情况

## 安全建议

1. **密钥管理**
   - 生产环境密钥不要提交到版本控制
   - 使用环境变量或安全的配置管理

2. **HTTPS配置**
   - 生产环境必须使用HTTPS
   - 配置有效的SSL证书

3. **回调验证**
   - 严格验证支付回调签名
   - 防止伪造支付通知

4. **日志记录**
   - 记录所有支付相关操作
   - 保留支付日志用于排查问题

## 常见问题

### Q: 支付回调没有收到？
A: 检查以下几点：
- 回调地址是否外网可访问
- 是否使用HTTPS（生产环境必须）
- 服务器防火墙配置
- 回调接口是否正常响应

### Q: 签名验证失败？
A: 检查以下几点：
- 密钥是否正确配置
- 字符编码是否一致
- 参数排序是否正确

### Q: 支付成功但订单状态未更新？
A: 检查以下几点：
- 回调处理逻辑是否正确
- 数据库连接是否正常
- 是否有异常被捕获但未处理

## 技术支持

如果遇到问题，可以：
1. 查看应用日志 (`logs/app.log`)
2. 检查支付平台的开发者文档
3. 使用支付平台提供的调试工具

## 文件结构

```
项目根目录/
├── payment_config.py                    # 支付配置和处理类
├── .env                                 # 环境配置文件
├── app.py                              # 主应用（包含支付路由）
└── templates/user/
    ├── payment.html                    # 支付页面
    ├── payment_process.html            # 支付处理页面
    └── payment_success.html            # 支付成功页面
```

## 版本信息

- 微信支付SDK: wechatpy 1.8.18
- 支付宝SDK: python-alipay-sdk 3.3.0
- 支持的支付方式: 微信扫码支付、支付宝网页支付
- 最后更新: 2025-09-20