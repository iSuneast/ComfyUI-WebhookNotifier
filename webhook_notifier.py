import requests
import json
import os
from pathlib import Path
import urllib.parse
import uuid
import time
import numpy as np
from PIL import Image

# 加载配置文件
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    default_config = {
        "default_webhook_url": "https://example.com/webhook",
        "enable_debug_logs": True,
        "base_url": "http://localhost:8188",
        "output_dir": "output"  # 添加默认输出目录
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                # 确保config中包含必要的字段
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
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
                "base_url": ("STRING", {"default": CONFIG.get("base_url", "http://localhost:8188")}),
                "save_images": ("BOOLEAN", {"default": True}),
                "filename_prefix": ("STRING", {"default": "webhook_"}),
                "output_dir": ("STRING", {"default": CONFIG.get("output_dir", "output")}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "saved_paths")
    FUNCTION = "notify"
    CATEGORY = "utils"

    def notify(self, images, webhook_url, include_metadata=True, custom_payload="{}", 
              base_url=None, save_images=True, filename_prefix="webhook_", output_dir=None):
        try:
            # 如果未提供base_url和output_dir，则使用配置中的默认值
            if not base_url:
                base_url = CONFIG.get("base_url", "http://localhost:8188")
            if not output_dir:
                output_dir = CONFIG.get("output_dir", "output")
                
            # 确保base_url没有尾部斜杠
            base_url = base_url.rstrip('/')
            
            # 准备基本信息
            image_info = {
                "image_count": len(images),
                "dimensions": f"{images.shape[1]}x{images.shape[2]}"
            }
            
            saved_paths = []
            download_links = []
            
            # 如果需要保存图片
            if save_images:
                try:
                    # 确保输出目录存在
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # 为每张图片生成唯一文件名并保存
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    
                    for i in range(len(images)):
                        # 生成文件名
                        unique_id = str(uuid.uuid4())[:8]
                        filename = f"{filename_prefix}{timestamp}_{unique_id}.png"
                        filepath = os.path.join(output_dir, filename)
                        
                        # 将numpy数组转换为PIL图像并保存
                        img = Image.fromarray((images[i] * 255).astype(np.uint8))
                        img.save(filepath)
                        
                        # 记录保存的路径
                        saved_paths.append(filepath)
                        
                        # 生成下载链接
                        encoded_path = urllib.parse.quote(os.path.join(os.path.basename(output_dir), filename))
                        download_url = f"{base_url}/view?filename={encoded_path}"
                        download_links.append(download_url)
                        
                    if CONFIG.get("enable_debug_logs", False):
                        print(f"图片已保存到: {saved_paths}")
                        print(f"下载链接: {download_links}")
                        
                except Exception as e:
                    print(f"保存图片时出错: {str(e)}")
            
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
            
            # 如果已保存图片，添加路径和下载链接
            if save_images and saved_paths:
                payload["image_paths"] = saved_paths
                payload["download_links"] = download_links
            
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
        
        # 返回原始图像和保存的路径（逗号分隔的字符串）
        return (images, ",".join(saved_paths))


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
                "base_url": ("STRING", {"default": CONFIG.get("base_url", "http://localhost:8188")}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify_saved"
    CATEGORY = "utils"
    
    def notify_saved(self, saved_images, webhook_url, custom_payload="{}", base_url=None):
        try:
            # 如果未提供base_url，则使用配置中的默认值
            if not base_url:
                base_url = CONFIG.get("base_url", "http://localhost:8188")
            
            # 确保base_url没有尾部斜杠
            base_url = base_url.rstrip('/')
                
            # 解析保存的图片路径
            image_paths = saved_images.split(",") if isinstance(saved_images, str) else []
            image_paths = [p.strip() for p in image_paths if p.strip()]
            
            # 准备下载链接
            download_links = []
            for path in image_paths:
                # 获取相对于ComfyUI输出文件夹的路径
                try:
                    # 假设路径格式为绝对路径，需要提取相对于output目录的部分
                    relative_path = path
                    if os.path.isabs(path):
                        # 尝试找到output目录的位置
                        output_dir = None
                        parts = Path(path).parts
                        for i, part in enumerate(parts):
                            if part == "output":
                                output_dir = os.path.join(*parts[:i+1])
                                relative_path = os.path.join(*parts[i+1:])
                                break
                    
                    # 使用URL编码处理文件路径
                    encoded_path = urllib.parse.quote(relative_path)
                    # 构建完整的下载URL
                    download_url = f"{base_url}/view?filename={encoded_path}"
                    download_links.append(download_url)
                except Exception as e:
                    print(f"处理图片路径时出错: {str(e)}")
                    # 如果出错，至少提供原始路径
                    download_links.append(path)
            
            # 准备发送的信息
            try:
                base_payload = json.loads(custom_payload) if custom_payload else {}
            except json.JSONDecodeError:
                base_payload = {}
            
            # 构建包含图片路径和下载链接的payload
            payload = {
                **base_payload,
                "image_paths": image_paths,
                "download_links": download_links,  # 添加下载链接
                "timestamp": import_time_module(),
                "total_images": len(image_paths)
            }
            
            # 记录调试信息
            if CONFIG.get("enable_debug_logs", False):
                print(f"正在发送webhook通知，图片路径: {image_paths}")
                print(f"下载链接: {download_links}")
            
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