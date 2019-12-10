import os
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError

userID = "U0ad3a8e167be131b57735b3073d1eb27"

accesstoken = "qg4eVtnYir36ZcCSDNZyXyy+lpyDaM9Py1YIGzlvdsd82IUPYSfIZoLaYHroMQC7agDi2c3iI6JndkMgM9GwRHUqnilvhranozggoKPKug8wW7NaM5eUvJ6qWgQNqm6U/wHaLUtfVp63gSVOBi/9BQdB04t89/1O/w1cDnyilFU="
weatherkey = "CWB-EECDE765-431A-4E99-BE52-2FD6E7E33631"
MyImage = {'cat': "https://static.boredpanda.com/blog/wp-content/uploads/2019/02/zoo-rescued-puma-house-cat-messi-russia-13.jpg",
           'dog': "https://www.washingtonpost.com/resizer/kPkFQsQjvSIjfXG-mFXDEpxq6-4=/767x0/smart/arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/HB4AT3D3IMI6TMPTWIZ74WAR54.jpg"
          }




def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(accesstoken)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def get_env_variable(var):
    try:
        return os.environ[var]
    except KeyError:
        print("Environment var '%s' not found." % var)


def send_image_url(id, img_url):
    line_bot_api = LineBotApi(accesstoken)
    try:
        line_bot_api.push_message(id, ImageSendMessage(
            original_content_url=img_url, preview_image_url=img_url))
        return "OK image"
    except LineBotApiError:
        line_bot_api.push_message(id, TextSendMessage(text = "Canot send image"))
"""
def send_button_message(id, text, buttons):
    pass
"""
