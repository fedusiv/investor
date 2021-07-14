PORT = 3002
KEEP_ALIVE_TIME = 2
KEEP_ALIVE_ERROR = 5
# logic loop will work 50 times in second
LOOP_UPDATE_TIME = 0.02
# How often companies applies situation happend by news and make some progress or regress
COMPANY_NEWS_UPDATE = 20
# How often company recalculates self value, this is not related to news
COMPANY_COST_UPDATE = 5
# Maximum amount of open companies on the server
MAX_OPEN_COMPANIES_AMOUNT = 10
# Maximum amount of closed compnaies on the server
MAX_CLOSED_COMPANIES_AMOUNT = 10
# News generation time invterval
NEWS_GENERATION_TIME_DISPERSION = (3.0, 7.0)
# Start amount of money for new player
PLAYER_DEFAULT_MONEY_AMOUNT = 3000
# Amount of damping for news. If there is no update related to these type. How many circles need to be to decrease influence level.
NEWS_DAMPING_AMOUNT = 3
# When open company generated need to spicy amount of silver stocks
OPEN_COMPANY_DEFAULT_AMOUNT_SILVER_STOCKS = 60
# Minimun amount of value of one stock to specify it, when create player company
MINIMUN_STOCK_VALUE_TO_CREATE = 0.01
# Closed compnaies has less depence on global news and world situation. This amount of less dependency persent
# Example rate 1.05, 50 persentage of rate will be 1.025 And 50% means 0.5
CLOSED_COMPANY_RATE_DECREASE = 0.5
# Fine multiplicator based on life cycles of company
WORKING_PLAN_FINE = 1000
# What amount of company can go to payback
INVESTMENT_COMPANY_VALUE_PAYBACK = 0.49
# Link to database and access password
DATABASE_LINK = "postgresql://postgres:ilya@localhost:5432/investor"
