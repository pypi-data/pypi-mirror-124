from codino.data import CodonDesign, CodonTable, AminoAcidTable


class Converter:
    def __init__(self) -> None:
        """Converter class for converting codon designs to amino acid
        frequencies.

        Contains methods to take as input the codon design (frequency of
        nucleotides at each position) then return the AA frequencies they would
        be predicted to generate. In future, Converter will hopefully also be
        able to do the reverse.
        """
        self.cd = CodonDesign()
        self.ct = CodonTable()
        self.aat = AminoAcidTable()

    def cd_to_aa(self, first: dict, second: dict, third: dict,
                 refresh: bool = True) -> dict:
        """Convert codon design to AA frequencies

        Takes as input the nucleotide frequencies at each position in a codon,
        then calculates the predicted AA frequencies.

       Args:
            first (dict): nucleotide frequencies for first position.
            second (dict): nucleotide frequencies for second position.
            third (dict): nucleotide frequencies for third position.
            refresh (bool): Whether to refresh the frequencies in the Convertor
            after obtaining the AA frequencies.

        Returns:
            dict: Frequencies of the AA which are predicted to be generated from
            the codon design.
        """
        self.cd.set_codon_design(first, second, third)
        self._cd_to_ct()
        self._ct_to_aa()

        aa_freq = self.aat.get_non_0_freq().copy()

        if refresh:
            self.refresh()

        return aa_freq

    def aa_to_cd(self, aa: dict, refresh: bool = True) -> tuple:
        """Convert AA frequencies to codon design

       Args:
            aa (dict): AA frequencies.
            refresh (bool): Whether to refresh the frequencies in the Convertor
            after obtaining the codon design.

        Returns:
            tuple: Estimated codon design to obtain the inputted AA
            frequencies.
        """
        self.aat.freq = aa
        self._aa_to_cd()

        cd_freq = (self.cd.first.get_non_0_freq(),
                   self.cd.second.get_non_0_freq(),
                   self.cd.third.get_non_0_freq())

        if refresh:
            self.refresh()

        return cd_freq

    def _cd_to_ct(self) -> None:
        """Convert codon design into codon frequencies"""
        new_freq = {}
        for k1 in self.cd.first.freq:
            if self.cd.first.freq[k1] == 0.0:
                continue
            for k2 in self.cd.second.freq:
                if self.cd.second.freq[k2] == 0.0:
                    continue
                for k3 in self.cd.third.freq:
                    if self.cd.third.freq[k3] == 0.0:
                        continue
                    codon = k1 + k2 + k3
                    freq = self.cd.first.freq[k1] * \
                           self.cd.second.freq[k2] * \
                           self.cd.third.freq[k3]

                    new_freq[codon] = freq

        # use freq.setter - check values sum to 1
        self.ct.freq = new_freq

    def _ct_to_aa(self) -> None:
        """Convert codon frequencies to AA frequencies"""
        for aa, codons in self.aat.aa_to_codon.items():
            # using list comprehension - try a generator here?
            freq = sum([self.ct.freq[c] for c in codons])
            self.aat.freq[aa] = freq

    def _aa_to_cd(self) -> None:
        """Convert AA frequencies to codon frequencies"""
        first = {"A": 0, "T": 0, "C": 0, "G": 0}
        second = {"A": 0, "T": 0, "C": 0, "G": 0}
        third = {"A": 0, "T": 0, "C": 0, "G": 0}

        # for each aa, for each codon, for each nucleotide
        # sum the exp freq for the original AA divided by number of codons
        # this will be an estimate of the codon design
        for aa, freq in self.aat.get_non_0_freq().items():
            codons = self.aat.aa_to_codon[aa]
            for c in codons:
                first[c[0]] = first.get(c[0], 0) + freq/len(codons)
                second[c[1]] = second.get(c[1], 0) + freq/len(codons)
                third[c[2]] = third.get(c[2], 0) + freq/len(codons)

        self.cd.first.freq = first
        self.cd.second.freq = second
        self.cd.third.freq = third

    def refresh(self) -> None:
        """Refresh the frequencies in the codon design, codon table and AA table
        back to 0.
        """
        self.cd.first.refresh()
        self.cd.second.refresh()
        self.cd.third.refresh()
        self.ct.refresh()
        self.aat.refresh()
