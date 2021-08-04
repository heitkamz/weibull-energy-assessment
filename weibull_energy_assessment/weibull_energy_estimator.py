import pandas as pd
from weibull_energy_assessment import templates
from weibull_energy_assessment.weibull import Weibull
from plant_info.turbine import Turbine
from power_analysis.curve_interpolator import CurveInterpolator
import numpy as np


class WeibullEnergyEstimator:
    def __init__(self, weibull, rho: float):
        self.t = templates.Templates()
        self.w: Weibull = weibull
        self.ws_array = self.t.wind_speed_array
        self.rho_array = self.t.get_constant_density_array(rho=rho)
        self.ws_frequencies = self.w.pdf(x=self.ws_array)

    def __get_gross_energy_array(self, power_array):
        """
        This function uses the Weibull CDF to calculate annual gross energy.
        :param power_array:
        :return:
        """
        ws_cdf = self.w.cdf(self.ws_array)
        ws_bin_frequency = np.diffs(ws_cdf)

        power_step_change = np.diff(power_array)
        average_power = power_array[0:-1] + power_step_change

        power_density_array = ws_bin_frequency * average_power

        energy_array = power_density_array * (8766/1000)
        
        return energy_array

    def gross_annual_energy_from_power_curve(self, turbine: Turbine):
        """

        :param turbine: turbine object
        :return: gross annual energy in MWh
        """
        curve_interpolator = CurveInterpolator(turbine_model=turbine.model)
        power_array = curve_interpolator.interpolate_power(wind_speed=self.ws_array, rho=self.rho_array)
        annual_gross_energy_array = self.__get_gross_energy_array(power_array)

        return np.sum(annual_gross_energy_array)

    def gross_annual_energy_from_model(self, power_model):
        """

        :param power_model: the fitted model for turbine's performance
        :return: (float) annual gross energy based on the modeled turbine performance.
        """
        X = pd.DataFrame({'wind speed': self.ws_array,
                          'density': self.rho_array})
        power_array = power_model.predict(X)

        annual_gross_energy_array = self.__get_gross_energy_array(power_array)
        return np.sum(annual_gross_energy_array)


