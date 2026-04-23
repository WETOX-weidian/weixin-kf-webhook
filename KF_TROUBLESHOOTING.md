# 微信小店客服消息问题排查指南

## 当前问题

所有客服消息API端点都返回错误：

| API端点 | 错误码 | 错误信息 |
|---------|--------|----------|
| `cgi-bin/message/custom/send` | 48001 | api unauthorized |
| `shop/kf/message/send` | 40066 | invalid url |
| `shop/kf/send` | 40066 | invalid url |
| `wxa/business/kf/send` | 40066 | invalid url |

## 错误码说明

### 40066 - invalid url
**可能原因**：
1. 微信小店未开启"自研客服"功能
2. API端点与微信小店版本不匹配
3. 需要特殊的店铺ID或认证信息
4. 微信小店配置未完成

### 48001 - api unauthorized
**可能原因**：
1. 公众号/小程序没有开通客服消息权限
2. API调用权限不足
3. 需要在微信公众平台申请权限

## 解决方案

### 方案1：开启微信小店自研客服功能（推荐）

#### 步骤1：登录微信小店管理后台
- 访问：https://shop.weixin.qq.com/
- 使用管理员账号登录

#### 步骤2：开启自研客服
1. 进入【店铺管理】→【客服管理】
2. 找到【接入自研客服】入口
3. 按照指引完成配置

#### 步骤3：配置回调地址
1. 在自研客服配置中填写回调URL
2. 回调URL格式：`https://你的域名/webhook/weixin`
3. 点击"验证"按钮

#### 步骤4：获取必要的配置信息
- 客服账号
- 店铺ID（shopid）
- API密钥（如果有）

### 方案2：使用微信小店提供的客服工具

如果自研客服功能无法使用，可以考虑：

1. **使用微信小店内置客服系统**
   - 不需要开发
   - 直接在微信小店后台管理
   - 适合小型店铺

2. **使用第三方客服系统**
   - 有很多成熟的第三方客服系统
   - 通常提供微信小程序/小店的集成
   - 可以快速上线

### 方案3：改用订阅消息（备选方案）

如果客服消息API确实无法使用，可以考虑：

1. **使用订阅消息**
   - 需要在微信公众平台申请订阅消息模板
   - 用户需要主动订阅
   - 适合发送通知类消息

2. **使用模板消息**
   - 类似订阅消息
   - 但使用场景不同

## 调试步骤

### 1. 确认微信小店配置

在微信小店管理后台检查：
- [ ] 是否开启了"自研客服"功能
- [ ] 回调URL是否正确配置
- [ ] 回调URL是否验证通过
- [ ] 客服账号是否设置

### 2. 检查API权限

在微信公众平台检查：
- [ ] 小程序是否有客服消息权限
- [ ] 是否有调用相关API的权限
- [ ] IP白名单是否配置（如果需要）

### 3. 测试API调用

可以使用在线调试工具：
- 微信公众平台在线调试：https://developers.weixin.qq.com/debug
- 或者使用Postman等工具直接测试

### 4. 查看官方文档

参考文档：
- 微信小店客服API：https://developers.weixin.qq.com/doc/store/shop/API/kf/api_sendmsg.html
- 微信小店自研客服接入指引：https://developers.weixin.qq.com/doc/store/shop/product/kf/kf_api_guidelines

## 临时解决方案

在客服消息问题解决之前，可以考虑：

1. **将AI回复保存到日志**
   - 记录所有AI回复
   - 后续可以通过日志查看对话内容

2. **使用其他通知方式**
   - 邮件通知
   - 短信通知
   - 站内信

3. **定期检查对话记录**
   - 通过微信公众平台查看客服对话记录
   - 人工回复

## 代码建议

在客服消息发送失败时，可以添加更好的错误处理：

```python
def send_text(self, to_user: str, text: str) -> bool:
    access_token = self._get_access_token()
    if not access_token:
        logger.error("无法获取access_token")
        return False

    url = f"{self.base_url}/shop/kf/message/send?access_token={access_token}"

    data = {
        "touser": to_user,
        "msgtype": "text",
        "text": {
            "content": text
        }
    }

    try:
        response = httpx.post(url, json=data, timeout=10)
        result = response.json()

        errcode = result.get("errcode")
        errmsg = result.get("errmsg")

        if errcode == 0:
            logger.info(f"发送客服消息成功: to_user={to_user}, text={text[:50]}...")
            return True
        else:
            # 详细的错误日志
            logger.error(f"发送客服消息失败: errcode={errcode}, errmsg={errmsg}")
            logger.error(f"完整响应: {result}")

            # 根据错误码给出建议
            if errcode == 40066:
                logger.error("错误码40066：可能是微信小店未开启自研客服功能")
                logger.error("请检查微信小店管理后台的客服配置")
            elif errcode == 48001:
                logger.error("错误码48001：API未授权")
                logger.error("请在微信公众平台申请客服消息权限")

            return False

    except Exception as e:
        logger.error(f"发送客服消息异常: {e}")
        return False
```

## 联系微信客服

如果以上方案都无法解决问题：

1. **提交工单**
   - 在微信公众平台提交技术支持工单
   - 详细描述问题现象
   - 提供错误码和日志

2. **咨询客服**
   - 联系微信小店的客服
   - 询问自研客服功能的开通流程

3. **社区提问**
   - 在微信开发者社区提问
   - 参考类似问题的解决方案

## 总结

当前问题是微信小店客服消息API返回 `errcode: 40066 (invalid url)`，这通常意味着：

1. **微信小店未开启自研客服功能**（最可能）
2. API端点或参数格式不正确
3. 缺少必要的店铺ID或认证信息

**建议优先检查微信小店管理后台的自研客服配置。**
