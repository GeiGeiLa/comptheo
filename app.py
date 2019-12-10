
import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import platform
from fsm import TocMachine
from utils import send_text_message
import parse_weather
mStates = ["user", "state1", "state2", "cat", "likecat", "weather"]

load_dotenv()
print(platform.python_version())
accesstoken = "qg4eVtnYir36ZcCSDNZyXyy+lpyDaM9Py1YIGzlvdsd82IUPYSfIZoLaYHroMQC7agDi2c3iI6JndkMgM9GwRHUqnilvhranozggoKPKug8wW7NaM5eUvJ6qWgQNqm6U/wHaLUtfVp63gSVOBi/9BQdB04t89/1O/w1cDnyilFU="
secret = "48da0c6234a4fca127ccaae491c55dbf"
weatherkey = "CWB-EECDE765-431A-4E99-BE52-2FD6E7E33631"

all_none_init_states = ["state1", "state2", "cat","likecat","weather"]

try: 
    machine = TocMachine(
        states = mStates,
        transitions=
        [
            {
                "trigger": "advance",
                "source": "user",
                "dest": "state1",
                "conditions": "is_going_to_state1",
            },
            {
                "trigger": "advance",
                "source": "user",
                "dest": "state2",
                "conditions": "is_going_to_state2",
            },
            {
                "trigger":"go_back",
                "source":all_none_init_states,
                "dest":"user",
            },
            {
                "trigger": "advance", 
                "source":  all_none_init_states,
                "dest": "user",
                "conditions": "is_going_back"
            },
            {
                "trigger": "advance",
                "source": "user",
                "dest": "cat",
                "conditions": "can_see_cat"
            },
            {
                "trigger": "advance",
                "source": "cat",
                "dest":"likecat",
                "conditions":"can_answer_cat"
            },
            {
                "trigger": "advance",
                "source": "user",
                "dest": "weather",
                "conditions":"is_toweather",
            },
        ],
        initial="user",
        auto_transitions=False,
        show_conditions=True,
    )
except:
    print("Error occured")


app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
if secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if accesstoken is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(accesstoken)
parser = WebhookParser(secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    mdoby = "Request body"+body
    app.logger.info(mdoby)
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        # if(event.message.text.lower() == "draw"):
        #     show_fsm()
        if not isinstance(event.message.text, str):
            continue
        print("\nFSM STATE: "+machine.state)
        print("REQUEST BODY: \n"+body)
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Bad command")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")



if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port, debug=True)
