# ComfyUI-WebhookNotifier

ComfyUI的Webhook通知插件，可以在工作流程执行完成时，将生成图片的信息发送到指定的Webhook URL。

## 功能特点

- 支持通知生成图像的基本信息
- 支持通知已保存图像的具体路径
- 支持自定义通知载荷（payload）
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

插件提供了两种节点：

### 1. Webhook Notifier

直接连接到图像输出，发送图像的基本信息。

参数说明：
- `images`: 输入图像（必填）
- `webhook_url`: Webhook URL地址（必填）
- `include_metadata`: 是否包含元数据（可选）
- `custom_payload`: 自定义JSON载荷（可选）

### 2. Saved Image Webhook

连接到SaveImage节点的输出，发送已保存图像的路径信息。

参数说明：
- `saved_images`: SaveImage节点的输出（必填）
- `webhook_url`: Webhook URL地址（必填）
- `custom_payload`: 自定义JSON载荷（可选）

## 示例工作流

1. 基本使用示例：
   - 将SaveImage节点连接到Saved Image Webhook节点
   - 设置webhook_url为你的接收端点
   - 运行工作流

2. 带自定义数据的示例：
   - 将自定义JSON设置为如下格式：
   ```json
   {
     "workflow_name": "我的测试工作流",
     "user_id": "user_123",
     "additional_info": "任何你想要的附加信息"
   }
   ```

## Webhook响应格式

SavedImageWebhook节点发送的数据格式示例：

```json
{
  "image_paths": ["/path/to/image1.png", "/path/to/image2.png"],
  "timestamp": "2023-04-03 15:30:45",
  "total_images": 2,
  "custom_field1": "自定义值1",
  "custom_field2": "自定义值2"
}
```

## 许可证

MIT

## 贡献

欢迎提交问题和拉取请求！ 