import pint
import pandas as pd


class Turbine:
    # instantiate unit registry
    u = pint.UnitRegistry()

    attributes = ['id', 'model', 'feeder', 'capacity', 'rotor_diameter',
                  'hub_height', 'latitude', 'longitude', 'elevation', 'weibull_a', 'weibull_k', 'average_air_density',
                  'primary_neighbor', 'secondary_neighbor']

    def __init__(self, t_id: str, turbine_info_db: pd.DataFrame):
        self.db = turbine_info_db
        self.id = t_id

        if self.id not in list(self.db['Turbine']):
            raise Exception('Turbine ID Not Recognized for Project')

        self.model = None
        self.feeder = None
        self.capacity = None
        self.rotor_diameter = None
        self.hub_height = None
        self.latitude = None
        self.longitude = None
        self.elevation = None
        self.weibull_a = None
        self.weibull_k = None
        self.average_air_density = None
        self.primary_neighbor = None
        self.secondary_neighbor = None

        # set turbine attributes
        self.__set_turbine_info_attr()

        # create tag properties
        self.tags = self.Tags(self.id)
        self.primary_neighbor_tags = self.Tags(self.primary_neighbor)
        self.secondary_neighbor_tags = self.Tags(self.secondary_neighbor)

    def __set_turbine_info_attr(self):
        db = self.db
        _id = self.id

        # get the index of the turbine id
        i = db[db['Turbine'] == _id].index[0]
        col_vals = list(db.loc[i])

        for col_val, attr in zip(col_vals, self.attributes):
            setattr(self, attr, col_val)

        # assign units
        self.elevation = self.elevation * self.u.foot
        self.hub_height = self.hub_height * self.u.meter
        return

    class Tags:
        def __init__(self, t_id):
            self.wind_speed = f'{t_id} Wind Speed [m/s]'
            self.density = f'{t_id} Air Density [kg/m^3]'
            self.active_power = f' {t_id} Active Power [kW]'

