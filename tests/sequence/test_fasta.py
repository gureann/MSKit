import io
import os.path
import re
import unittest

from mskit import rapid_kit as rk
from mskit import sequence

_this_dir = os.path.abspath('.')
_test_folder = os.path.dirname(_this_dir)
PATH_FastaForTest = {
    'mouse_sp': 'Fasta-Mouse_10090-spOnly_10entries.fasta',
    'mouse_sp_tr_iso': 'Fasta-Mouse_10090-sp_tr_iso_200entries.fasta',
    'yeast_sp_tr': 'Fasta-Yeast_559292-sp_tr_8entries.fasta',
    'irt': 'Fasta-iRT-1entry.fasta',
}
PATH_FastaForTest = {
    name: os.path.join(_test_folder, 'TestData', f)
    for name, f in PATH_FastaForTest.items()
}


class FastaParserTestCase(unittest.TestCase):

    def test_xx(self):
        par = sequence.FastaFile(PATH_FastaForTest['mouse_sp'])


if __name__ == '__main__':
    unittest.main()
