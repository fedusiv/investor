import json
import random
import time

from companies.companies_types import CompanyBusinessType

class CompanyNameGenerator():

    @staticmethod
    def name_generate(b_type : CompanyBusinessType) -> str:
        with open("companies/BusinessTypeNames.json") as type_names:
            data = json.load(type_names)
            names_list = data[b_type.name]
            random.seed(time.time())
            type_name = random.choice(names_list)
        with open("companies/CompaniesOwnerNames.json") as names:
            data = json.load(names)
            random.seed(time.time())
            first_name = random.choice(data["FirstName"])
            random.seed(time.time())
            second_name = random.choice(data["SecondName"])
        
        full_name = type_name + " of " + first_name + " " + second_name
        return full_name
