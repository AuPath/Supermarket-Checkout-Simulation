import subprocess

import yaml

from src.config import ENTRYPOINT

SIMULATION_FILE = 'simulation.yaml'


def load_simulation_file(filename):
    with open(filename) as f:
        simulations_dict = yaml.safe_load(f)
    return [x["simulation"] for x in simulations_dict[0]['simulations']]


def parse_simulations(simulations):
    return [x["simulation"] for x in simulations[0]['simulations']]


simulations_list = load_simulation_file(SIMULATION_FILE)

commands_list = []
for simulation in simulations_list:
    parameters = ' '.join([f'--{key} {value}' for key, value in simulation.items()])
    command = f'python {ENTRYPOINT} {parameters} &'
    commands_list.append(command)

ID = 11
#script_file = '\n'.join(script_file)
subprocess.Popen(commands_list[ID], shell=True)
