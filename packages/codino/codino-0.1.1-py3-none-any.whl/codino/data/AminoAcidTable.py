from codino.data import FreqTable


class AminoAcidTable(FreqTable):
    def __init__(self) -> None:
        """AminoAcidTable class for storing AA frequencies and mapping.

        Stores the frequency of each AA as well as a map, detailing which of the
        codons is translated into which AA.
        """
        # codons are stored as lists - consider an immutable type, tuples?
        self._aa_to_codon = {
            "C": ["TGC", "TGT"],
            "S": ["AGC", "AGT", "TCA", "TCC", "TCG", "TCT"],
            "T": ["ACA", "ACC", "ACG", "ACT"],
            "P": ["CCA", "CCC", "CCG", "CCT"],
            "A": ["GCA", "GCC", "GCG", "GCT"],
            "G": ["GGA", "GGC", "GGG", "GGT"],
            "N": ["AAC", "AAT"],
            "D": ["GAC", "GAT"],
            "E": ["GAA", "GAG"],
            "Q": ["CAA", "CAG"],
            "H": ["CAC", "CAT"],
            "R": ["AGA", "AGG", "CGA", "CGC", "CGG", "CGT"],
            "K": ["AAA", "AAG"],
            "M": ["ATG"],
            "I": ["ATA", "ATC", "ATT"],
            "L": ["CTA", "CTC", "CTG", "CTT", "TTA", "TTG"],
            "V": ["GTA", "GTC", "GTG", "GTT"],
            "F": ["TTC", "TTT"],
            "Y": ["TAC", "TAT"],
            "W": ["TGG"],
            "X": ["TAA", "TAG", "TGA"]
        }

        aa_freq = {
            "A": 0.00,
            "C": 0.00,
            "D": 0.00,
            "E": 0.00,
            "F": 0.00,
            "G": 0.00,
            "H": 0.00,
            "I": 0.00,
            "K": 0.00,
            "L": 0.00,
            "M": 0.00,
            "N": 0.00,
            "P": 0.00,
            "Q": 0.00,
            "R": 0.00,
            "S": 0.00,
            "T": 0.00,
            "V": 0.00,
            "W": 0.00,
            "X": 0.00,
            "Y": 0.00
        }

        super().__init__(aa_freq)

    @property
    def aa_to_codon(self) -> dict:
        """Obtain the AA to codon mapping

        Returns:
            dict: details which AAs are encoded by which codons.
        """
        return self._aa_to_codon
