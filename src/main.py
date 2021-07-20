import logging
from datetime import datetime

from numpy import random
import pandas as pd
import math

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from src.Supermarket import Supermarket
from src.queuechoicestrategy.QueueChoiceLeastPeople import QueueChoiceLeastPeople
from src.queuechoicestrategy.QueueChoiceLeastItems import QueueChoiceLeastItems
from src.queuechoicestrategy.QueueChoiceLeastWaitingTimeServiceImplied import QueueChoiceLeastWaitingTimeServiceImplied
from src.queuechoicestrategy.QueueChoiceLeastWaitingPowerImplied import QueueChoiceLeastWaitingPowerImplied

from src.queuejockeystrategy.QueueJockeyNoJockeying import QueueJockeyNoJockeying
from src.queuejockeystrategy.QueueJockeyLeastPeople import QueueJockeyLeastPeople
from src.queuejockeystrategy.QueueJockeyLeastItems import QueueJockeyLeastItems

# colors
RED = "#eb3461"
BLUE = "#3493eb"
GREEN = "#77eb34"
ORANGE = "#eba234"
GREY = "#a1a3a0"
BLACK = "#000000"

# Basket size exponential distribution parameter
LAMBA_EXPONENTIAL_DISTRIBUTION = 0.0736184654254411

filename = '../log/log' + str(datetime.now().strftime("%d-%m-%Y")) + '.log'
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(filename),
        logging.StreamHandler()
    ]
)


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if agent.type == 0:
        portrayal = {"scale": 1,
                     "r": 0.5,
                     "Layer": 1}
        # Todo questa cose con le stringhe magiche va cambiata per forza
        if type(agent.state).__name__ == "CustomerEnteredState":
            portrayal["Shape"] = "images/eCircle.png"
        elif type(agent.state).__name__ == "CustomerShoppingState":
            if not agent.self_scan:
                portrayal["Shape"] = "images/sCircleCyan.png"
            else:
                portrayal["Shape"] = "images/sCircleGrey.png"
        elif type(agent.state).__name__ == "CustomerChoosingQueueState":
            portrayal["Shape"] = "images/cCircle.png"
        elif type(agent.state).__name__ == "CustomerQueuedState":
            portrayal["Shape"] = "images/qCircle.png"
        elif type(agent.state).__name__ == "CustomerAtCashDeskState":
            portrayal["Shape"] = "images/pCircle.png"
    elif agent.type == 1:
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Color": BLACK,
                     "Layer": 1}
        if agent.direction == "v":
            portrayal["w"] = 0.2
            portrayal["h"] = 1
        elif agent.direction == "h":
            portrayal["w"] = 1
            portrayal["h"] = 0.2
    elif agent.type == 2:
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "w": 1,
                     "h": 1,
                     "Layer": 1}
        if type(agent).__name__ == "CashDeskStandard":
            portrayal["Color"] = BLUE
        elif type(agent).__name__ == "CashDeskSelfService":
            portrayal["Color"] = GREEN
        elif type(agent).__name__ == "CashDeskSelfScan":
            portrayal["Color"] = RED
        elif type(agent).__name__ == "CashDeskReserved":
            portrayal["Color"] = ORANGE

    return portrayal


def generate_basket_size(n, lambda_parameter=LAMBA_EXPONENTIAL_DISTRIBUTION):
    values = pd.Series(random.exponential(scale=1 / lambda_parameter, size=1000))
    values = values.apply(lambda x: math.ceil(round(x)))
    return values


def generate_customers_metadata(n_customers):
    customers_metadata = []

    basket_size_values = generate_basket_size(n_customers)
    # TODO: Cancellare questa riga!!!!
    basket_size_values = [20 + i for i in range(n_customers)]

    for basket_size in basket_size_values:
        self_scan = False
        new_tuple = (basket_size, self_scan, queue_choice_strategy, queue_jockeying_strategy())
        customers_metadata.append(new_tuple)
    return customers_metadata


# Zones metadata
entering_zone_width = 6
shopping_zone_height = 3
number_cash_desk_self_scan = 0
number_cash_desk = 2
number_cash_desk_self_service_groups = 0
zones_metadata = [('ENTERING', entering_zone_width),
                  ('SHOPPING', shopping_zone_height),
                  ('CASH_DESK_SELF_SCAN', number_cash_desk_self_scan),
                  ('CASH_DESK_STANDARD', number_cash_desk),
                  ('CASH_DESK_SELF_SERVICE', number_cash_desk_self_service_groups)]

# Customers metadata
queue_choice_strategy = QueueChoiceLeastPeople()
queue_jockeying_strategy = QueueJockeyLeastPeople()

N_CUSTOMERS = 5
customers_metadata = generate_customers_metadata(N_CUSTOMERS)

height = 20
# numero casse self-scan (ognuna occupa 2) + 1 spazio + barriera (1) + 1 spazio +
# numero casse standard (ognuna occupa 2) + 2 spazi + numero gruppi casse self (ognuna occupa 4) +
# barriera (1) + larghezza entering zone
width = number_cash_desk_self_scan * 2 + 3 + number_cash_desk * 2 + 1 + \
        number_cash_desk_self_service_groups * 4 + 1 + entering_zone_width
pixels_width = 500
pixels_height = 500 / width * height
grid = CanvasGrid(agent_portrayal, width,
                  height, pixels_width, pixels_height)

# Create server
server = ModularServer(Supermarket,
                       [grid],
                       "Supermarket",
                       {"customers_metadata": customers_metadata,
                        "zones_metadata": zones_metadata})
server.port = 8521  # The default
server.launch()
