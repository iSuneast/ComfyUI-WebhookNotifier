import requests
import json
import os
from pathlib import Path

# 加载配置文件
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    default_config = {
        "default_webhook_url": "https://example.com/webhook",
        "enable_debug_logs": True
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                return config
        else:
            # 如果配置文件不存在，创建一个默认配置
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=4)
            return default_config
    except Exception as e:
        print(f"加载配置文件出错: {str(e)}")
        return default_config

# 全局配置
CONFIG = load_config()

class WebhookNotifierNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "webhook_url": ("STRING", {"default": CONFIG.get("default_webhook_url", "https://example.com/webhook")}),
            },
            "optional": {
                "include_metadata": ("BOOLEAN", {"default": True}),
                "custom_payload": ("STRING", {"default": "{}", "multiline": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "notify"
    CATEGORY = "utils"

    def notify(self, images, webhook_url, include_metadata=True, custom_payload="{}"):
        try:
            # 这里我们需要获取生成的图片文件路径
            # 由于ComfyUI在这个阶段可能还没有保存图片，我们只能传递基本信息
            
            # 准备基本信息
            image_info = {
                "image_count": len(images),
                "dimensions": f"{images.shape[1]}x{images.shape[2]}"
            }
            
            # 构造payload
            try:
                base_payload = json.loads(custom_payload) if custom_payload else {}
            except json.JSONDecodeError:
                base_payload = {}
            
            # 合并信息
            payload = {
                **base_payload,
                "images": image_info
            }
            
            if include_metadata:
                # 添加更多可能的元数据
                payload["metadata"] = {
                    "timestamp": import_time_module(),
                    "shape": images.shape,
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
        
        # 返回原始图像，不做任何修改
        return (images,)


class SavedImageWebhookNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "saved_images": ("STRING", {"forceInput": True}),  # 接收SaveImage节点的输出
                "webhook_url": ("STRING", {"default": CONFIG.get("default_webhook_url", "https://example.com/webhook")}),
            },
            "optional": {
                "custom_payload": ("STRING", {"default": "{}", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify_saved"
    CATEGORY = "utils"
    
    def notify_saved(self, saved_images, webhook_url, custom_payload="{}"):
        try:
            # 解析保存的图片路径
            image_paths = saved_images.split(",") if isinstance(saved_images, str) else []
            image_paths = [p.strip() for p in image_paths if p.strip()]
            
            # 准备发送的信息
            try:
                base_payload = json.loads(custom_payload) if custom_payload else {}
            except json.JSONDecodeError:
                base_payload = {}
            
            # 构建包含图片路径的payload
            payload = {
                **base_payload,
                "image_paths": image_paths,
                "timestamp": import_time_module(),
                "total_images": len(image_paths)
            }
            
            # 记录调试信息
            if CONFIG.get("enable_debug_logs", False):
                print(f"正在发送webhook通知，图片路径: {image_paths}")
            
            # 发送webhook
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code >= 400:
                print(f"保存图片Webhook通知失败: {response.status_code} - {response.text}")
            else:
                print(f"保存图片Webhook通知成功: {response.status_code}")
                
        except Exception as e:
            print(f"发送保存图片webhook时出错: {str(e)}")
        
        # 返回原始的保存路径信息
        return (saved_images,)


# 导入time模块的辅助函数 - 避免全局导入
def import_time_module():
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S") 