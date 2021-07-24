import pandas as pd


class CurveImporter:
    power_curve_file_dict = {'ST-2.55MW': 'sim_ref_power_curve.csv'
                             }

    rel_path = r'data'

    def get_power_curve(self, turbine_model: str):
        if turbine_model not in self.power_curve_file_dict.keys():
            raise Exception('Turbine model specified is not recognized.')

        return pd.read_csv(f'{self.rel_path}/{self.power_curve_file_dict[turbine_model]}', dtype=float)