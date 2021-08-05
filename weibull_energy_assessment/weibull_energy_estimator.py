import pandas as pd
from weibull_energy_assessment import templates
from weibull_energy_assessment.weibull import Weibull
from plant_info.turbine import Turbine
from power_analysis.curve_interpolator import CurveInterpolator
import numpy as np
from scipy.integrate import trapezoid

class WeibullEnergyEstimator:
    def __init__(self, weibull, rho: float):
        self.t = templates.Templates()
        self.w: Weibull = weibull
        self.ws_array = self.t.wind_speed_array
        self.rho_array = self.t.get_constant_density_array(rho=rho)
        self.ws_frequencies = self.w.pdf(x=self.ws_array)

    def __get_gross_annual_energy(self, power_array):
        """
        This function uses the Weibull PDF and integrates using the trapezoid rule to calculate annual gross energy.
        :param power_array:
        :return: (float): annual energy in MWh
        """
        # combine power output values and respective probability
        y = power_array * self.w.pdf(self.ws_array)

        # integrate using the trapezoid rule
        p_avg = trapezoid(y=y, x=self.ws_array)

        # convert power to annual energy in MWh
        annual_energy = p_avg * 8766 / 1000

        return annual_energy

    def gross_annual_energy_from_power_curve(self, turbine: Turbine):
        """

        :param turbine: turbine object
        :return: gross annual energy in MWh
        """
        curve_interpolator = CurveInterpolator(turbine_model=turbine.model)
        power_array = curve_interpolator.interpolate_power(wind_speed=self.ws_array, rho=self.rho_array)
        annual_gross_energy = self.__get_gross_annual_energy(power_array)

        return annual_gross_energy

    def gross_annual_energy_from_model(self, power_model):
        """

        :param power_model: the fitted model for turbine's performance
        :return: (float) annual gross energy based on the modeled turbine performance.
        """
        X = pd.DataFrame({'wind speed': self.ws_array,
                          'density': self.rho_array})
        power_array = power_model.predict(X)

        annual_gross_energy = self.__get_gross_annual_energy(power_array)
        return annual_gross_energy


