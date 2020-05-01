import os
from mskit.inherited_builtins import NonOverwriteDict


def read_prosit_fragment_result(prosit_result):
    """
    '[Oxidation (M)]'
    '[Carbamidomethyl (C)]'
    """
    with open(os.path.abspath(prosit_result), 'r') as prosit_handle:
        prosit_title = prosit_handle.readline()
        title_dict = dict([(__, _) for _, __ in enumerate(prosit_title.strip('\n').split(','))])
        predicted_fragment_data = dict()

        for each_line in prosit_handle:
            if not each_line or each_line == '\n':
                continue
            split_line = each_line.strip('\n').split(',')
            if split_line[0] == '0':
                continue

            loss_type = split_line[title_dict['FragmentLossType']]
            if loss_type != 'noloss':
                continue
            mod_pep = split_line[title_dict['ModifiedPeptide']]
            charge = split_line[title_dict['PrecursorCharge']]
            intensity = split_line[title_dict['RelativeIntensity']]
            fragment_num = split_line[title_dict['FragmentNumber']]
            fragment_type = split_line[title_dict['FragmentType']]
            fragment_charge = split_line[title_dict['FragmentCharge']]

            prec = charge + mod_pep
            fragment_name = '{}{}+{}'.format(fragment_type, fragment_num, fragment_charge)
            if prec not in predicted_fragment_data:
                predicted_fragment_data[prec] = {fragment_name: float(intensity)}
            else:
                predicted_fragment_data[prec][fragment_name] = float(intensity)
    return predicted_fragment_data


def read_prosit_irt_result(prosit_result):
    with open(os.path.abspath(prosit_result), 'r') as prosit_handle:
        prosit_title = prosit_handle.readline()
        title_dict = dict([(__, _) for _, __ in enumerate(prosit_title.strip('\n').split(','))])
        predicted_irt_data = NonOverwriteDict()

        for each_line in prosit_handle:
            if not each_line or each_line == '\n':
                continue
            split_line = each_line.strip('\n').split(',')
            if split_line[0] == '0':
                continue

            irt = split_line[title_dict['iRT']]
            mod_pep = split_line[title_dict['ModifiedPeptide']]

            int_replaced_pep = mod_pep.strip('_').replace('C[Carbamidomethyl (C)]', 'C').replace('M[Oxidation (M)]', '1')
            if '[' in int_replaced_pep:
                continue
            predicted_irt_data[int_replaced_pep] = float(irt)
    return predicted_irt_data
