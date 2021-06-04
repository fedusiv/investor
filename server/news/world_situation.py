from typing import TypedDict

from companies.bussines_news_connection import NewsDependency
from news.news_element import NewsElement
from news.news_types import NewsTypes
import config

class SituationElement():
    @property
    def type(self)-> NewsTypes:
        return self.__type

    @property
    def influence_level(self)-> int:
        return self.__inf_level

    def __init__(self, t: NewsTypes):
        self.__type : NewsTypes = t
        self.__counter = config.NEWS_DAMPING_AMOUNT # Update counter, when it comes to zero news level decreases
        self.__inf_level : int = 0

    def update_value(self, inf: int):
        if self.__inf_level < inf:
            # New event has bigger influence level
            self.__inf_level = inf
            self.__counter = config.NEWS_DAMPING_AMOUNT # Default value of changes period
        else:
            # No need to do anything. if current level of influence is same or less, we just give one more loop of current values
            pass
            #self.empty_update()

    # Damping influence operation
    def empty_update(self):
        if self.influence_level == 0:
            # Already low, operation is not required
            return
        self.__counter -= 1
        if self.__counter <= 0:
            # decrease influce level
            self.__inf_level -= 1

class SituationStorage(TypedDict):
    war : SituationElement
    science : SituationElement
    entertainment : SituationElement
    social : SituationElement
    hardware : SituationElement
    financial : SituationElement
    graphics : SituationElement

class WorldSituation():

    @property
    def situation(self):
        return self.__situation

    def __init__(self):
        # Create situation default
        # TODO: Fix this fucking mess with situation storage initialization!
        self.__situation = SituationStorage(war=SituationElement(NewsTypes.WAR),
                                            science=SituationElement(NewsTypes.SCIENCE),
                                            entertainment=SituationElement(NewsTypes.ENTERTAINMENT),
                                            social=SituationElement(NewsTypes.SOCIAL),
                                            hardware=SituationElement(NewsTypes.HARDWARE),
                                            financial=SituationElement(NewsTypes.FINANCIAL),
                                            graphics=SituationElement(NewsTypes.GRAPHICS)
                                            )

    def change_situation(self, event : NewsElement):
        string_repr = event.news_type.name.lower()
        cur_situation = self.__situation[string_repr]
        cur_situation.update_value(event.influence_level)
        # For others make empty update
        # Pylance is arguing on element in loop, I do not know why. If you know why - fix it
        for element in self.__situation.values():
            element : SituationElement
            if element.type != cur_situation.type:
                element.empty_update()

    # Return influence level for given news dependency
    def required_influence_types_level(self, news_dependency: NewsDependency) -> int:
        level = 0
        # Positive affects increase level value
        for p in news_dependency.pos :
            level += self.get_situation_by_type(p).influence_level
        # Negative affects decrease level value
        for n in news_dependency.neg :
            level -= self.get_situation_by_type(n).influence_level
        return level

    def get_situation_by_type(self,t : NewsTypes) -> SituationElement:
        string = t.name.lower()
        s = self.__situation[string]
        return s

    #############################
    # Debug Server Methods
    #############################

    def print_world_situation(self):
        print("World Situation")
        for key in self.__situation:
            element : SituationElement
            element = self.__situation[key]
            print("\t",key, " ",element.influence_level)
