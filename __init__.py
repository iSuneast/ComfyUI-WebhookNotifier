import importlib.util
import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

from .webhook_notifier import WebhookNotifierNode

NODE_CLASS_MAPPINGS["WebhookNotifierNode"] = WebhookNotifierNode
NODE_DISPLAY_NAME_MAPPINGS["WebhookNotifierNode"] = "Webhook Notifier" 