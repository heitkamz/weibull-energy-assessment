from power_analysis.curve_importer import CurveImporter
import numpy as np
from scipy.interpolate import RegularGridInterpolator


class CurveInterpolator:
    def __init__(self, turbine_model: str):
        self.power_curve_df = CurveImporter().get_power_curve(turbine_model=turbine_model)
        self.power_matrix = self.power_curve_df.iloc[:, 1:].values
        ws_array = np.array(list(self.power_curve_df['Wind Speed [m/s]']))
        density_array_str = list(self.power_curve_df.columns[1:])
        density_array = np.array([float(i) for i in density_array_str])

        self.power_curve_interpolator = RegularGridInterpolator(points=(ws_array, density_array),
                                                                values=self.power_matrix,
                                                                bounds_error=False,
                                                                fill_value=None)
        return

    def interpolate_power(self, wind_speed, rho):
        # convert wind speed and density to numpy arrays
        ws = np.array(wind_speed)
        rho = np.array(rho)

        # combine wind speed and density arrays into a points set
        input_array = np.stack((ws, rho), axis=1)

        # interpolate the power
        power = self.power_curve_interpolator(input_array)

        return power


