# Set depencency of news types and types of business
# What news types affect to chosen business type

from companies.companies_types import CompanyBusinessType
from news.news_types import NewsTypes

class NewsDependency():
    def __init__(self):
        self.pos = None
        self.neg = None
        pass

    # Apply positive depencency of a news
    def set_positive(self, dep: list):
        self.pos = dep

    # Apply negativer depencency from a news
    def set_negative(self, dep: list):
        self.neg = dep

# Class describe how business types relates to appeared news
# Positive affect means, that if this news type has positive meaning compnay will have positive affect
# Negative affect means, that if this news type has positive meaning company will have negative affect
# TODO remove all these relation setup from code to text file representation, to better and easier gameplay changes
class BusinessNewsRelation():

    @staticmethod
    def create_dependency(positive: list, negative: list) -> NewsDependency:
        dependency = NewsDependency()
        dependency.set_positive(positive)
        dependency.set_negative(negative)
        return dependency

    @staticmethod
    def military_business_relation()-> NewsDependency:
        pos = [NewsTypes.WAR]
        neg = [NewsTypes.SOCIAL]
        dependency = BusinessNewsRelation.create_dependency(pos,neg)
        return dependency

    @staticmethod
    def game_dev_relation() -> NewsDependency:
        pos = [NewsTypes.ENTERTAINMENT, NewsTypes.GRAPHICS]
        neg = [NewsTypes.WAR]
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def science_relation() -> NewsDependency:
        pos = [NewsTypes.SCIENCE]
        neg = [NewsTypes.FINANCIAL]
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def fintech_relation() -> NewsDependency:
        pos = [NewsTypes.FINANCIAL]
        neg = [NewsTypes.WAR]
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def socialtech_relation() -> NewsDependency:
        pos = [NewsTypes.SOCIAL]
        neg = [NewsTypes.SCIENCE]
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def automotive_relation() -> NewsDependency:
        pos = [NewsTypes.SCIENCE, NewsTypes.HARDWARE]
        neg = []
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def graphicsvideo_relation() -> NewsDependency:
        pos = [NewsTypes.ENTERTAINMENT, NewsTypes.GRAPHICS, NewsTypes.HARDWARE]
        neg = [NewsTypes.WAR]
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def mobileapp_relation() -> NewsDependency:
        pos = [NewsTypes.ENTERTAINMENT, NewsTypes.SOCIAL, NewsTypes.HARDWARE]
        neg = [NewsTypes.FINANCIAL, NewsTypes.WAR]
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def securitytech_relation() -> NewsDependency:
        pos = [NewsTypes.WAR, NewsTypes.FINANCIAL]
        neg = []
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def outsource_relation() -> NewsDependency:
        pos = [NewsTypes.FINANCIAL]
        neg = [NewsTypes.WAR]
        dep = BusinessNewsRelation.create_dependency(pos,neg)
        return dep

    @staticmethod
    def empty_relation()-> NewsDependency:
        dep = NewsDependency()
        return dep

    @staticmethod
    def business_news_relation(b_type : CompanyBusinessType) -> NewsDependency:
        switcher = {
            CompanyBusinessType.Military : BusinessNewsRelation.military_business_relation,
            CompanyBusinessType.GameDev : BusinessNewsRelation.game_dev_relation,
            CompanyBusinessType.Science : BusinessNewsRelation.science_relation,
            CompanyBusinessType.FinancialTech : BusinessNewsRelation.fintech_relation,
            CompanyBusinessType.Social : BusinessNewsRelation.socialtech_relation,
            CompanyBusinessType.Automotive : BusinessNewsRelation.automotive_relation,
            CompanyBusinessType.GraphicsVideo : BusinessNewsRelation.graphicsvideo_relation,
            CompanyBusinessType.MobileApplication : BusinessNewsRelation.mobileapp_relation,
            CompanyBusinessType.Security : BusinessNewsRelation.securitytech_relation,
            CompanyBusinessType.Outsource : BusinessNewsRelation.outsource_relation
       }
        func = switcher.get(b_type,BusinessNewsRelation.empty_relation)
        dep = func()
        return dep

