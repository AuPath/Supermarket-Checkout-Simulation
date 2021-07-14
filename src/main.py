from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from src.Supermarket import Supermarket
from src.queue.NormalQueue import NormalQueue
from src.queuechoicestrategy.QueueChoiceLeastItems import QueueChoiceLeastItems
from src.zones.stationary.EnteringZone import EnteringZone
from src.zones.stationary.ShoppingZone import ShoppingZone


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if agent.type == 0:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "r": 0.5,
                     "Color": "grey",
                     "Layer": 1}
    elif agent.type == 1:
        if agent.is_cashdesk:
            portrayal = {"Shape": "rect",
                         "Filled": "true",
                         "Color": "red",
                         "w": 1,
                         "h": 1,
                         "Layer": 1}
        else:
            if agent.direction == "v":
                portrayal = {"Shape": "rect",
                             "Filled": "true",
                             "Color": "black",
                             "w": 0.2,
                             "h": 1,
                             "Layer": 1}
            elif agent.direction == "h":
                portrayal = {"Shape": "rect",
                             "Filled": "true",
                             "Color": "black",
                             "w": 1,
                             "h": 0.2,
                             "Layer": 1}

    return portrayal


# Zones metadata
zones_metadata = [('ENTERING', 3),
                  ('SHOPPING', 3)]
# Cash desks metadata
cash_desks_metadata = [NormalQueue(), NormalQueue()]
# Customers metadata
customers_metadata = [(3, False, QueueChoiceLeastItems()),
                      (4, False, QueueChoiceLeastItems()),
                      (5, False, QueueChoiceLeastItems())]

width = 2 * 2 + 3
height = 10
pixels_width = 500
pixels_height = 500 / width * height
grid = CanvasGrid(agent_portrayal, len(cash_desks_metadata) * 2 + 3,
                  height, pixels_width, pixels_height)

# Create server
server = ModularServer(Supermarket,
                       [grid],
                       "Supermarket",
                       {"customers_metadata": customers_metadata,
                        "cash_desks_metadata": cash_desks_metadata,
                        "zones_metadata": zones_metadata})
server.port = 8521  # The default
server.launch()
