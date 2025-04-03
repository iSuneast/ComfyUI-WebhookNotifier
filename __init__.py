import importlib.util
import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

from .webhook_notifier import WebhookNotifierNode, SavedImageWebhookNode

NODE_CLASS_MAPPINGS["WebhookNotifierNode"] = WebhookNotifierNode
NODE_DISPLAY_NAME_MAPPINGS["WebhookNotifierNode"] = "Webhook Notifier"

NODE_CLASS_MAPPINGS["SavedImageWebhookNode"] = SavedImageWebhookNode
NODE_DISPLAY_NAME_MAPPINGS["SavedImageWebhookNode"] = "Saved Image Webhook" 