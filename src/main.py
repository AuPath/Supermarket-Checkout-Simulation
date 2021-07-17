import logging
from datetime import datetime

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from src.Customer import CustomerState
from src.Supermarket import Supermarket
# colors
from src.queuechoicestrategy.QueueChoiceLeastPeople import QueueChoiceLeastPeople

RED = "#eb3461"
BLUE = "#3493eb"
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
        portrayal = {"scale": 1,
                     "r": 0.5,
                     "Layer": 1}
        if agent.state == CustomerState.ENTERED:
            portrayal["Shape"] = "images/eCircle.png"
        elif agent.state == CustomerState.SHOPPING:
            portrayal["Shape"] = "images/sCircle.png"
        elif agent.state == CustomerState.CHOOSING_QUEUE:
            portrayal["Shape"] = "images/cCircle.png"
        elif agent.state == CustomerState.QUEUED:
            portrayal["Shape"] = "images/qCircle.png"
        elif agent.state == CustomerState.CASH_DESK:
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


# Zones metadata
entering_zone_width = 6
shopping_zone_height = 3
number_cash_desk_self_scan = 2
number_cash_desk = 1
number_cash_desk_self_service_groups = 1
zones_metadata = [('ENTERING', entering_zone_width),
                  ('SHOPPING', shopping_zone_height),
                  ('CASH_DESK_SELF_SCAN', number_cash_desk_self_scan),
                  ('CASH_DESK_STANDARD', number_cash_desk),
                  ('CASH_DESK_SELF_SERVICE', number_cash_desk_self_service_groups)]

# Customers metadata
customers_metadata = []
for i in range(15):
    customers_metadata.append((5 + i, True, QueueChoiceLeastPeople()))
for i in range(15):
    customers_metadata.append((5 + i, False, QueueChoiceLeastPeople()))

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
