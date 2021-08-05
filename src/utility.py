import os, logging, pickle, numpy as np
from datetime import datetime

from mesa.visualization.modules import ChartModule, CanvasGrid

from config import *

SIGMA_CUSTOMER_DISTRIBUTION = 0.4


def init_logging(log_path, enable_logging=False):
    if not enable_logging:
        return
    filename = f'{log_path}/{str(datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))}.log'
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(filename)),
            logging.StreamHandler()
        ]
    )


def read_html(static_path, page):
    with open(os.path.join(static_path, page)) as f:
        return ''.join(f.readlines())


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


def init_charts():
    charts = []
    chart0 = ChartModule([{"Label": "Total_customers",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart0)

    chart10 = ChartModule([{"Label": "Number_exiting_customers",
                            "Color": "Black"}],
                          data_collector_name='datacollector')

    charts.append(chart10)

    chart1 = ChartModule([{"Label": "Density_total",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart1)

    chart2 = ChartModule([{"Label": "Density_standard",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart2)

    chart3 = ChartModule([{"Label": "Density_self_scan",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart3)

    chart4 = ChartModule([{"Label": "Flow_total",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart4)

    chart5 = ChartModule([{"Label": "Flow_standard",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart5)

    chart6 = ChartModule([{"Label": "Flow_self_scan",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart6)

    chart7 = ChartModule([{"Label": "Total_steps",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart7)

    chart8 = ChartModule([{"Label": "Avg_waiting_times_standard",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart8)

    chart9 = ChartModule([{"Label": "Avg_waiting_times_self_scan",
                           "Color": "Black"}],
                         data_collector_name='datacollector')
    charts.append(chart9)

    return charts


def init_grid(height, pixels_width, pixels_height, zones_metadata):
    # Unzip metadata
    zones_metadata_dict = dict(zones_metadata)
    number_cash_desk_self_scan = zones_metadata_dict['CASH_DESK_SELF_SCAN']
    number_cash_desk = zones_metadata_dict['CASH_DESK_STANDARD']
    number_cash_desk_self_service_groups = zones_metadata_dict['CASH_DESK_SELF_SERVICE']
    entering_zone_width = zones_metadata_dict['ENTERING']

    # numero casse self-scan (ognuna occupa 2) + 1 spazio + barriera (1) + 1 spazio +
    # numero casse standard (ognuna occupa 2) + 2 spazi + numero gruppi casse self (ognuna occupa 8) +
    # barriera (1) + larghezza entering zone
    width = number_cash_desk_self_scan * 2 + 3 + number_cash_desk * 2 + 1 + \
            number_cash_desk_self_service_groups * 8 + 1 + entering_zone_width

    pixels_height = pixels_height / width * height

    grid = CanvasGrid(agent_portrayal, width, height, pixels_width, pixels_height)

    return grid


def init_zones_metadata(entering_zone_width, shopping_zone_height, number_cash_desk_self_scan,
                        number_cash_desk, shared_queue, number_cash_desk_self_service_groups):
    zones_metadata = [('ENTERING', entering_zone_width),
                      ('SHOPPING', shopping_zone_height),
                      ('CASH_DESK_SELF_SCAN', number_cash_desk_self_scan),
                      (('CASH_DESK_STANDARD_SHARED_QUEUE', number_cash_desk) if shared_queue else
                       ('CASH_DESK_STANDARD', number_cash_desk)),
                      ('CASH_DESK_SELF_SERVICE', number_cash_desk_self_service_groups),
                      ('CASH_DESK_RESERVED', 1)]
    return zones_metadata


def read_input_customer_distribution(input_file=INPUT_FILE_CUSTOMER_DISTRIBUTION):
    with open(input_file, 'rb') as f:
        df = pickle.load(f)
    return df


def generate_customers_dist(df, steps_in_hour, sigma=SIGMA_CUSTOMER_DISTRIBUTION):
    customers_distribution = []

    for customers_in_hour in df["value"]:
        # Generate samples
        mu = customers_in_hour / steps_in_hour
        bias_customers_in_hour = np.random.normal(mu, sigma, steps_in_hour)
        bias_customers_in_hour = [round(abs(x)) for x in bias_customers_in_hour]
        customers_distribution += bias_customers_in_hour

    return customers_distribution


def init_customer_distribution(step_in_seconds):
    df = read_input_customer_distribution()
    number_of_steps_in_hour = int(60 * 60 / step_in_seconds)
    customer_distribution = generate_customers_dist(df, number_of_steps_in_hour)
    return customer_distribution

