import json
import random
import time

class CompanyNameGenerator():

    @staticmethod
    def name_generate() -> str:
        name = ''
        addon = ''
        with open("companies/CompaniesBrandNames.json") as names:
            data= json.load(names)
            # Naming
            first_elements = data["elements"]
            random.seed(time.time())
            first_amount = random.randint(2,4)
            names_list = random.choices(first_elements,k = first_amount)
            name = ''.join(names_list)
            name = name.capitalize()
            # Additional
            if first_amount != 4:
                add_elements = data["addons"]
                random.seed(time.time())
                addon = random.choice(add_elements)

        full_name = name + " " + addon
        return full_name
