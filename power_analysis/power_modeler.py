from pygam import LinearGAM
from power_analysis.curve_interpolator import CurveInterpolator
import numpy as np
import pandas as pd
from weibull_energy_assessment.templates import Templates
from plant_info.turbine import Turbine
import matplotlib.pyplot as plt


class PowerModeler:
    def __init__(self, turbine: Turbine, pre_processed_data: pd.DataFrame,
                 wind_speed_range: tuple = (0, 14)):
        self.turbine = turbine
        self.interpolator = CurveInterpolator(turbine_model=self.turbine.model)
        self.data = pre_processed_data
        self.wind_speed_range = wind_speed_range
        self.templates = Templates()

        return

    def get_pygam_multi_param_model(self):

        data = self.data
        turbine = self.turbine
        print(f'{len(data)} points utilized for modeling.')

        training_x_data = data[[turbine.tags.wind_speed, turbine.tags.density]]
        training_y_data = data[turbine.tags.active_power]

        power_model = self.gam_multi_param(X=training_x_data, y=training_y_data)

        return power_model

    def get_oem_power_curve_model(self, rho: float):
        wind_speeds = np.linspace(start=self.wind_speed_range[0], stop=self.wind_speed_range[1], num=140)
        densities = np.array([rho] * len(wind_speeds))
        X = pd.DataFrame({'wind speed': wind_speeds,
                          'density': densities})

        interpolator = self.interpolator

        power_array = interpolator.interpolate_power(wind_speed=wind_speeds, rho=densities)
        y = pd.DataFrame({'power': power_array})

        expected_power_model = self.gam_multi_param(X=X, y=y)

        return expected_power_model

    @staticmethod
    def gam_multi_param(X, y, n_splines=20):
        """
        Model power performance using generalized additive model.
        :param X: (pandas dataframe) containing inputs (wind speed, density, etc.)
        :param y: (pandas series) containing grid power.
        :param n_splines: number of splines for fitting
        :return: Fitted model object
        """

        fitted_power_curve_model = LinearGAM(n_splines=n_splines).fit(X, y)

        return fitted_power_curve_model

    def visualize_model(self, power_model, rho: float):

        t = self.templates
        df = self.data
        turbine = self.turbine
        wind_speed_array = t.wind_speed_array
        density_array = t.get_constant_density_array(rho=rho)
        model_inputs = pd.DataFrame({'wind speed': wind_speed_array,
                                     'density': density_array})
        # filter dataframe for density
        df = df[(df[turbine.tags.density] > rho - .02) & (df[turbine.tags.density] < rho + .02)]

        # generate the plot
        plt.figure(figsize=(14, 10))
        plt.plot(wind_speed_array, power_model.predict(model_inputs), color='black', label='Turbine Model')
        plt.scatter(df[turbine.tags.wind_speed], df[turbine.tags.active_power], color='blue', alpha=0.3, s=4,
                    edgecolors='None', label='Actual Power - Normal Operation')
        plt.grid()
        plt.legend()
        plt.title(f'{turbine.id} Model Overlay')
        plt.xlabel('Wind Speed [m/s]')
        plt.ylabel('Power [kW]')
        plt.xlim((0, 14))
        plt.show()

        return

    def plot_model_vs_warranted_curve(self, power_model, rho: float):
        t = self.templates
        wind_speed_array = t.wind_speed_array
        density_array = t.get_constant_density_array(rho=rho)
        model_inputs = pd.DataFrame({'wind speed': wind_speed_array,
                                     'density': density_array})

        # generate the plot
        plt.figure(figsize=(14, 10))
        plt.plot(wind_speed_array, power_model.predict(model_inputs), color='orange',
                 label=f'{self.turbine.id} Modeled Performance')
        plt.plot(wind_speed_array, self.interpolator.interpolate_power(wind_speed=wind_speed_array, rho=density_array),
                 color='green', label=f'{self.turbine.model} Warranted Power Curve')
        plt.grid()
        plt.legend()
        plt.title(f'{self.turbine.id} Turbine Performance Comparison')
        plt.xlabel('Wind Speed [m/s]')
        plt.ylabel('Power [kW]')
        plt.xlim((0, 14))
        plt.show()

        return