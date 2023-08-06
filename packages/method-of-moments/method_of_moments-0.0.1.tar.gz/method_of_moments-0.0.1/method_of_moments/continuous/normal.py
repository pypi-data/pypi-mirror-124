"""
This module contains description of function and class
for normal (Gauss) distribution.

References
----------
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html

"""


from scipy.stats import norm

from method_of_moments.continuous.base_continuous import BaseContinuousDistribution


class Norm(BaseContinuousDistribution):
    """
    Class for Normal (Gauss) Distribution.

    Parameters
    ----------
    **kwargs : `base.BaseDistribution` properties.

    """

    def __init__(self, **kwargs) -> None:
        """Initialize self. See help(type(self)) for accurate signature."""
        super().__init__(**kwargs)
        self.loc = self.mean
        self.scale = self.variance ** 0.5

    def pdf(self, arg: float) -> float:
        """Return Gauss probability density function."""
        return norm.pdf(arg, loc=self.loc, scale=self.scale)

    def cdf(self, arg: float, low_limit=-float('inf')) -> float:
        """Return Gauss cumulative density function."""
        return norm.cdf(arg, loc=self.loc, scale=self.scale)
