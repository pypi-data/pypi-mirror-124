from codino.data import FreqTable


class CodonTable(FreqTable):
    def __init__(self) -> None:
        """CodonTable class for storing codon frequencies.

        Stores the frequency of each of the possible 64 codons.
        """

        codon_freq = {
            'AAA': 0.00,
            'AAC': 0.00,
            'AAG': 0.00,
            'AAT': 0.00,
            'ACA': 0.00,
            'ACC': 0.00,
            'ACG': 0.00,
            'ACT': 0.00,
            'AGA': 0.00,
            'AGC': 0.00,
            'AGG': 0.00,
            'AGT': 0.00,
            'ATA': 0.00,
            'ATC': 0.00,
            'ATG': 0.00,
            'ATT': 0.00,
            'CAA': 0.00,
            'CAC': 0.00,
            'CAG': 0.00,
            'CAT': 0.00,
            'CCA': 0.00,
            'CCC': 0.00,
            'CCG': 0.00,
            'CCT': 0.00,
            'CGA': 0.00,
            'CGC': 0.00,
            'CGG': 0.00,
            'CGT': 0.00,
            'CTA': 0.00,
            'CTC': 0.00,
            'CTG': 0.00,
            'CTT': 0.00,
            'GAA': 0.00,
            'GAC': 0.00,
            'GAG': 0.00,
            'GAT': 0.00,
            'GCA': 0.00,
            'GCC': 0.00,
            'GCG': 0.00,
            'GCT': 0.00,
            'GGA': 0.00,
            'GGC': 0.00,
            'GGG': 0.00,
            'GGT': 0.00,
            'GTA': 0.00,
            'GTC': 0.00,
            'GTG': 0.00,
            'GTT': 0.00,
            'TAA': 0.00,
            'TAC': 0.00,
            'TAG': 0.00,
            'TAT': 0.00,
            'TCA': 0.00,
            'TCC': 0.00,
            'TCG': 0.00,
            'TCT': 0.00,
            'TGA': 0.00,
            'TGC': 0.00,
            'TGG': 0.00,
            'TGT': 0.00,
            'TTA': 0.00,
            'TTC': 0.00,
            'TTG': 0.00,
            'TTT': 0.00
        }

        super().__init__(codon_freq)
