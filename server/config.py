# logic loop will work 50 times in second
LOOP_UPDATE_TIME = 0.02
# How often companies applies situation happend by news and make some progress or regress
COMPANY_NEWS_UPDATE = 12
# How often company recalculates self value, this is not related to news
COMPANY_COST_UPDATE = 6
# Maximum amount of open companies on the server
MAX_OPEN_COMPANIES_AMOUNT = 20
# Maximum amount of closed compnaies on the server
MAX_CLOSED_COMPANIES_AMOUNT = 10
# News generation time invterval
NEWS_GENERATION_TIME_DISPERSION = (3.0, 7.0)
# Start amount of money for new player
PLAYER_DEFAULT_MONEY_AMOUNT = 3000
# Amount of damping for news. If there is no update related to these type. How many circles need to be to decrease influence level.
NEWS_DAMPING_AMOUNT = 3
# When open company generated need to spicy amount of silver stocks
OPEN_COMPANY_DEFAULT_AMOUNT_SILVER_STOCKS = 50
