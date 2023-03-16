# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from time import sleep
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

api = {
    "北京": [{"city": "上海", "date": "上午", "ticket_number": "123"},
           {"city": "长沙", "date": "下午", "ticket_number": "456"},
           {"city": "深圳", "date": "中午", "ticket_number": "678"}]
}

from_city_flag = 0
from_city = ''
to_city_flag = 0
to_city = ''
date = ''
date_flag = 0


class ActionBookTicket(Action):

    def name(self) -> Text:
        return "action_book_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global from_city_flag
        global to_city_flag
        global date_flag
        global from_city
        global to_city
        global date
        # 获取识别过来的实体值
        for entity in tracker.latest_message['entities']:
            # dispatcher.utter_message(text=str(entity))
            # dispatcher.utter_message(text="1")
            if entity.get('entity') == 'city':
                # dispatcher.utter_message(text="2")
                # 判断是否已获取
                # 判别实体值是否存在
                if entity.get("value") is not None:
                    # dispatcher.utter_message(text="6")
                    if entity.get("role") == "from":
                        # dispatcher.utter_message(text="4")
                        from_city = entity.get("value")
                        from_city_flag = 1
                    else:
                        to_city = entity.get("value")
                        to_city_flag = 1
            else:
                # dispatcher.utter_message(text="3")
                if entity.get("value") is not None:
                    # dispatcher.utter_message(text="5")
                    date = entity.get("value")
                    date_flag = 1
        # 查API
        if from_city_flag == 1 and to_city_flag == 1 and date_flag == 1:
            dispatcher.utter_message(text="稍等，正在查询中。。。")

            for ticket in api.get(from_city):
                if ticket.get("city") == to_city:
                    if ticket.get("date") == date:

                        dispatcher.utter_message(text="已查询到相关信息，票号为:"
                                                      + ticket.get("ticket_number") +
                                                      '\n' + "请问您确定要购买吗")

                        break
                    else:

                        dispatcher.utter_message(text="没有" + date + "的票")
                        break
            else:
                dispatcher.utter_message(text="没有从" + from_city + "到" + to_city + "的票")
        else:
            if from_city_flag == 0:
                dispatcher.utter_message(text="请说出出发地点或完整的信息，如：“我想订一张上午从北京到上海的机票”")
            elif to_city_flag == 0:
                dispatcher.utter_message(text="请说出目的地信息，如：“我想订一张到上海的机票”")
            else:
                dispatcher.utter_message(text="请说出时间，如：“我想订一张下午的机票”")

        return []

