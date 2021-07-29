from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, TextElement, ChartModule

from src.Supermarket import Supermarket
from src.queuechoicestrategy.QueueChoiceLeastPeople import QueueChoiceLeastPeople
from src.queuejockeystrategy.QueueJockeyLeastPeople import QueueJockeyLeastPeople
from src.utility import *


class CustomerLegendElement(TextElement):
    def render(self, model):
        return read_html(STATIC_PAGE_PATH, 'customer_legend.html')


class CashDeskLegendElement(TextElement):
    def render(self, model):
        return read_html(STATIC_PAGE_PATH, 'cash_desk_legend.html')


# Init log
init_logging(LOG_PATH, enable_logging=False)

# Zones metadata
entering_zone_width = 6
shopping_zone_height = 3
number_cash_desk_self_scan = 4
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

height = 28
# numero casse self-scan (ognuna occupa 2) + 1 spazio + barriera (1) + 1 spazio +
# numero casse standard (ognuna occupa 2) + 2 spazi + numero gruppi casse self (ognuna occupa 8) +
# barriera (1) + larghezza entering zone
width = number_cash_desk_self_scan * 2 + 3 + number_cash_desk * 2 + 1 + \
        number_cash_desk_self_service_groups * 8 + 1 + entering_zone_width
pixels_width = 1500
pixels_height = 1500 / width * height
grid = CanvasGrid(agent_portrayal, width,
                  height, pixels_width, pixels_height)

# Grafici e metriche
chart = ChartModule([{"Label": "Total_customers",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

chart1 = ChartModule([{"Label": "Density_total",
                       "Color": "Black"}],
                     data_collector_name='datacollector')

chart2 = ChartModule([{"Label": "Density_standard",
                       "Color": "Black"}],
                     data_collector_name='datacollector')

chart3 = ChartModule([{"Label": "Density_self_scan",
                       "Color": "Black"}],
                     data_collector_name='datacollector')

chart4 = ChartModule([{"Label": "Flow_total",
                       "Color": "Black"}],
                     data_collector_name='datacollector')

chart5 = ChartModule([{"Label": "Flow_standard",
                       "Color": "Black"}],
                     data_collector_name='datacollector')

chart6 = ChartModule([{"Label": "Flow_self_scan",
                       "Color": "Black"}],
                     data_collector_name='datacollector')

# Create server
customer_legend_element = CustomerLegendElement()
cash_desk_legend_element = CashDeskLegendElement()
server = ModularServer(Supermarket,
                       [grid, customer_legend_element, cash_desk_legend_element, chart, chart1, chart2, chart3,
                        chart4, chart5, chart6],
                       "Supermarket",
                       {"zones_metadata": zones_metadata,
                        # lista con numero di clienti da generare ad ogni step es. [1, 2, 3, 2, 4, 5, 2, ...]
                        "customer_distribution": customer_distribution,
                        "queue_choice_strategy": QueueChoiceLeastPeople(),
                        "queue_jockey_strategy": QueueJockeyLeastPeople()
                        })
server.port = 8521  # The default
server.settings["template_path"] = STATIC_PAGE_PATH
server.launch()
