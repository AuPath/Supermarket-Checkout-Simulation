from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, TextElement

from src.Supermarket import Supermarket

from src.queuechoicestrategy.QueueChoiceLeastPeople import QueueChoiceLeastPeople
from src.queuechoicestrategy.QueueChoiceLeastItems import QueueChoiceLeastItems
from src.queuechoicestrategy.QueueChoiceLeastWaitingTimeServiceImplied import QueueChoiceLeastWaitingTimeServiceImplied
from src.queuechoicestrategy.QueueChoiceLeastWaitingPowerImplied import QueueChoiceLeastWaitingPowerImplied

from src.queuejockeystrategy.QueueJockeyLeastPeople import QueueJockeyLeastPeople
from src.queuejockeystrategy.QueueJockeyNoJockeying import QueueJockeyNoJockeying

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

threshold_items = 15
threshold_people = 3
probability_of_jockeying = 0.5

GRID_HEIGHT = 30
PIXELS_WIDTH = 1500
PIXELS_HEIGHT = 1500

# Time parameters
PERIOD_IN_SECONDS = 30
CUSTOMER_SPEED_PER_STEP = 0.5
SELF_SCAN_PERCENTAGE = 0
CUSTOMER_DISTRIBUTION = init_customer_distribution(PERIOD_IN_SECONDS)


def simulation_run(sim_name, zones_metadata, grid, customer_shop_speed, customer_arrival_distribution,
                   period_in_seconds, grid_height,
                   self_scan_customer_percentage, queue_choice_strategy, queue_jockey_strategy):
    return ModularServer(Supermarket,
                         [grid, CustomerLegendElement(), CashDeskLegendElement()] + charts[:N_CHARTS],
                         "Supermarket",
                         {"zones_metadata": zones_metadata,
                          "simulation_name": sim_name,
                          "customer_shopping_speed": customer_shop_speed,
                          "customer_distribution": customer_arrival_distribution,
                          "period_in_seconds": period_in_seconds,
                          "grid_height": grid_height,
                          "self_scan_percentage": self_scan_customer_percentage,
                          "queue_choice_strategy": queue_choice_strategy,
                          "queue_jockey_strategy": queue_jockey_strategy,
                          })


def validazione_1():
    entering_zone_width = 6
    shopping_zone_height = 10
    number_cash_desk_self_scan = 0
    number_cash_desk = 20
    number_cash_desk_self_service_groups = 1
    shared_queue = False

    zones_metadata = init_zones_metadata(
        entering_zone_width, shopping_zone_height, number_cash_desk_self_scan,
        number_cash_desk, shared_queue, number_cash_desk_self_service_groups)

    grid = init_grid(GRID_HEIGHT, PIXELS_WIDTH, PIXELS_HEIGHT, zones_metadata)

    queue_choice_strategy = QueueChoiceLeastItems()
    queue_jockeying_strategy = QueueJockeyNoJockeying()

    return simulation_run("validazione_1", zones_metadata, grid, CUSTOMER_SPEED_PER_STEP, CUSTOMER_DISTRIBUTION,
                          PERIOD_IN_SECONDS, GRID_HEIGHT, SELF_SCAN_PERCENTAGE,
                          queue_choice_strategy, queue_jockeying_strategy)


def validazione_2():
    entering_zone_width = 6
    shopping_zone_height = 10
    number_cash_desk_self_scan = 0
    number_cash_desk = 20
    number_cash_desk_self_service_groups = 1
    shared_queue = False

    zones_metadata = init_zones_metadata(
        entering_zone_width, shopping_zone_height, number_cash_desk_self_scan,
        number_cash_desk, shared_queue, number_cash_desk_self_service_groups)

    grid = init_grid(GRID_HEIGHT, PIXELS_WIDTH, PIXELS_HEIGHT, zones_metadata)

    queue_choice_strategy = QueueChoiceLeastPeople()
    queue_jockeying_strategy = QueueJockeyNoJockeying()

    return simulation_run("validazione_2", zones_metadata, grid, CUSTOMER_SPEED_PER_STEP, CUSTOMER_DISTRIBUTION,
                          PERIOD_IN_SECONDS, GRID_HEIGHT, SELF_SCAN_PERCENTAGE,
                          queue_choice_strategy, queue_jockeying_strategy)


def validazione_3():
    entering_zone_width = 6
    shopping_zone_height = 10
    number_cash_desk_self_scan = 0
    number_cash_desk = 20
    number_cash_desk_self_service_groups = 1
    shared_queue = False

    zones_metadata = init_zones_metadata(
        entering_zone_width, shopping_zone_height, number_cash_desk_self_scan,
        number_cash_desk, shared_queue, number_cash_desk_self_service_groups)

    grid = init_grid(GRID_HEIGHT, PIXELS_WIDTH, PIXELS_HEIGHT, zones_metadata)

    queue_choice_strategy = QueueChoiceLeastWaitingTimeServiceImplied()
    queue_jockeying_strategy = QueueJockeyNoJockeying()

    return simulation_run("validazione_3", zones_metadata, grid, CUSTOMER_SPEED_PER_STEP, CUSTOMER_DISTRIBUTION,
                          PERIOD_IN_SECONDS, GRID_HEIGHT, SELF_SCAN_PERCENTAGE,
                          queue_choice_strategy, queue_jockeying_strategy)


def validazione_4():
    entering_zone_width = 6
    shopping_zone_height = 10
    number_cash_desk_self_scan = 0
    number_cash_desk = 20
    number_cash_desk_self_service_groups = 1
    shared_queue = False

    zones_metadata = init_zones_metadata(
        entering_zone_width, shopping_zone_height, number_cash_desk_self_scan,
        number_cash_desk, shared_queue, number_cash_desk_self_service_groups)

    grid = init_grid(GRID_HEIGHT, PIXELS_WIDTH, PIXELS_HEIGHT, zones_metadata)

    queue_choice_strategy = QueueChoiceLeastWaitingPowerImplied()
    queue_jockeying_strategy = QueueJockeyNoJockeying()

    return simulation_run("validazione_4", zones_metadata, grid, CUSTOMER_SPEED_PER_STEP, CUSTOMER_DISTRIBUTION,
                          PERIOD_IN_SECONDS, GRID_HEIGHT, SELF_SCAN_PERCENTAGE,
                          queue_choice_strategy, queue_jockeying_strategy)


# todo da qua devo essere in grado di passare i parametri sulle probabilità di errore a chi di dovere
# Create server
server = validazione_4()
server.port = 8521  # The default
server.settings["template_path"] = STATIC_PAGE_PATH
server.launch()
