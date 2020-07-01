import re


def ion_info_from_mq(need_ion_type=('b', 'y'), verify_mass=True, verify_tolerance=20):
    pass


def inten_from_mq(x):
    raw_file = x['Raw file']
    scan_number = x['Scan number']
    charge = x['Charge']

    pep = x['Sequence']
    mod_pep = x['Modified sequence']
    mod_info = pdeep_mod_extraction(mod_pep)

    ions = x['Matches']
    intens = x['Intensities']

    ion_intens_list = list(zip(ions.split(';'), intens.split(';')))

    inten_dict = dict()

    for ion_type in ['b', 'y']:
        ion_info = [_ for _ in ion_intens_list if _[0].startswith(ion_type)]

        current_num = 0
        _mod_start = 0
        for ion, inten in ion_info:

            ion_num = re.findall(f'{ion_type}(\d+)', ion)[0]
            ion_num = int(ion_num)

            re_charge = re.findall('\((\d)\+\)', ion)
            if re_charge:
                ion_charge = re_charge[0]
            else:
                ion_charge = '1'

            if '*' in ion:
                if _mod_start == 0:
                    current_num = 0
                    _mod_start = 1
                elif _mod_start == 1:
                    if ion_num <= current_num:
                        _mod_start = 2
                    else:
                        pass
                else:
                    pass
            if '-' in ion:
                loss_type = re.findall('-(.+)$', ion)[0]

            current_num = ion_num
            frag = f'{ion_type}{str(ion_num)}+{ion_charge}'

            if '*' in ion:
                frag += f'-{_mod_start},Phospho (STY);'
                if '-' in ion:
                    frag += f'1,{loss_type};'
            elif '-' in ion:
                frag += f'-1,{loss_type};'
            else:
                pass

            inten_dict[frag] = inten

    one_psm_data = {
        'Raw': raw_file,
        'Scan number': scan_number,
        'Charge': charge,
        'Pep': pep,
        'Modpep': mod_pep,
        'Mod info': mod_info,
        'Frag inten': inten_dict,
    }
    return f'{mod_pep}.{charge}', one_psm_data

