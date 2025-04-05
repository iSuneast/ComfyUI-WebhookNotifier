# ComfyUI-WebhookNotifier

Webhook notification plugin for ComfyUI, used to send webhook notifications when image generation is completed.

## Features

- Automatically sends webhook notifications after generating images
- Notifications include basic information such as image count, dimensions, etc.
- Supports passing ComfyUI's unique_id, prompt, and extra_pnginfo
- Can add custom additional information
- Simple to use, just connect to the image output

## Installation

1. Clone this repository to ComfyUI's `custom_nodes` directory:

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/yourusername/ComfyUI-WebhookNotifier.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Restart ComfyUI service

## Usage

The plugin provides a Webhook Notifier node that can be connected to image output to send notifications when generation is complete.

Parameter description:
- `images`: Input images (required, connect to the output of an image generation node)
- `webhook_url`: Webhook URL address (required, default is "https://example.com/webhook")
- `additional_info`: Additional information in JSON format (optional, default is empty)

## Webhook Notification Format

Example of data format sent by the WebhookNotifier node:

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
  "custom_field1": "Custom value 1",
  "custom_field2": "Custom value 2"
}
```

Where:
- `status`: Always "completed", indicating the task is finished
- `timestamp`: Timestamp of when the task completed
- `images`: Contains image count and dimension information
- `unique_id`: ComfyUI's task ID
- `prompt`: Complete prompt information from ComfyUI
- `extra_pnginfo`: Additional PNG information from ComfyUI
- Other fields: Custom fields from the additional_info parameter

## Example

Connect the output of an image generation node to the WebhookNotifier node's images input, set your webhook URL, and you will receive notifications when image generation is complete.

## Debugging

The node prints debug information, including whether the webhook notification was sent successfully and the status of received hidden parameters.

## License

MIT

## Contributions

Issues and pull requests are welcome! 