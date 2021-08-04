from scipy.special import gamma
import numpy as np
import matplotlib.pyplot as plt
from weibull_energy_assessment.templates import Templates


class Weibull:
    """
    Reference: https://en.wikipedia.org/wiki/Weibull_distribution
    """
    def __init__(self, a: float, k: float):
        self.a: float = a  # weibull scale parameter ("lambda")
        self.k: float = k  # weibull shape parameter ("kappa")

        self.mean: float = self.a * gamma(1 + 1/self.k)
        self.median: float = self.a * (np.log(2))**(1/self.k)
        self.mode: float = self.a * ((self.k - 1)/self.k)**(1/self.k)

        # get wind speed templates
        self.wind_speed_array = Templates.wind_speed_array

    def pdf(self, x):
        """

        :param x: (float or array): random variable
        :return: (float or array) probability of occurrence
        """
        return (self.k / self.a) * (x / self.a) ** (self.k - 1) * np.exp(-(x / self.a) ** self.k)

    def cdf(self, x):
        """

        :param x: (float or array): random variable
        :return: (float or array): cumulative probability
        """
        return 1 - np.exp(-(x/self.a)**self.k)

    def inverse_cdf(self, r):
        """
        This function returns sample wind speed values from the weibull distribution
        :param r: float or array of random values between 0 and 1
        :return: float or array of sample wind speeds.
        """
        return -self.a * (np.sign(np.log(r)) * np.abs((np.log(r)))**(1/self.k))

    def plot_pdf(self):

        p = self.pdf(self.wind_speed_array)

        plt.figure(figsize=(14, 10))
        plt.plot(self.wind_speed_array, p)
        plt.grid()
        plt.xlabel('Wind Speed [m/s]')
        plt.ylabel('PDF')
        plt.title(fr'Probability Density Function for $\lambda$={self.a}; k={self.k}')
        plt.show()

        return

    def plot_cdf(self):
        cd = self.cdf(self.wind_speed_array)

        plt.figure(figsize=(14, 10))
        plt.plot(self.wind_speed_array, cd * 100, color='k')
        plt.grid()
        plt.xlabel('Wind Speed [m/s]')
        plt.ylabel('CDF')
        plt.title(fr'Cumulative Distribution Function for $\lambda$={self.a}; k={self.k}')
        plt.show()

        return





