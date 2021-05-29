from typing import TypedDict

from news.news_element import NewsElement
from news.news_types import InfluenceStage
from news.news_types import NewsTypes
import config

class SituationElement():
    @property
    def type(self)-> NewsTypes:
        return self.__type

    @property
    def influence_level(self)-> InfluenceStage:
        return self.__inf_level

    def __init__(self, t: NewsTypes):
        self.__type : NewsTypes = t
        self.__counter = config.NEWS_DAMPING_AMOUNT # Update counter, when it comes to zero news level decreases
        self.__inf_level = InfluenceStage.NONE

    def update_value(self, inf: InfluenceStage):
        if self.__inf_level.value < inf.value:
            # New event has bigger influence level
            self.__inf_level = inf
            self.__counter = config.NEWS_DAMPING_AMOUNT # Default value of changes period
        else:
            self.empty_update()

    # Damping influence operation
    def empty_update(self):
        if self.influence_level.value == 0:
            # Already low, operation is not required
            return
        self.__counter -= 1
        if self.__counter <= 0:
            # decrease influce level
            self.__inf_level = InfluenceStage(self.__inf_level.value - 1)

class SituationStorage(TypedDict):
    war : SituationElement
    science : SituationElement
    entertainment : SituationElement
    social : SituationElement

class WorldSituation():

    @property
    def situation(self):
        return self.__situation

    def __init__(self):
        # Create situation default
        self.__situation = SituationStorage(war=SituationElement(NewsTypes.WAR),
                                            science=SituationElement(NewsTypes.SCIENCE),
                                            entertainment=SituationElement(NewsTypes.ENTERTAINMENT),
                                            social=SituationElement(NewsTypes.SOCIAL)
                                            )

    def change_situation(self, event : NewsElement):
        string_repr = event.news_type.name.lower()
        cur_situation = self.__situation[string_repr]
        cur_situation.update_value(event.influence_level)
        # For others make empty update
        for element in self.__situation.values():
            element : SituationElement
            if element.type != cur_situation.type:
                element.empty_update()
        self.print_world_situation()

    # Return list of influnce levels only for required news types
    def required_influence_types_level(self, interested_types: list):
        req = []
        for t in interested_types:
            t: NewsTypes
            cur = self.get_situation_by_type(t)
            req.append(cur.influence_level)
        return req

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
