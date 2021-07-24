from data.get_simulated_data import TurbineDataSimulator as tds
import numpy as np
import matplotlib.pyplot as plt


simulator = tds('T01', num_points=6000, perf_factor=1.0)

simulator.get_simulated_data()
plt.scatter(simulator.wind_speed_data, simulator.get_expected_power(), alpha=0.25, s=4, label='expected_power')
plt.scatter(simulator.wind_speed_data, simulator.get_active_power(), alpha=0.25, s=4, color='r', label='active power')

plt.legend()
plt.grid()
plt.show()