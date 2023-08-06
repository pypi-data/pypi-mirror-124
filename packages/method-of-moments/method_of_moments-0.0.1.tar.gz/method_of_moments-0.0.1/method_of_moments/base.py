"""
This module contains description of abstract base class
for probability distributions initialized with mean and variance.

"""


from abc import ABC
from typing import Optional

from pretty_repr import RepresentableObject


class BaseDistribution(RepresentableObject, ABC):
    """
    Abstract class for probability method_of_moments.

    Parameters
    ----------
    mean : float
        Expected value of random variable.
    variance : float, optional
        Variance of random variable.
        If it is None, absolute value of `mean` is used.
    is_negative_mean_allowed : bool, optional, default: True
        Whether is negative expected value allowed.

    Raises
    ------
    ValueError
        If `mean` is negative while `is_negative_parameters_allowed` is False
        or `variance` is negative.

    """

    def __init__(
            self,
            mean: float,
            variance: Optional[float] = None,
            is_negative_mean_allowed: bool = True
    ) -> None:
        """Initialize self. See help(type(self)) for accurate signature."""
        self.is_negative_mean_allowed = is_negative_mean_allowed
        self.mean = mean
        self.variance = variance

    @property
    def mean(self) -> float:
        """Expected value of random variable."""
        return self.__mean

    @mean.setter
    def mean(self, mean: float) -> None:
        """Property setter for `self.mean`"""
        if mean < 0 and not self.is_negative_mean_allowed:
            raise ValueError('Mean value cannot be negative.')
        self.__mean = mean

    @property
    def variance(self) -> float:
        """Variance of random variable."""
        return self.__variance

    @variance.setter
    def variance(self, variance: Optional[float] = None) -> None:
        """Property setter for `self.variance`"""
        _variance = abs(self.mean) if variance is None else variance
        if _variance < 0:
            raise ValueError('Variance value cannot be negative.')
        self.__variance = _variance
