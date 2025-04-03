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
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "notify"
    CATEGORY = "utils"

    def notify(self, images, webhook_url, workflow_name="默认工作流", additional_info="{}", extra_pnginfo=None):
        try:
            # 从ComfyUI获取prompt_id (client_id)
            prompt_id = "unknown"
            
            # 尝试从extra_pnginfo获取client_id
            if extra_pnginfo is not None and "workflow" in extra_pnginfo:
                if "execution_id" in extra_pnginfo["workflow"]:
                    prompt_id = extra_pnginfo["workflow"]["execution_id"]
                elif "client_id" in extra_pnginfo["workflow"]:
                    prompt_id = extra_pnginfo["workflow"]["client_id"]
            
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
            
            # 准备hidden参数数据
            hidden_data = {}
            
            # 添加extra_pnginfo参数
            if extra_pnginfo is not None:
                hidden_data["extra_pnginfo"] = extra_pnginfo
            
            # 构造payload
            payload = {
                "status": "completed",
                "prompt_id": prompt_id,
                "workflow_name": workflow_name,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "images": image_info,
                "hidden_params": hidden_data,
                **extra_info
            }
            
            # 调试信息
            print(f"Debug - 获取到的hidden参数:")
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
                print(f"Webhook通知成功: {response.status_code}, prompt_id: {prompt_id}")
                
        except Exception as e:
            print(f"发送webhook时出错: {str(e)}")
        
        # 返回原始图像
        return (images,) 