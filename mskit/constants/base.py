"""

"""


class Base:
    BaseComb = {
        'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'U': 'U',
        'K': 'GT', 'M': 'AC', 'R': 'AG', 'S': 'CG', 'W': 'AT', 'Y': 'CT',
        'B': 'CGT', 'D': 'AGT', 'H': 'ACT', 'V': 'ACG',
        'N': 'ACGT',
    }

    BaseStart = 'ATG'
    BaseEnd = ['TAA', 'TGA', 'TAG']

    BaseReverse = {
        'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C', 'U': 'A',

        'K': 'M',
        'M': 'K',
        'R': 'Y',
        'S': 'S',
        'W': 'W',
        'Y': 'R',
        'N': 'N',
    }

    BaseToAA = {
        'GCT': 'A',
        'GCC': 'A',
        'GCA': 'A',
        'GCG': 'A',
        'CGT': 'R',
        'CGC': 'R',
        'CGA': 'R',
        'CGG': 'R',
        'AGA': 'R',
        'AGG': 'R',
        'AAT': 'N',
        'AAC': 'N',
        'GAT': 'D',
        'GAC': 'D',
        'TGT': 'C',
        'TGC': 'C',
        'CAA': 'Q',
        'CAG': 'Q',
        'GAA': 'E',
        'GAG': 'E',
        'GGT': 'G',
        'GGC': 'G',
        'GGA': 'G',
        'GGG': 'G',
        'CAT': 'H',
        'CAC': 'H',
        'ATT': 'I',
        'ATC': 'I',
        'ATA': 'I',
        'TTA': 'L',
        'TTG': 'L',
        'CTT': 'L',
        'CTC': 'L',
        'CTA': 'L',
        'CTG': 'L',
        'AAA': 'K',
        'AAG': 'K',
        'ATG': 'M',
        'TTT': 'F',
        'TTC': 'F',
        'CCT': 'P',
        'CCC': 'P',
        'CCA': 'P',
        'CCG': 'P',
        'TCT': 'S',
        'TCC': 'S',
        'TCA': 'S',
        'TCG': 'S',
        'AGT': 'S',
        'AGC': 'S',
        'ACT': 'T',
        'ACC': 'T',
        'ACA': 'T',
        'ACG': 'T',
        'TGG': 'W',
        'TAT': 'Y',
        'TAC': 'Y',
        'GTT': 'V',
        'GTC': 'V',
        'GTA': 'V',
        'GTG': 'V',
    }
