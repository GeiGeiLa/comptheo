import transitions
from transitions.extensions import GraphMachine
from utils import send_text_message
import utils
from linebot import LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import parse_weather
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    text = None

    # state1
    def is_going_to_state1(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "go to state1"

    def on_enter_state1(self, event):
        print("I'm entering state1")
        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        #self.go_back()

    def on_exit_state1(self, *args, **kwargs):
        print("Leaving state1")

    #state2
    def is_going_to_state2(self, event):
        self.text = event.message.text
        print(self.text)
        return (self.text).lower() == "go to state2"

    def on_enter_state2(self, event):
        print("I'm entering state2")
        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self, *args, **kwargs):
        print("Leaving state2")

    # go back
    def is_going_back(self, event):
        self.text = event.message.text
        return (self.text).lower() == "go back"
    def on_enter_user(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger user")
        #self.go_back()
        
    def on_exit_user(self, *args, **kwargs):
        print("Leaving user")
    
    # cat
    def can_see_cat(self, event):
        print("checking cat")
        is_cat = (event.message.text).lower() in ["cat", "kitty", "puma", "cats"]
        print(is_cat)
        return is_cat

    def on_enter_cat(self, event):
        print("enter cat")
        reply_token = event.reply_token
        utils.send_image_url(utils.userID, utils.MyImage.cat_url)
        send_text_message(reply_token, "Do you like this cat?")
    def on_exit_cat(self, *args, **kwargs):
        print("Goodbye from Messi the cougar.")
    
    # like cat answer
    def can_answer_cat(self, event):
        self.text = event.message.text
        return (self.text).lower() in ["like","yes","hate","no"]
    
    def on_enter_likecat(self, event):
        print("enter like cat?")
        reply_token = event.reply_token
        if self.text.lower() in ["hate","no"]:
            print("hate")
            send_text_message(reply_token, "So you are a dog person? Eat this!")
            utils.send_image_url(utils.userID, utils.MyImage.dog_url)
        else: 
            send_text_message(reply_token, "Alright")
    def on_exit_likecat(self, *args, **kwargs):
        print("Answer complete")
    
    # weather
    def is_toweather(self,event):
        self.text = event.message.text
        return (self.text).lower() == "weather" or self.text == "天氣"
    def on_enter_weather(self,event):
        print("into weather")
        reply_token = event.reply_token
        wb = Weatherbot()
        self.text = event.message.text
        response = wb.getResponse(self.text)
        print(response)
        send_text_message(reply_token,response)
        self.go_back()
    def on_exit_weather(self,event):
        print("bye bye weather")




    # def on_enter_(self, event):
    #     pass
    # def on_exit_(self, event):
    #     pass
    # def yourcondition(self, *args, **kwargs):
    #     pass

class Weatherbot(object):
    """
    實現 Echo 與應答天氣訊息的聊天機器人
    """

    def __init__(self):

        self.weather_parser = parse_weather.WeatherParser()
        self.taiwan_cities = ["臺北", "新北", "桃園", "臺中", "臺南",
                              "高雄", "基隆", "新竹", "嘉義", "新竹", "苗栗",
                              "彰化", "南投", "雲林", "嘉義", "屏東", "宜蘭",
                              "花蓮", "臺東", "澎湖", "金門", "連江"]

    def getResponse(self, sentence):
        sentence.replace("台", "臺")
        if "天氣" in sentence or "weather" in sentence.lower():
            location = self.getLocation(sentence)
            report = self.weather_parser.getReport(location)  # 依照地點取得該地今天的天氣
            response = "目前%s的天氣是%s" % (location, report)
        else:
            response = self.echo(sentence)
        return response

    def getLocation(self, sentence):
        """
        比對 sentence 與臺灣的 23 個,
        如果比對成功回傳該名, 否則回傳臺南
        """

        for city in self.taiwan_cities:
 
            if city in sentence:
                return city
        return "臺南"

    def echo(self, sentence):
        return sentence
