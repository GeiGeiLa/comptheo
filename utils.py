import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage


accesstoken = "qg4eVtnYir36ZcCSDNZyXyy+lpyDaM9Py1YIGzlvdsd82IUPYSfIZoLaYHroMQC7agDi2c3iI6JndkMgM9GwRHUqnilvhranozggoKPKug8wW7NaM5eUvJ6qWgQNqm6U/wHaLUtfVp63gSVOBi/9BQdB04t89/1O/w1cDnyilFU="


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(accesstoken)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
