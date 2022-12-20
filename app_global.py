
from linebot import (
    LineBotApi, WebhookHandler
)
import os

line_bot_api = LineBotApi(os.environ['CH_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CH_SECRET'])
APP_URL = os.environ.get('APP_URL', None)
