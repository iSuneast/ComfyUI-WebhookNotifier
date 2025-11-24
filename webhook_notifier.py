import requests
import json
import time
import threading

class WebhookNotifierNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("*",),
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

    def send_webhook(self, webhook_url, payload):
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

    def notify(self, images, webhook_url, additional_info="{}"):
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
                target=self.send_webhook, 
                args=(webhook_url, payload),
                daemon=True
            ).start()
            print("Webhook notification started in background")
                
        except Exception as e:
            print(f"Error preparing webhook: {str(e)}")
        
        # No return value
        return () 