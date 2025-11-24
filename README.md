# ComfyUI-WebhookNotifier

Webhook notification plugin for ComfyUI, used to send webhook notifications when image generation is completed.

## Features

- Automatically sends webhook notifications after generating images
- Supports custom JSON data in notifications
- Provides two nodes:
  - `Webhook Notifier`: connect to an `IMAGE` output as a trigger
  - `Webhook Notifier (VHS)`: connect to a `VHS_FILENAMES` output as a trigger

## Installation

1. Clone this repository to ComfyUI's `custom_nodes` directory:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/iSuneast/ComfyUI-WebhookNotifier.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Restart ComfyUI service

## Usage

The plugin provides a Webhook Notifier node that can be connected to image output to send notifications when generation is complete.

Parameter description:
- `images`: Trigger input (required, can connect to an `IMAGE` output or a `VHS_FILENAMES` output; the data is **not** read or sent, only used as a trigger)
- `webhook_url`: Webhook URL address (required, default is "https://example.com/webhook")
- `additional_info`: Additional information in JSON format (optional, default is empty)

## Webhook Notification Format

The WebhookNotifier node sends the contents of the `additional_info` parameter as the JSON payload. **Note that the image data itself is not included in the webhook payload**. The node only requires the image input to trigger the notification when image generation is complete.

For example, if you provide the following in the additional_info field:

```json
{
  "status": "completed",
  "custom_field1": "Custom value 1",
  "custom_field2": "Custom value 2"
}
```

This exact JSON will be sent to the webhook URL. If the additional_info field is left empty or contains invalid JSON, an empty JSON object `{}` will be sent.

## Example

Connect the output of an image generation node (type `IMAGE`) or a VHS/VideoHelperSuite node (type `VHS_FILENAMES`) to the WebhookNotifier node's `images` input, set your webhook URL, and optionally provide additional information in JSON format. When generation is complete and this node is executed, it will send a POST request to the specified webhook URL with your custom data.

## Debugging

The node prints debug information to the console, including whether the webhook notification was sent successfully:
- "Webhook notification started in background" when the webhook thread is started
- "Webhook notification successful: [status code]" for successful requests
- "Webhook notification failed: [status code] - [response text]" for failed requests
- "Error sending webhook: [error message]" for exceptions
- "Error preparing webhook: [error message]" if there are errors before sending

## License

MIT

## Contributions

Issues and pull requests are welcome!