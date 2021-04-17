import io
import re
import unittest

import pandas as pd

from mskit.calc import calc_fragment_mz


class FragMZCalcTest(unittest.TestCase):

    @staticmethod
    def prepare_frag_mz_data_1():
        test_pep = '_M[Oxidation (M)]S[Phospho (STY)]GFIYQGK_'
        test_mz_df = pd.read_csv(io.StringIO('''\
noloss	3	b	1	372.0624986
noloss	3	y	1	332.1928454
noloss	4	b	1	519.1309126
noloss	4	y	1	495.2561739
H3PO4	4	b	1	421.1540144
noloss	5	b	1	632.2149765
noloss	5	y	1	608.3402379
H3PO4	5	b	1	534.2380783
noloss	6	y	1	755.4086518
H3PO4	6	b	1	697.3014069
noloss	7	y	1	812.4301155
H3PO4	7	b	1	825.3599844
noloss	8	y	1	979.4284745
H3PO4	8	y	1	881.4515763
NH3	3	y	1	315.166297
NH3	4	y	1	478.2296255
NH3	5	y	1	591.3136895
1(+H2+O)1(+H3+O4+P)	8	y	1	863.4410115
noloss	6	y	2	378.2079641
1(+H2+O)1(+H3+O4+P)	7	b	1	807.3494253\
'''), sep='\t', header=None)
        test_mz_df.columns = ['LossType', 'FragNum', 'FragType', 'FragCharge', 'MZ']
        test_mz_df['TestFrag'] = test_mz_df.apply(
            lambda x: x['FragType'] + str(x['FragNum']) + '+' + str(x['FragCharge']) + '-' + {
                'noloss': 'Noloss',
                'H3PO4': '1,H3PO4',
                'NH3': '1,NH3',
                '1(+H2+O)1(+H3+O4+P)': '1,H2O;1,H3PO4'
            }[x['LossType']], axis=1)
        return test_pep, test_mz_df

    def test_frag_mz_data_1(self):
        test_pep, test_mz_df = self.prepare_frag_mz_data_1()
        calc_mz_list = []
        for frag in test_mz_df['TestFrag'].tolist():
            frag_type, frag_num, frag_charge, frag_losstype = re.findall(
                '([abcxyz])(\d+)\+(\d)-(.+)', frag)[0]
            calc_mz_list.append([frag, calc_fragment_mz(test_pep, frag_type, frag_num, frag_charge, frag_losstype)])
        calc_mz_df = pd.DataFrame(calc_mz_list, columns=['PredFrag', 'CalcMZ'])
        mz_compare_df = pd.merge(test_mz_df, calc_mz_df, left_on='TestFrag', right_on='PredFrag')
        print(mz_compare_df[['TestFrag', 'PredFrag', 'MZ', 'CalcMZ']])
        self.assertEqual(list(map(lambda x: round(x, 4), test_mz_df['MZ'].values, )),
                         list(map(lambda x: round(x, 4), mz_compare_df['CalcMZ'].values, )))


if __name__ == '__main__':
    unittest.main()
