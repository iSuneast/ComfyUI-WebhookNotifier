import requests
import json
import time

class WebhookNotifierNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "webhook_url": ("STRING", {"default": "https://example.com/webhook"})
            },
            "optional": {
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

    def notify(self, images, webhook_url, additional_info="{}"):
        try:
            # 尝试解析额外信息
            try:
                extra_info = json.loads(additional_info) if additional_info else {}
            except json.JSONDecodeError:
                extra_info = {}
            
            # 构造payload
            payload = {
                **extra_info
            }
            
            # 发送webhook
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code >= 400:
                print(f"Webhook通知失败: {response.status_code} - {response.text}")
            else:
                print(f"Webhook通知成功: {response.status_code}")
                
        except Exception as e:
            print(f"发送webhook时出错: {str(e)}")
        
        # 不返回任何内容
        return () 