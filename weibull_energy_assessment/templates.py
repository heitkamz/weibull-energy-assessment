import numpy as np


class Templates:
    wind_speed_array: np.array = np.linspace(start=0, stop=30, num=61, endpoint=True)
    density_array: np.array = np.linspace(start=0.95, stop=1.275, num=14)

    def get_constant_density_array(self, rho: float):
        return np.array([rho]*len(self.wind_speed_array))
