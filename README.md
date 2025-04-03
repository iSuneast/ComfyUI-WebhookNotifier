# ComfyUI-WebhookNotifier

ComfyUI的Webhook通知插件，可以在工作流程执行完成时，发送任务完成的通知。

## 功能特点

- 在生成图像后发送完成通知
- 通知中包含当前工作流的prompt ID
- 支持自定义通知内容
- 可配置默认Webhook URL

## 安装方法

1. 克隆此仓库到ComfyUI的`custom_nodes`目录：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/yourusername/ComfyUI-WebhookNotifier.git
```

2. 安装依赖项：

```bash
pip install requests
```

3. 重启ComfyUI服务

## 配置说明

插件提供了`config.json`文件，可以在其中设置：

- `default_webhook_url`: 默认的Webhook URL
- `enable_debug_logs`: 是否启用调试日志

## 使用方法

插件提供了 Webhook Notifier 节点，可以连接到图像输出，当生成完成时发送通知。

参数说明：
- `images`: 输入图像（必填）
- `webhook_url`: Webhook URL地址（必填）
- `workflow_name`: 工作流名称（可选）
- `additional_info`: 自定义JSON载荷（可选）

## Webhook响应格式

WebhookNotifier节点发送的数据格式示例：

```json
{
  "status": "completed",
  "prompt_id": "12345678",
  "workflow_name": "我的测试工作流",
  "timestamp": "2023-04-03 15:30:45",
  "images": {
    "image_count": 1,
    "dimensions": "512x512"
  },
  "custom_field1": "自定义值1",
  "custom_field2": "自定义值2"
}
```

## 许可证

MIT

## 贡献

欢迎提交问题和拉取请求！ 