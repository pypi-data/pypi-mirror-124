"""
This module contains description of abstract base class
for continuous probability distributions initialized with mean and variance.

"""


from abc import abstractmethod

from scipy.integrate import quad

from method_of_moments.base import BaseDistribution
from method_of_moments.errors import NotDefinedError


class BaseContinuousDistribution(BaseDistribution):
    """
    Abstract class for continuous probability method_of_moments.

    Methods
    -------
    pdf(arg)
        Return probability density function.
    cdf(arg)
        Return cumulative density function.

    """

    @abstractmethod
    def pdf(self, arg: float) -> float:
        """Return probability density function."""
        raise NotDefinedError(self)

    def cdf(self, arg: float, low_limit: float = 0.0) -> float:
        """Return cumulative density function."""
        return quad(self.pdf, low_limit, arg)[0]
