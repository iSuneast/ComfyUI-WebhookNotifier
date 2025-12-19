import importlib.util
import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

from .webhook_notifier import WebhookNotifierNode, WebhookNotifierAnyNode

NODE_CLASS_MAPPINGS["WebhookNotifierNode"] = WebhookNotifierNode
NODE_DISPLAY_NAME_MAPPINGS["WebhookNotifierNode"] = "Webhook Notifier"

NODE_CLASS_MAPPINGS["WebhookNotifierAnyNode"] = WebhookNotifierAnyNode
NODE_DISPLAY_NAME_MAPPINGS["WebhookNotifierAnyNode"] = "Webhook Notifier (Any)"