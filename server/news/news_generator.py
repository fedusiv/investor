import json
import random
import time


class GeneratorElement():
    def __init__(self, chance, content, n_type):
        self.chance = chance
        self.content = content
        self.n_type = n_type

# Module handle the generation of news.
class NewsGenerator():
    # Singleton part
    __instance = None

    @staticmethod
    def Instance():
        if NewsGenerator.__instance == None:
            NewsGenerator()
        return NewsGenerator.__instance

    def __init__(self):
        NewsGenerator.__instance = self
        # Probably dict is not good decision to keep Data from NewsList.json because GeneratorElement also store news type string
        # If you are reading this and have time - fix it and upgrade
        self.__storage = {}

        # Init elements and chances values
        with open("news/NewsList.json") as type_names:
            data = json.load(type_names)
            news_dict = data["news"]
            keys_amount = len(news_dict.keys())
            type_chance = 1 / keys_amount
            for key in news_dict:
                # Generate element of storage for current types of news
                el = GeneratorElement(type_chance, news_dict[key],key)
                # Store this element
                self.__storage[key] = el



    ##############
    # Logic Part #
    ##############

    def request_element(self):
        random.seed(time.time())
        weight = list()
        # Get weight
        for item in self.__storage.values():
            weight.append(item.chance)

        # Get element
        el = random.choices(list(self.__storage.values()),weight,k=1)
        element = el[0]
        # Update chances
        for item in self.__storage.values():
            if item == element:
                continue
            item.chance += 0.01
        # Decrease chanse of current chosen element
        element.chance = element.chance - (len(weight) - 1) / 100
        event_list = random.choice(list(element.content))
        return element.n_type, event_list

    #################
    # Debug methods #
    #################

    # print data about current state of storage
    def print_generator_data(self):
        for key in self.__storage:
            print("Type : ", key, " chance: ", self.__storage[key].chance)

