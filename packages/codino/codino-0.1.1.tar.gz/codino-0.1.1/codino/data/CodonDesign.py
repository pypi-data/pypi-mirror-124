from codino.data import FreqTable


class CodonDesign:
    def __init__(self) -> None:
        """CodonDesign class for storing codon designs.

        Stores the frequency of each nucleotide (A/T/C/G) at each position
        (1/2/3) of a codon. Frequencies are stored in FreqTables.
        """
        self.first = FreqTable({"A": 0.0,
                                "T": 0.0,
                                "C": 0.0,
                                "G": 0.0})

        self.second = FreqTable({"A": 0.0,
                                 "T": 0.0,
                                 "C": 0.0,
                                 "G": 0.0})

        self.third = FreqTable({"A": 0.0,
                                "T": 0.0,
                                "C": 0.0,
                                "G": 0.0})

    def set_codon_design(self, first: dict, second: dict, third: dict) -> None:
        """Method for setting the codon design

        Sets the frequency of the nucleotides at the 3 positions.

        Args:
            first (dict): nucleotide frequencies for first position.
            second (dict): nucleotide frequencies for second position.
            third (dict): nucleotide frequencies for third position.
        """
        self.first.freq = first
        self.second.freq = second
        self.third.freq = third
