import requests
import json
import time
import copy

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
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "execution_id": "EXECUTION_ID",
                "unique_id": "UNIQUE_ID",
                "my_unique_id": "MY_UNIQUE_ID",
                "id": "ID",
                "inputs": "INPUTS",
                "outputs": "OUTPUTS"
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "notify"
    CATEGORY = "utils"

    def notify(self, images, webhook_url, workflow_name="默认工作流", additional_info="{}", 
               prompt=None, extra_pnginfo=None, execution_id=None, unique_id=None, 
               my_unique_id=None, id=None, inputs=None, outputs=None):
        try:
            # 从ComfyUI获取prompt_id (client_id)
            prompt_id = "unknown"
            
            # 尝试从各种来源获取client_id
            if prompt is not None and "client_id" in prompt:
                prompt_id = prompt["client_id"]
            elif execution_id is not None:
                prompt_id = execution_id
            elif prompt is not None and "extra_pnginfo" in prompt and "workflow" in prompt["extra_pnginfo"]:
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
            
            # 准备hidden参数数据
            hidden_data = {}
            
            # 安全地复制prompt (可能会非常大，只取部分关键信息)
            if prompt is not None and isinstance(prompt, dict):
                safe_prompt = {
                    "keys_available": list(prompt.keys())
                }
                if "client_id" in prompt:
                    safe_prompt["client_id"] = prompt["client_id"]
                hidden_data["prompt"] = safe_prompt
            
            # 添加其他hidden参数
            if extra_pnginfo is not None:
                hidden_data["extra_pnginfo"] = extra_pnginfo
            if execution_id is not None:
                hidden_data["execution_id"] = execution_id
            if unique_id is not None:
                hidden_data["unique_id"] = unique_id
            if my_unique_id is not None:
                hidden_data["my_unique_id"] = my_unique_id
            if id is not None:
                hidden_data["id"] = id
            if inputs is not None:
                # 安全处理inputs（可能包含大型张量等）
                if isinstance(inputs, dict):
                    hidden_data["inputs"] = {k: str(type(v)) for k, v in inputs.items()}
                else:
                    hidden_data["inputs"] = str(type(inputs))
            if outputs is not None:
                hidden_data["outputs"] = outputs
            
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
            print(f"- prompt类型: {type(prompt)}")
            print(f"- extra_pnginfo: {type(extra_pnginfo)}")
            print(f"- execution_id: {execution_id}")
            print(f"- unique_id: {unique_id}")
            print(f"- my_unique_id: {my_unique_id}")
            print(f"- id: {id}")
            print(f"- inputs类型: {type(inputs)}")
            print(f"- outputs类型: {type(outputs)}")
            
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