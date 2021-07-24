import pandas as pd
import numpy as np
from weibull_energy_assessment.weibull import Weibull
from plant_info.turbine import Turbine
from power_analysis.curve_interpolator import CurveInterpolator


class TurbineDataSimulator:
    turbine_info_db = pd.read_excel('data/turbine_info_db.xlsx')

    __wind_speed_data = None
    __density_data = None

    def __init__(self, t_id: str, num_points: int,  perf_factor: float = 3.1):
        self.turbine = Turbine(t_id=t_id, turbine_info_db=self.turbine_info_db)
        self.num_points = num_points
        self.perf_factor = perf_factor
        self.out_df: pd.DataFrame = pd.DataFrame()
        self.cols = self.OutputDataFrameColumns(t_id=t_id)

    class OutputDataFrameColumns:
        def __init__(self, t_id):
            self.date = 'Date-Time'
            self.wind_speed = f'{t_id} Wind Speed [m/s]'
            self.density = f'{t_id} Air Density [kg/m^3]'
            self.power = f' {t_id} Active Power [kW]'

    @property
    def wind_speed_data(self):
        if self.__wind_speed_data is None:
            # instantiate weibull distribution
            w = Weibull(a=self.turbine.weibull_a, k=self.turbine.weibull_k)
            self.__wind_speed_data = w.inverse_cdf(r=np.random.rand(self.num_points))

        return self.__wind_speed_data

    @property
    def density_data(self):
        if self.__density_data is None:
            density_variation = np.random.randint(low=-25, high=25, size=self.num_points) / 1000

            self.__density_data = density_variation + self.turbine.average_air_density

        return self.__density_data

    def get_expected_power(self) -> np.array:
        interpolator = CurveInterpolator(turbine_model=self.turbine.model)
        exp_power = interpolator.interpolate_power(wind_speed=self.wind_speed_data, rho=self.density_data)
        return exp_power

    def get_active_power(self) -> np.array:
        wind_speed = self.wind_speed_data

        # apply adjustments to wind speed data and pass through curve interpolator to simulate turbine operational power
        noise = np.random.randint(-30, 30, len(wind_speed))/100
        adjustment = np.minimum(np.exp(wind_speed/self.perf_factor)/100, 1.8) + noise

        adj_wind_speed = wind_speed - adjustment

        # get power from adjust wind speeds
        interpolator = CurveInterpolator(turbine_model=self.turbine.model)
        power = interpolator.interpolate_power(wind_speed=adj_wind_speed, rho=self.density_data)

        return power

    def get_simulated_data(self):
        active_power = self.get_active_power()

        self.out_df = pd.DataFrame({self.cols.wind_speed: self.wind_speed_data,
                                    self.cols.density: self.density_data,
                                    self.cols.power: active_power})

        self.out_df.to_csv('data/simulated_turbine_data.csv')

        return













