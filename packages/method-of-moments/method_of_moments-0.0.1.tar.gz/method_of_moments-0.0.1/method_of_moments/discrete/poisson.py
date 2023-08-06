"""
This module contains description of function and class
for poisson distribution.

References
----------
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html

"""


from scipy.stats import poisson

from method_of_moments.discrete.base_discrete import BaseDiscreteDistribution


class Poisson(BaseDiscreteDistribution):
    """
    Class for Poisson Distribution.

    Parameters
    ----------
    **kwargs : `base.BaseDistribution` properties.

    """

    def __init__(self, **kwargs) -> None:
        """Initialize self. See help(type(self)) for accurate signature."""
        super().__init__(**kwargs)
        if self.mean != self.variance:
            raise ValueError('Mean is not equal to variance')
        self.lmd = self.mean

    def pmf(self, arg: int) -> float:
        """Return Poisson probability mass function."""
        return poisson.pmf(arg, mu=self.lmd, loc=0)

    def cdf(self, arg: int) -> float:
        """Return Beta cumulative mass function."""
        return poisson.cdf(arg, mu=self.lmd, loc=0)
