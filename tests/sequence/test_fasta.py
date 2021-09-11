import io
import re
import unittest

from mskit.sequence import fasta


PATH_FastaForTest = {
    'mouse_sp': 'Fasta-Mouse_10090-spOnly_10entries.fasta',
    'mouse_sp_tr_iso': 'Fasta-Mouse_10090-sp_tr_iso_200entries.fasta',
    'yeast_sp_tr': 'Fasta-Yeast_559292-sp_tr_8entries.fasta',
    'irt': 'Fasta-iRT-1entry.fasta',
}


class FastaParserTestCase(unittest.TestCase):


    def test_xx(self):
        pass


if __name__ == '__main__':
    unittest.main()
