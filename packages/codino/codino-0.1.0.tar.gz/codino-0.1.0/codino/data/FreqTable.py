class FreqTable:
    def __init__(self, freq: dict) -> None:
        """FreqTable class for manipulating frequency tables.

        Contains a frequency tables as a dictionary in the attribute freq, which
        stores keys as categories and values as frequencies. FreqTable includes
        methods to check, get and set the keys or values in the frequency table.
        """
        self._check_dict(freq)

        self._freq = freq

    @property
    def freq(self) -> dict:
        """Get frequency table.

        This gets the private attribute _freq. @property _freq should be be set
        through freq.setter.
        """
        return self._freq

    @freq.setter
    def freq(self, value: dict) -> None:
        """Set the keys/values in the frequency table.

        Updates the frequency table with inputted dictionary. The keys must be
        found in the existing frequency table. Values must either sum to 0
        (when refreshing) or 1.

        Args:
            value (dict): contains values to update the frequency table with.
        """
        self._check_dict(value)
        self._check_keys(value)
        self._check_values(value)

        self.freq.update(value)

    def refresh(self) -> None:
        """Refresh/reset the values in the frequency table to 0."""
        self.freq = dict.fromkeys(self.freq, 0)

    def get_non_0_freq(self) -> dict:
        """Obtain the elements with a non-0 frequency

        Returns:
            dict: contains elements with that have a frequency >0
        """
        return {k: v for (k, v) in self.freq.items() if v != 0.0}

    @staticmethod
    def _check_dict(value) -> None:
        """Check if value is a dictionary"""
        if type(value) is not dict:
            raise TypeError("Value must be a dictionary")

    def _check_keys(self, value: dict) -> None:
        """Check if input keys are part of freq keys"""
        poss_keys = self.freq.keys()

        if any([k not in poss_keys for k in value.keys()]):
            raise KeyError("Keys must be one of: " +
                           ", ".join(self.freq.keys()))

    def _check_values(self, value: dict) -> None:
        """Check if input values are between 0-1 and sum to 0/1"""
        if any([v > 1 or v < 0 for v in value.values()]):
            raise ValueError("Values must be between 0 and 1")

        # check that values sum to 0 (when calling .refresh) or 1
        # without changing the _freq attribute
        # round(X, 3) - avoid math errors causing problems
        tmp_freq = self._freq.copy()
        tmp_freq.update(value)

        if round(sum(tmp_freq.values()), 3) == 0:
            pass

        elif round(sum(tmp_freq.values()), 3) != 1:
            raise ValueError("Values must sum to 1")
