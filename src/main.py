import math

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from src.OccupiedCell import CashDeskType
from src.Supermarket import Supermarket
from src.queuechoicestrategy.QueueChoiceLeastItems import QueueChoiceLeastItems

# colors
RED = "#eb3461"
BLUE = "#3493eb"
GREEN = "#77eb34"
ORANGE = "#eba234"
GREY = "#a1a3a0"
BLACK = "#000000"


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if agent.type == 0:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "r": 0.5,
                     "Color": GREY,
                     "Layer": 1}
    elif agent.type == 1:
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "w": 1,
                     "h": 1,
                     "Layer": 1}
        if agent.cash_desk_type == CashDeskType.STANDARD:
            portrayal["Color"] = BLUE
        elif agent.cash_desk_type == CashDeskType.SELF_SERVICE:
            portrayal["Color"] = GREEN
        elif agent.cash_desk_type == CashDeskType.SELF_SCAN:
            portrayal["Color"] = RED
        elif agent.cash_desk_type == CashDeskType.RESERVED:
            portrayal["Color"] = ORANGE
        elif agent.cash_desk_type == CashDeskType.NONE:
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
        else:
            pass

    return portrayal


# Zones metadata
entering_zone_width = 3
shopping_zone_height = 3
number_cash_desk_self_scan = 6
number_cash_desk = 10
number_cash_desk_self_service_groups = 2
zones_metadata = [('ENTERING', entering_zone_width),
                  ('SHOPPING', shopping_zone_height),
                  ('CASH_DESK_SELF_SCAN', number_cash_desk_self_scan),
                  ('CASH_DESK_STANDARD', number_cash_desk),
                  ('CASH_DESK_SELF_SERVICE', number_cash_desk_self_service_groups)]

# Customers metadata
customers_metadata = [(3, False, QueueChoiceLeastItems()),
                      (4, False, QueueChoiceLeastItems()),
                      (5, False, QueueChoiceLeastItems())]

height = 10
# larghezza self scan sulla sx + numero di self scan sull'orizzontale + 3 spazi + numero di gruppi di 4 casse
# self-service (ogni gruppo occupa 4 caselle in larghezza) + numero di casse con uno spazio tra una e l'altra
# + 1 spazio + larghezza della entering zone
width = 2 + (number_cash_desk_self_scan - math.ceil((height - shopping_zone_height - 1) / 2)) * 2 + 3 + \
        number_cash_desk_self_service_groups * 5 + number_cash_desk * 2 + 1 + entering_zone_width
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
