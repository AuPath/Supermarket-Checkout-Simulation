from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, TextElement

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

# Init charts
N_CHARTS = 1
charts = init_charts()

# Zones metadata
entering_zone_width = 6
shopping_zone_height = 10

number_cash_desk_self_scan = 4
number_cash_desk = 10

threshold_items = 15
threshold_people = 3
probability_of_jockeying = 0.5

number_cash_desk_self_service_groups = 1
shared_queue = False  # coda unica tipo decathlon

zones_metadata = init_zones_metadata(
    entering_zone_width, shopping_zone_height, number_cash_desk_self_scan,
    number_cash_desk, shared_queue, number_cash_desk_self_service_groups)

height = 30
pixels_width = 1500
pixels_height = 1500
grid = init_grid(height, pixels_width, pixels_height, zones_metadata)

# Time parameters
PERIOD_IN_SECONDS = 30
CUSTOMER_SPEED_PER_STEP = 0.5
SELF_SCAN_PERCENTAGE = 0.35
customer_distribution = init_customer_distribution(PERIOD_IN_SECONDS)

# Simulation name
simulation_name = 'validazione'
# Create server
server = ModularServer(Supermarket,
                       [grid, CustomerLegendElement(), CashDeskLegendElement()] + charts[:N_CHARTS],
                       "Supermarket",
                       {"zones_metadata": zones_metadata,
                        "simulation_name": simulation_name,
                        "customer_shopping_speed": CUSTOMER_SPEED_PER_STEP,
                        "customer_distribution": customer_distribution,
                        "period_in_seconds": PERIOD_IN_SECONDS,
                        "grid_height": height,
                        "self_scan_percentage": SELF_SCAN_PERCENTAGE,
                        "queue_choice_strategy": QueueChoiceLeastPeople(),
                        "queue_jockey_strategy": QueueJockeyLeastPeople(threshold_people,
                                                                        probability_of_jockeying)
                        })
server.port = 8521  # The default
server.settings["template_path"] = STATIC_PAGE_PATH
server.launch()
