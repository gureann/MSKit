import io
import re
import unittest

import pandas as pd

from mskit.calc import calc_ion_mz, calc_fragment_mz


class IonMZCalcTest(unittest.TestCase):

    @staticmethod
    def prepare_mz_data_1():
        test_mz_df = pd.read_csv(io.StringIO('''\
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	6	b	2	323.162501055777	b6-H3PO4+2
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	5	y	2	334.661179629632	y5-H3PO4+2
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	7	b	2	373.686340289982	b7-H3PO4+2
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	noloss	3	b	1	382.190737215382	b3-noloss+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	6	y	2	392.174651141547	y6-H3PO4+2
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	8	b	2	431.199811801897	b8-H3PO4+2
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	noloss	3	y	1	485.250694619652	y3-noloss+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	8	y	2	491.224872300177	y8-H3PO4+2
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	noloss	8	y	2	540.213321396857	y8-noloss+2
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	5	b	1	548.264961795893	b5-H3PO4+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	NH3	4	y	1	582.267073675172	y4-NH3+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	noloss	4	y	1	599.293622060792	y4-noloss+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	5	y	1	668.315082792453	y5-H3PO4+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	6	y	1	783.342025816283	y6-H3PO4+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	noloss	6	y	1	881.318924009642	y6-noloss+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	H3PO4	7	y	1	884.389704284693	y7-H3PO4+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	3	575.556167594322	noloss	7	y	1	982.366602478052	y7-noloss+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	noloss	3	b	1	382.190737215382	b3-noloss+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	H3PO4	5	b	1	548.264961795893	b5-H3PO4+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	H3PO4	5	y	1	668.315082792453	y5-H3PO4+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	H3PO4	11	y	2	679.792465675677	y11-H3PO4+2
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	noloss	5	y	1	766.291980985812	y5-noloss+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	H3PO4	8	y	1	981.442468133543	y8-H3PO4+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	noloss	8	y	1	1079.4193663269	y8-noloss+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	H3PO4	10	y	1	1245.49359090741	y10-H3PO4+1
_MHLPS[Phospho (STY)]PTDS[Phospho (STY)]NFYR_	MHLPS(UniMod:21)PTDS(UniMod:21)NFYR	2	862.830613158077	noloss	10	y	1	1343.47048910077	y10-noloss+1
'''), sep='\t', header=None)
        test_mz_df.columns = [
            'ModifiedPeptide',
            'UniModPep',
            'PrecursorCharge',
            'PrecursorMz',
            'FragmentLossType',
            'FragmentNumber',
            'FragmentType',
            'FragmentCharge',
            'FragmentMz',
            'FragName',
        ]
        return test_mz_df

    def test_mz_data_1(self):
        test_mz_df = self.prepare_mz_data_1()

        test_pep = test_mz_df['ModifiedPeptide'].iloc[0]
        mzs = calc_ion_mz(
            test_pep,
            [test_mz_df['PrecursorCharge'].astype(int).iloc[0], *test_mz_df['FragmentCharge'].astype(int).tolist()],
            ion_type=[None, *test_mz_df['FragmentType'].tolist()],
            ion_series_num=[None, *test_mz_df['FragmentNumber'].tolist()],
            ion_loss_type=[None, *test_mz_df['FragmentLossType'].tolist()],
            mod_mould='[',
            c_with_fixed_mod=False,
            pep_preprocess_func='underscore_dot',
        )

        mz_compare_df = test_mz_df[['FragName', 'FragmentMz']].copy()
        mz_compare_df['CalcFragMz'] = mzs[1:]
        print(mz_compare_df)
        print(test_mz_df['PrecursorMz'].astype(float).iloc[0], mzs[0])

        self.assertEqual(list(map(lambda x: round(x, 4), mzs, )),
                         list(map(lambda x: round(x, 4), [test_mz_df['PrecursorMz'].astype(float).iloc[0], *test_mz_df['FragmentMz'].astype(float).tolist()], )))

        test_pep = test_mz_df['UniModPep'].iloc[0]
        mzs = calc_ion_mz(
            test_pep,
            [test_mz_df['PrecursorCharge'].astype(int).iloc[0], *test_mz_df['FragmentCharge'].astype(int).tolist()],
            ion_type=[None, *test_mz_df['FragmentType'].tolist()],
            ion_series_num=[None, *test_mz_df['FragmentNumber'].tolist()],
            ion_loss_type=[None, *test_mz_df['FragmentLossType'].tolist()],
            mod_mould='(',
            c_with_fixed_mod=False,
            pep_preprocess_func=None,
        )

        mz_compare_df = test_mz_df[['FragName', 'FragmentMz']].copy()
        mz_compare_df['CalcFragMz'] = mzs[1:]

        self.assertEqual(list(map(lambda x: round(x, 4), mzs, )),
                         list(map(lambda x: round(x, 4), [test_mz_df['PrecursorMz'].astype(float).iloc[0], *test_mz_df['FragmentMz'].astype(float).tolist()], )))

    @staticmethod
    def prepare_mz_data_2():
        test_mz_df = pd.read_csv(io.StringIO('''\
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	NH3	11	b	4	316.149686526439	b11+4-NH3
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H2O	3	y	1	357.213246361395	y3+1-H2O
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	3	y	1	375.223811165472	y3+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	3	b	1	432.179897748162	b3+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H2O	4	b	1	529.196275967915	b4+1-H2O
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	4	b	1	547.206840771992	b4+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H2O	5	y	1	583.308603298215	y5+1-H2O
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	5	y	1	601.319168102292	y5+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	5	b	1	660.290904749122	b5+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H3PO4	18	y	3	663.994228042505	y18+3-H3PO4
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H3PO4	20	y	3	715.352303898979	y20+3-H3PO4
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H2O	6	b	1	729.312368349315	b6+1-H2O
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	13	y	2	737.898648228737	y13+2-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	6	b	1	747.322933153392	b6+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	20	y	3	748.011269963432	y20+3-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	22	y	3	804.041229174619	y22+3-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	7	y	1	811.455995928272	y7+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H3PO4	17	y	2	904.980699335772	y17+2-H3PO4
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	8	y	1	912.503674396682	y8+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H2O	17	y	2	944.963866030413	y17+2-H2O
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	NH3	17	y	2	945.455874239642	y17+2-NH3
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	17	y	2	953.969148432452	y17+2-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H3PO4	20	y	2	1072.52481761506	y20+2-H3PO4
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	20	y	2	1121.51326671174	y20+2-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H3PO4	22	y	2	1156.56975643184	y22+2-H3PO4
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H2O	11	y	1	1203.62558031413	y11+1-H2O
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	22	y	2	1205.55820552852	y22+2-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	11	y	1	1221.63614511821	y11+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H2O	13	b	1	1434.6569570954	b13+1-H2O
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	NH3	13	b	1	1435.64097351386	b13+1-NH3
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	13	b	1	1452.66752189948	b13+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	H2O	13	y	1	1456.77945518658	y13+1-H2O
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	13	y	1	1474.79001999066	y13+1-noloss
_[Acetyl (Protein N-term)]M[Oxidation (M)]ELDLSPPHLSSSPEDLC[Carbamidomethyl (C)]PAPGT[Phospho (STY)]PPGT[Phospho (STY)]PRPPDTPLPEEVK_	4	1119.7570554666	noloss	16	b	1	1793.78982186013	b16+1-noloss'''), sep='\t', header=None)
        test_mz_df.columns = [
            'ModifiedPeptide',
            'PrecursorCharge',
            'PrecursorMz',
            'FragmentLossType',
            'FragmentNumber',
            'FragmentType',
            'FragmentCharge',
            'FragmentMz',
            'FragName',
        ]
        return test_mz_df

    def test_mz_data_2(self):
        test_mz_df = self.prepare_mz_data_2()

        test_pep = test_mz_df['ModifiedPeptide'].iloc[0]
        mzs = calc_ion_mz(
            test_pep,
            [test_mz_df['PrecursorCharge'].astype(int).iloc[0], *test_mz_df['FragmentCharge'].astype(int).tolist()],
            ion_type=[None, *test_mz_df['FragmentType'].tolist()],
            ion_series_num=[None, *test_mz_df['FragmentNumber'].tolist()],
            ion_loss_type=[None, *test_mz_df['FragmentLossType'].tolist()],
            mod_mould='[',
            c_with_fixed_mod=False,
            pep_preprocess_func='underscore_dot',
        )

        mz_compare_df = test_mz_df[['FragName', 'FragmentMz']].copy()
        mz_compare_df['CalcFragMz'] = mzs[1:]
        print(mz_compare_df)
        print(test_mz_df['PrecursorMz'].astype(float).iloc[0], mzs[0])

        self.assertEqual(list(map(lambda x: round(x, 4), mzs, )),
                         list(map(lambda x: round(x, 4), [test_mz_df['PrecursorMz'].astype(float).iloc[0], *test_mz_df['FragmentMz'].astype(float).tolist()], )))


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
