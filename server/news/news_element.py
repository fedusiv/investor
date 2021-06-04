import json
import time
import random

from news.news_types import NewsTypes

class NewsElement():
    def __init__(self, server_time: float):
        self.time = server_time
        with open("news/NewsList.json") as type_names:
            data = json.load(type_names)
            news_dict = data["news"]
            # Current event type and events list
            random.seed(time.time())
            event_type, event_list = random.choice(list(news_dict.items()))
            # Current event
            events_amount = len(event_list)
            event_id = random.randint(0,events_amount - 1) # -1 because index starts from 0
            event = event_list[event_id]
            # Apply points
            self.news_type : NewsTypes = self.str_to_news_type(event_type)
            self.influence_level = event["influence"]
            # Apply description
            self.theme = event["theme"]
            self.source = event["source"]

    # This method is better than default python one, because we need to have NONE type otherwise is something bad
    # Just additional safety level. If you can improve it, please improve
    def str_to_news_type(self, string: str) -> NewsTypes:
        switcher = {
            "war" : NewsTypes.WAR,
            "science" : NewsTypes.SCIENCE,
            "entertainment" : NewsTypes.ENTERTAINMENT,
            "social" : NewsTypes.SOCIAL,
            "hardware" : NewsTypes.HARDWARE,
            "financial" : NewsTypes.FINANCIAL,
            "graphics" : NewsTypes.GRAPHICS
        }
        cur_type = switcher.get(string,NewsTypes.NONE)
        return cur_type
