from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from src.Supermarket import Supermarket
from src.cashdesk.CashDeskStandard import CashDeskStandard
from src.queue.NormalQueue import NormalQueue


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


cash_desks = [CashDeskStandard(NormalQueue()), CashDeskStandard(NormalQueue())]
width = len(cash_desks) * 2 + 3

height = 10
pixels_width = 500
pixels_height = 500 / width * height
grid = CanvasGrid(agent_portrayal, width, height, pixels_width, pixels_height)

server = ModularServer(Supermarket,
                       [grid],
                       "Supermarket",
                       {"width": width, "height": height, "cash_desks": cash_desks})
server.port = 8521  # The default
server.launch()
