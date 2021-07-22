import logging
from datetime import datetime

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from src.Supermarket import Supermarket
from src.queuechoicestrategy.QueueChoiceLeastPeople import QueueChoiceLeastPeople
from src.queuejockeystrategy.QueueJockeyLeastPeople import QueueJockeyLeastPeople

# colors
RED = "#eb3461"
BLUE = "#3493eb"
BLUE_GREY = "#a9bac9"
GREEN = "#77eb34"
ORANGE = "#eba234"
GREY = "#a1a3a0"
BLACK = "#000000"

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
        portrayal = {"Shape": agent.state.get_image(),
                     "scale": 1,
                     "r": 0.5,
                     "Layer": 1}
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
        portrayal = {"Shape": agent.get_image(),
                     "Filled": "true",
                     "w": 1,
                     "h": 1,
                     "Layer": 1}
    return portrayal


# Zones metadata
entering_zone_width = 6
shopping_zone_height = 3
number_cash_desk_self_scan = 0
number_cash_desk = 10

number_cash_desk_self_service_groups = 1
shared_queue = False  # coda unica tipo decathlon
zones_metadata = [('ENTERING', entering_zone_width),
                  ('SHOPPING', shopping_zone_height),
                  ('CASH_DESK_SELF_SCAN', number_cash_desk_self_scan),
                  (('CASH_DESK_STANDARD_SHARED_QUEUE', number_cash_desk) if shared_queue else
                   ('CASH_DESK_STANDARD', number_cash_desk)),
                  ('CASH_DESK_SELF_SERVICE', number_cash_desk_self_service_groups),
                  ('CASH_DESK_RESERVED', 1)]

# TODO: quanto vale uno step? qui 1 minuto, gli faccio entrare un cliente al minuto, e la giornata dura 8 ore
customer_distribution = [1] * (60 * 8)

height = 20
# numero casse self-scan (ognuna occupa 2) + 1 spazio + barriera (1) + 1 spazio +
# numero casse standard (ognuna occupa 2) + 2 spazi + numero gruppi casse self (ognuna occupa 8) +
# barriera (1) + larghezza entering zone
width = number_cash_desk_self_scan * 2 + 3 + number_cash_desk * 2 + 1 + \
        number_cash_desk_self_service_groups * 8 + 1 + entering_zone_width
pixels_width = 500
pixels_height = 500 / width * height
grid = CanvasGrid(agent_portrayal, width,
                  height, pixels_width, pixels_height)

# Create server
server = ModularServer(Supermarket,
                       [grid],
                       "Supermarket",
                       {"zones_metadata": zones_metadata,
                        # lista con numero di clienti da generare ad ogni step es. [1, 2, 3, 2, 4, 5, 2, ...]
                        "customer_distribution": customer_distribution,
                        "queue_choice_strategy": QueueChoiceLeastPeople(),
                        "queue_jockey_strategy": QueueJockeyLeastPeople()
                        })
server.port = 8521  # The default
server.launch()