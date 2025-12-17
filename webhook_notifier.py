import requests
import json
import threading


def send_webhook_request(webhook_url, payload):
    """
    发送 webhook 请求的通用函数，供各个节点复用。
    """
    # 如果 webhook_url 为空或仅包含空白字符，则直接返回，不发送请求
    if not webhook_url or not str(webhook_url).strip():
        print("Webhook URL is empty, skip sending webhook.")
        return

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code >= 400:
            print(f"Webhook notification failed: {response.status_code} - {response.text}")
        else:
            print(f"Webhook notification successful: {response.status_code}")
    except Exception as e:
        print(f"Error sending webhook: {str(e)}")

class WebhookNotifierNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "webhook_url": ("STRING", {"default": "https://example.com/webhook"})
            },
            "optional": {
                # 通配符，接受任意类型作为触发输入
                "any_input": ("*",),
                "additional_info": ("STRING", {"default": "{}", "multiline": True})
            },
            "hidden": {
            }
        }

    OUTPUT_NODE = True

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "notify"
    CATEGORY = "utils"

    def notify(self, webhook_url, any_input=None, additional_info="{}"):
        try:
            # Try to parse additional information
            try:
                extra_info = json.loads(additional_info) if additional_info else {}
            except json.JSONDecodeError:
                extra_info = {}
            
            # Construct payload
            payload = {
                **extra_info
            }
            
            # Start the webhook sending in a background thread
            threading.Thread(
                target=send_webhook_request, 
                args=(webhook_url, payload),
                daemon=True
            ).start()
            print("Webhook notification started in background")
                
        except Exception as e:
            print(f"Error preparing webhook: {str(e)}")
        
        # No return value
        return () 