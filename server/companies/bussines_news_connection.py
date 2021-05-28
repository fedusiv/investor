# Set depencency of news types and types of business
# What news types affect to chosen business type

from companies.companies_types import CompanyBusinessType
from news.news_types import NewsTypes


class BusinessNewsRelation():

    @staticmethod
    def military_business_relation()-> list:
        war_dependece = NewsTypes.WAR
        depencency = [war_dependece]
        return depencency


    @staticmethod
    def empty_relation()-> list:
        l = []
        return l

    @staticmethod
    def business_news_relation(b_type : CompanyBusinessType):
        switcher = {
            CompanyBusinessType.MILITARY : BusinessNewsRelation.military_business_relation
        }
        func = switcher.get(b_type,BusinessNewsRelation.empty_relation)
        l_r = func()
        return l_r

