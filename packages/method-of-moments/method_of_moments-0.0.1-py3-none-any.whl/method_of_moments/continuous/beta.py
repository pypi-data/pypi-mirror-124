"""
This module contains description of class
for beta distribution initialized with mean and variance.

References
----------
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html

"""


from scipy.stats import beta

from method_of_moments.continuous.base_continuous import BaseContinuousDistribution


class Beta(BaseContinuousDistribution):
    """
    Class for Beta distribution.

    Parameters
    ----------
    max_bin : int
        The value of `scale` parameter for scipy.stats.beta.
    **kwargs : `base.BaseDistribution` properties.

    """

    def __init__(
            self,
            max_bin: int = 1,
            **kwargs,
    ) -> None:
        """Initialize self. See help(type(self)) for accurate signature."""
        super().__init__(**kwargs)
        self.max_bin = max_bin
        _factor = self.mean * (1 - self.mean) / self.variance - 1.0
        self.a_param = _factor * self.mean
        self.b_param = _factor * (1 - self.mean)

    @property
    def max_bin(self) -> int:
        """The value of `scale` parameter for scipy.stats.beta."""
        return self.__max_bin

    @max_bin.setter
    def max_bin(
            self,
            max_bin: int = 1,
    ) -> None:
        """Property setter for `self.max_bin`."""
        if max_bin < 0:
            raise ValueError('`max_bin` value must be positive.')
        self.__max_bin = max_bin

    def pdf(self, arg: float) -> float:
        """Return Beta probability density function."""
        return beta.pdf(
            arg,
            a=self.a_param,
            b=self.b_param,
            scale=self.max_bin,
        )

    def cdf(self, arg: float, low_limit: float = 0.0) -> float:
        """Return Beta cumulative density function."""
        return beta.cdf(
            arg,
            a=self.a_param,
            b=self.b_param,
            # scale=self.max_bin,
        )
