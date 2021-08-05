# weibull-energy-assessment
This project provides a framework for evaluating the wind resource and energy production given Weibull wind resource parameters at a turbine site.

### Background:
In wind energy applications, the Weibull distribution is often used to describe the wind speed probability distribution. Since wind speed values can be mapped to active power by utlizing a wind turbine's "power curve", the probability distribution function (PDF) for wind speed can be used to calculate the expected power output. The expected power value is obtained by integrating the product of the probability of a given windspeed and the power at that given windspeed over the wind speed domain.  Multiplying the expected power value by a scalar time duration returns the expected energy over the time duration. Generally, the time duration used should be 8,766 hours to model annual energy in megawatt-hours and to account for seasonal impacts to the wind resource.

The Weibull scale parameter (lambda) and shape parameter (kappa) can be obtained for a given location by utilizing services such as Windnavigator by UL. The parameters assigned to the turbine used in this demonstration were not obtained from a third party source, however. Instead, the values are arbitrary, albeit, realistic. 

The weibull.py and weibull_energy_estimator.py modules in this repository can be used to assess the wind resource at a specified turbine location and estimate the annual gross energy for the given turbine technology type. Additionally, the power_modeler.py module can be used to model a wind turbine's operational performance by providing operational wind speed, air density, and active power data. This allows a comparison between the expected energy based on the warranted power curve for the turbine and a model of the turbine's actual performance to calculate annual performance losses. Use of the classes within the modules are demonstrated in the demo.ipynb file. 

### A note on the data:
All data has been simulated. In fact, the get_simulated_data.py module has been developed to generate simulated but realistic operating data. In practice, users will provide their own operating data to perform the analysis. It is assumed that the data reflects normal operating conditions for the turbine, so care should be taken by the user to first preprocess the data for normal turbine operation. Additionally, the turbine information and turbine model in the turbine_info_db.xlsx file along with the reference power curve data is simulated. 
