# Render 环境变量配置指南

## 问题

当前服务出现错误：
1. `Request URL is missing an 'http://' or 'https://' protocol.` - 工作流URL配置错误
2. `{'errcode': 48001, 'errmsg': 'api unauthorized'}` - 客服消息API使用错误（已修复）

## 解决方案

### 步骤1：登录 Render Dashboard

1. 访问：https://dashboard.render.com/
2. 进入 `My project > Production > weixin-webhook`
3. 点击左侧菜单的 `Environment`

### 步骤2：添加环境变量

点击 "Add Environment Variable"，逐个添加以下变量：

| Key | Value | 类型 |
|-----|-------|------|
| `WEIXIN_TOKEN` | `GcFWzYhV0y8ktQuW` | 普通 |
| `WEIXIN_ENCODING_AES_KEY` | `Zj4JlbGom1eR8hNWPRJLi25YIS6UBTD551cyfq9n5In` | 普通 |
| `WEIXIN_APP_ID` | `wx6d76fe7674ec5657` | 普通 |
| `WEIXIN_APP_SECRET` | `e0ed88e6b89e4e1319dc220223b3096b` | 普通 |
| `COZE_WORKFLOW_URL` | `https://z2f493xmnp.coze.site/stream_run` | 普通 |
| `COZE_JWT_TOKEN` | `eyJhbGciOiJSUzI1NiIsImtpZCI6IjRhODQyODA2LWQwZGYtNDlmYS05ZDAxLWNhM2MyNDJkMWUyNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkNWWk1Fdkc4OXY3d2gzMlhNaWxhVlZLd3ZGQjVhZEhMIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2OTQ1NDY2LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI4NjA4Mzk2MDEwMTkyOTIyIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjMxOTIyNjYzOTM3NTQwMTIyIn0.mFSK0hO0eD2uSDPjS94BYoW6NpWNOXlr1oXgQ8nw5ph4y6TPCkn1oQjNiIoPgNzTTAUyf72mTVn3oWzqRHys4umjHm2QuNIgsVAdlYBUTWARJutHaJsTl8rHxZmFMHwqkv8vz7R5Kjo-SdpdLSSKZVwvMtOFTARkw9jxYOKPTtMBE9MR8k_TXdWUx73RwrO_DKUXbtO74RL1pBTHw-ZtttxAuK9G11huSAZn2E0ry-Bi6AI21_lV_HJhEJwYp870fdzdL2nPILdamM7Ye18bL-ZOUBOPQSI7lJmINmDjztyONP9F2n2629fk7pL8mEmw0WWqBp3XXnVE3292EKt-5Q` | 敏感 |

### 步骤3：重新部署

1. 添加完所有环境变量后
2. 点击右上角的 "Save Changes"
3. 等待自动部署完成（约2-3分钟）

### 步骤4：验证配置

部署完成后，查看日志：

```bash
# 在 Render Dashboard 的 Logs 页面
# 应该看到类似以下日志：
✅ 配置验证成功
✅ 扣子工作流API客户端初始化成功
```

## 注意事项

1. **COZE_JWT_TOKEN 必须选择"敏感"类型**
   - 在 Render 中，长字符串Token应该标记为敏感变量
   - 这样在日志中会被自动隐藏，防止泄露

2. **所有变量都要复制完整**
   - 尤其是 COZE_JWT_TOKEN，非常长，确保没有截断

3. **部署后自动生效**
   - 不需要手动重启，添加环境变量后会自动部署

## 测试

配置完成后：

1. 通过微信发送测试消息（例如："你好"）
2. 在 Render Dashboard 查看 Logs
3. 应该看到：
   - 消息解密成功
   - 工作流API调用成功
   - AI回复生成
   - 客服消息发送成功（如果权限正常）

## 如果仍然有问题

### 问题1：工作流URL错误
```
Request URL is missing an 'http://' or 'https://' protocol.
```
- 检查 `COZE_WORKFLOW_URL` 是否包含 `https://` 前缀
- 确保没有多余的空格

### 问题2：客服消息权限错误
```
errcode: 48001, errmsg: api unauthorized
```
- 可能需要在微信小店后台开通"自研客服"功能
- 或联系微信客服申请权限

### 问题3：AI返回默认消息
```
如果您没有其他问题的话，本次对话就结束啦...
```
- 这是工作流的默认结束消息
- 需要在扣子平台配置工作流的对话逻辑
