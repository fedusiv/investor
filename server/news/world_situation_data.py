from news.news_types import InfluenceStage
# Inforamtion element with world situation
class WorldSituationData():
    def __init__(self):
        self.war = InfluenceStage.NONE
        self.scince = InfluenceStage.NONE
        self.entertainment = InfluenceStage.NONE
        self.hardware = InfluenceStage.NONE
        self.social = InfluenceStage.NONE
