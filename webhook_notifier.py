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
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT", 
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "notify"
    CATEGORY = "utils"

    def notify(self, images, webhook_url, additional_info="{}", extra_pnginfo=None, unique_id=None, prompt=None):
        try:
            # 准备基本信息
            image_info = {
                "image_count": len(images),
                "dimensions": f"{images.shape[1]}x{images.shape[2]}"
            }
            
            # 尝试解析额外信息
            try:
                extra_info = json.loads(additional_info) if additional_info else {}
            except json.JSONDecodeError:
                extra_info = {}
            
            # 构造payload
            payload = {
                "status": "completed",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "images": image_info,
                "unique_id": unique_id,
                "prompt": prompt,
                "extra_pnginfo": extra_pnginfo,
                **extra_info
            }
            
            # 调试信息
            print(f"Debug - 获取到的hidden参数:")
            print(f"- unique_id: {unique_id}")
            print(f"- prompt: {type(prompt)}")
            print(f"- extra_pnginfo: {type(extra_pnginfo)}")
            
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