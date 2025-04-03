# ComfyUI-WebhookNotifier

ComfyUI的Webhook通知插件，用于在图像生成完成时发送webhook通知。

## 功能特点

- 在生成图像后自动发送webhook通知
- 通知中包含图像数量、尺寸等基本信息
- 支持传递ComfyUI的unique_id、prompt和extra_pnginfo
- 可添加自定义附加信息
- 简单易用，只需连接图像输出即可

## 安装方法

1. 克隆此仓库到ComfyUI的`custom_nodes`目录：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/yourusername/ComfyUI-WebhookNotifier.git
```

2. 安装依赖项：

```bash
pip install -r requirements.txt
```

3. 重启ComfyUI服务

## 使用方法

插件提供了 Webhook Notifier 节点，可以连接到图像输出，当生成完成时发送通知。

参数说明：
- `images`: 输入图像（必填，连接到图像生成节点的输出）
- `webhook_url`: Webhook URL地址（必填，默认为"https://example.com/webhook"）
- `additional_info`: 附加信息，JSON格式（可选，默认为空）

## Webhook通知格式

WebhookNotifier节点发送的数据格式示例：

```json
{
  "status": "completed",
  "timestamp": "2023-04-03 15:30:45",
  "images": {
    "image_count": 1,
    "dimensions": "512x512"
  },
  "unique_id": "12345678-1234-5678-abcd-1234567890ab",
  "prompt": {...},
  "extra_pnginfo": {...},
  "custom_field1": "自定义值1",
  "custom_field2": "自定义值2"
}
```

其中：
- `status`: 始终为"completed"，表示任务完成
- `timestamp`: 任务完成的时间戳
- `images`: 包含图像数量和尺寸信息
- `unique_id`: ComfyUI的任务ID
- `prompt`: ComfyUI的完整提示信息
- `extra_pnginfo`: 来自ComfyUI的额外PNG信息
- 其他字段: 来自additional_info参数的自定义字段

## 示例

将图像生成节点的输出连接到WebhookNotifier节点的images输入，设置您的webhook URL，就可以在图像生成完成时收到通知。

## 调试

节点会打印调试信息，包括是否成功发送webhook通知，以及接收到的hidden参数情况。

## 许可证

MIT

## 贡献

欢迎提交问题和拉取请求！ 