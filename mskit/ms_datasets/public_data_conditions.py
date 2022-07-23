"""
data name of each data
function of getting data by finding data name
"""


class RPE1DIA20NC:
    RPE1_AllRuns = [
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_NoSerum_01',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_NoSerum_02',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_NoSerum_03',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_EGF_01',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_EGF_02',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_EGF_03',

        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_0-5uM_01',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_0-5uM_02',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_0-5uM_03',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_5uM_01',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_5uM_02',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_5uM_03',

        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_0-5uM_01',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_0-5uM_02',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_0-5uM_03',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_5uM_01',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_5uM_02',
        '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_5uM_03',
    ]

    RPE1_AllConds = [
        'Control', 'EGF', 'Cob-L', 'Cob-H', 'PD-L', 'PD-H'
    ]

    RPE1_CondToRuns = {
        'Control': [
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_NoSerum_01',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_NoSerum_02',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_NoSerum_03',
        ],
        'EGF': [
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_EGF_01',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_EGF_02',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_EGF_03',
        ],
        'Cob-L': [
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_0-5uM_01',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_0-5uM_02',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_0-5uM_03',
        ],
        'Cob-H': [
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_5uM_01',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_5uM_02',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_Cobimetinib_5uM_03',
        ],
        'PD-L': [
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_0-5uM_01',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_0-5uM_02',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_0-5uM_03',
        ],
        'PD-H': [
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_5uM_01',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_5uM_02',
            '20171125_QE7_nLC14_DBJ_SA_DIAphos_RPE1_pilot2_PD0325901_5uM_03',
        ],
    }
