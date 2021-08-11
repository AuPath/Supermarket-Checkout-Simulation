from src.queuechoicestrategy.QueueChoiceLeastItems import QueueChoiceLeastItems
from src.queuechoicestrategy.QueueChoiceLeastPeople import QueueChoiceLeastPeople
from src.queuechoicestrategy.QueueChoiceLeastWaitingPowerImplied import QueueChoiceLeastWaitingPowerImplied
from src.queuechoicestrategy.QueueChoiceLeastWaitingTimeServiceImplied import QueueChoiceLeastWaitingTimeServiceImplied
from src.queuejockeystrategy.QueueJockeyLeastItems import QueueJockeyLeastItems
from src.queuejockeystrategy.QueueJockeyLeastPeople import QueueJockeyLeastPeople
from src.queuejockeystrategy.QueueJockeyNoJockeying import QueueJockeyNoJockeying
from src.utility import *

# Logging
init_logging(LOG_PATH, enable_logging=False)

# Init charts
N_CHARTS = 1

# Grid parameters
GRID_HEIGHT = 30
PIXELS_WIDTH = 1500
PIXELS_HEIGHT = 1500

# Supermarket parameters
ENTERING_ZONE_WIDTH = 6
SHOPPING_ZONE_HEIGHT = 10

# Time parameters
PERIOD_IN_SECONDS = 30
CUSTOMER_SPEED_PER_STEP = 0.5
SELF_SCAN_PERCENTAGE = 0
CUSTOMER_DISTRIBUTION = init_customer_distribution(PERIOD_IN_SECONDS)


def preprocess_jockeying_strategy(parameters):
    out_parameters = parameters
    jockeying = None
    if parameters['queue_jockeying_strategy'] == 'no_jockeying':
        jockeying = QueueJockeyNoJockeying()
    elif parameters['queue_jockeying_strategy'] == 'least_items':
        threshold, prob_jockey = parameters['threshold_people'], parameters['probability_of_jockeying']
        jockeying = QueueJockeyLeastItems(threshold=threshold, prob_jockey=prob_jockey)
    elif parameters['queue_jockeying_strategy'] == 'least_people':
        threshold, prob_jockey = parameters['threshold_people'], parameters['probability_of_jockeying']
        jockeying = QueueJockeyLeastPeople(threshold=threshold, prob_jockey=prob_jockey)
    out_parameters.update([('queue_jockeying_strategy', jockeying)])

    return out_parameters


def preprocess_queue_choice_strategy(parameters):
    out_parameters = parameters
    queue_choice_strategy = None
    if parameters['queue_choice_strategy'] == 'least_items':
        queue_choice_strategy = QueueChoiceLeastItems()
    elif parameters['queue_choice_strategy'] == 'least_people':
        queue_choice_strategy = QueueChoiceLeastPeople()
    elif parameters['queue_choice_strategy'] == 'least_waiting_time_service_implied':
        queue_choice_strategy = QueueChoiceLeastWaitingTimeServiceImplied()
    elif parameters['queue_choice_strategy'] == 'least_waiting_power_implied':
        queue_choice_strategy = QueueChoiceLeastWaitingPowerImplied()
    out_parameters.update([('queue_choice_strategy', queue_choice_strategy)])

    return out_parameters


def preprocess_simulation_parameters(input_parameters):
    input_parameters = vars(input_parameters)
    input_parameters = preprocess_jockeying_strategy(input_parameters)
    input_parameters = preprocess_queue_choice_strategy(input_parameters)

    zones_metadata = init_zones_metadata(
        entering_zone_width=ENTERING_ZONE_WIDTH,
        shopping_zone_height=SHOPPING_ZONE_HEIGHT,
        number_cash_desk_self_scan=input_parameters['number_cash_desk_self_scan'],
        number_cash_desk=input_parameters['number_cash_desk'],
        shared_queue=input_parameters['shared_queue'],
        number_cash_desk_self_service_groups=input_parameters['number_cash_desk_self_service_groups'])

    grid = init_grid(GRID_HEIGHT, PIXELS_WIDTH, PIXELS_HEIGHT, zones_metadata)

    keys_to_remove = [
        'number_cash_desk_self_scan',
        'number_cash_desk',
        'number_cash_desk_self_service_groups',
        'shared_queue',
        'threshold_people',
        'probability_of_jockeying']

    for dict_key in keys_to_remove:
        input_parameters.pop(dict_key, None)

    server_parameters = dict(
        zones_metadata=zones_metadata,
        grid=grid,
        customer_shop_speed=CUSTOMER_SPEED_PER_STEP,
        customer_arrival_distribution=CUSTOMER_DISTRIBUTION,
        period_in_seconds=PERIOD_IN_SECONDS,
        grid_height=GRID_HEIGHT
    )

    parameters = dict(input_parameters, **server_parameters)
    return parameters


def get_simulation_parameters():
    parameters = parse_simulations_parameters()
    parameters = preprocess_simulation_parameters(parameters)
    return parameters


def init_server(parameters):
    out_server = simulation_run(**parameters, n_charts=N_CHARTS)
    out_server.settings["template_path"] = STATIC_PAGE_PATH
    return out_server


# Create server
simulation_parameters = get_simulation_parameters()
server = init_server(simulation_parameters)

port = 8521
while True:
    try:
        server.port = port  # The default
        server.launch()
        print(f'Server running on port {port}')
        break
    except OSError:
        port += 1
