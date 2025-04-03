# ComfyUI-WebhookNotifier

ComfyUI的Webhook通知插件，可以在工作流程执行完成时，将生成图片的信息发送到指定的Webhook URL。

## 功能特点

- 支持通知生成图像的基本信息
- 支持通知已保存图像的具体路径
- **支持提供图片的下载链接**
- **支持在通知前自动保存图片**
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
- `base_url`: ComfyUI服务器的基础URL，默认为`http://localhost:8188`
- `output_dir`: 默认的图片输出目录，默认为`output`

## 使用方法

插件提供了两种节点：

### 1. Webhook Notifier

直接连接到图像输出，可以自动保存图片并发送图像信息和下载链接。

参数说明：
- `images`: 输入图像（必填）
- `webhook_url`: Webhook URL地址（必填）
- `include_metadata`: 是否包含元数据（可选）
- `custom_payload`: 自定义JSON载荷（可选）
- `base_url`: ComfyUI服务器的基础URL（可选，默认使用配置文件中的值）
- `save_images`: 是否保存图片（可选，默认为true）
- `filename_prefix`: 保存文件名前缀（可选，默认为"webhook_"）
- `output_dir`: 输出目录（可选，默认使用配置文件中的值）

此节点有两个输出：
1. `images`: 原始图像数据，可以连接到其他节点
2. `saved_paths`: 保存的图片路径，可以连接到其他需要文件路径的节点

### 2. Saved Image Webhook

连接到SaveImage节点的输出，发送已保存图像的路径信息和下载链接。

参数说明：
- `saved_images`: SaveImage节点的输出（必填）
- `webhook_url`: Webhook URL地址（必填）
- `custom_payload`: 自定义JSON载荷（可选）
- `base_url`: ComfyUI服务器的基础URL（可选，默认使用配置文件中的值）

## 示例工作流

1. 基本使用示例（不需要SaveImage节点）：
   - 将模型输出的图像连接到Webhook Notifier节点
   - 设置webhook_url为你的接收端点
   - 设置save_images为true
   - 运行工作流，图片会自动保存并发送通知

2. 与SaveImage节点配合使用：
   - 将SaveImage节点的输出连接到Saved Image Webhook节点
   - 设置webhook_url为你的接收端点
   - 运行工作流

3. 带自定义数据的示例：
   - 将自定义JSON设置为如下格式：
   ```json
   {
     "workflow_name": "我的测试工作流",
     "user_id": "user_123",
     "additional_info": "任何你想要的附加信息"
   }
   ```

## Webhook响应格式

WebhookNotifier节点发送的数据格式示例（当save_images=true时）：

```json
{
  "images": {
    "image_count": 1,
    "dimensions": "512x512"
  },
  "image_paths": ["/path/to/output/webhook_20230403-153045_abcd1234.png"],
  "download_links": ["http://localhost:8188/view?filename=output/webhook_20230403-153045_abcd1234.png"],
  "metadata": {
    "timestamp": "2023-04-03 15:30:45",
    "shape": [1, 512, 512, 3]
  },
  "custom_field1": "自定义值1",
  "custom_field2": "自定义值2"
}
```

SavedImageWebhook节点发送的数据格式示例：

```json
{
  "image_paths": ["/path/to/image1.png", "/path/to/image2.png"],
  "download_links": ["http://localhost:8188/view?filename=image1.png", "http://localhost:8188/view?filename=image2.png"],
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