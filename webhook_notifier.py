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
                "workflow_name": ("STRING", {"default": "默认工作流"}),
                "additional_info": ("STRING", {"default": "{}", "multiline": True})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "notify"
    CATEGORY = "utils"

    def notify(self, images, webhook_url, workflow_name="默认工作流", additional_info="{}", prompt=None):
        try:
            # 从ComfyUI获取prompt_id (execution_id)
            prompt_id = "unknown"
            if prompt is not None and "extra_pnginfo" in prompt and "workflow" in prompt["extra_pnginfo"]:
                if "execution_id" in prompt["extra_pnginfo"]["workflow"]:
                    prompt_id = prompt["extra_pnginfo"]["workflow"]["execution_id"]
                elif "client_id" in prompt["extra_pnginfo"]["workflow"]:
                    prompt_id = prompt["extra_pnginfo"]["workflow"]["client_id"]
            
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
                "prompt_id": prompt_id,
                "workflow_name": workflow_name,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "images": image_info,
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
                print(f"Webhook通知成功: {response.status_code}, prompt_id: {prompt_id}")
                
        except Exception as e:
            print(f"发送webhook时出错: {str(e)}")
        
        # 返回原始图像
        return (images,) 