"""
This module contains description of function and class
for generalized poisson distribution.

References
----------
P.C.Consul, G.C.Jain. A Generalization of the Poisson Distribution.
Technometrics, Vol. 15, No. 4, 1973, 791-799.

"""


from typing import Tuple

from math import exp, lgamma, log

from method_of_moments.discrete.base_discrete import BaseDiscreteDistribution


def get_generalized_poisson_distribution(
        arg: int,
        lmd_1: float,
        lmd_2: float,
) -> float:
    """Return GPD probability mass function with specified parameters."""
    if lmd_1 + arg * lmd_2 > 0.0:
        log_result = (
                log(lmd_1)
                + (arg - 1) * log(lmd_1 + arg * lmd_2) -
                (lmd_1 + arg * lmd_2) - lgamma(arg + 1)
        )
        return exp(log_result)
    return 0.0


class GPD(BaseDiscreteDistribution):
    """
    Class for Generalized Poisson Distribution (GPD).

    Parameters
    ----------
    **kwargs : `base.BaseDistribution` properties.

    """

    def __init__(self, **kwargs) -> None:
        """Initialize self. See help(type(self)) for accurate signature."""
        super().__init__(**kwargs)
        _parameter = (self.mean / self.variance) ** 0.5
        self.lmd_1 = self.mean * _parameter
        self.lmd_2 = 1 - _parameter

    def pmf(self, arg: int) -> float:
        """Return GPD probability mass function."""
        return get_generalized_poisson_distribution(
            arg=arg,
            lmd_1=self.lmd_1,
            lmd_2=self.lmd_2,
        )

    def get_parameters(self) -> Tuple[float, float]:
        """Return parameters of GPD."""
        return self.lmd_1, self.lmd_2
