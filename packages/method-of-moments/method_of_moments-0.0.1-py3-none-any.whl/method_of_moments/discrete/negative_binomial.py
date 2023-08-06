"""
This module contains description of function and class
for negative binomial distribution.

References
----------
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.nbinom.html

"""


from math_round_af import get_rounded_number
from scipy.stats import nbinom

from method_of_moments.discrete.base_discrete import BaseDiscreteDistribution


class NBD(BaseDiscreteDistribution):
    """
    Class for Negative Binomial Distribution (NBD).

    Parameters
    ----------
    **kwargs : `base.BaseDistribution` properties.

    """

    def __init__(self, **kwargs) -> None:
        """Initialize self. See help(type(self)) for accurate signature."""
        super().__init__(**kwargs)
        self.success_probability = self.mean / self.variance
        self.successes = int(get_rounded_number(
            self.mean * self.success_probability
            / (1. - self.success_probability)
        ))

    def pmf(self, arg: int) -> float:
        """Return NBD probability mass function."""
        return nbinom.pmf(
            k=arg,
            n=self.successes,
            p=self.success_probability,
        )

    def cdf(self, arg: int) -> float:
        """Return NBD cumulative mass function."""
        return nbinom.cdf(
            k=arg,
            n=self.successes,
            p=self.success_probability,
        )
