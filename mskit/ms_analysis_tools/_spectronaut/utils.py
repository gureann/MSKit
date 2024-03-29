import os
import re

import numpy as np
import pandas as pd

from mskit import calc
from mskit import rapid_kit
from .sn_constant import SNLibraryTitle

__all__ = [
    'filter_inten_neutral_loss_pos',
    'sn_modpep_to_unimodpep',
    'get_lib_prec',
    'select_target_run_df',
    'get_library_info',
    'merge_lib',
    'norm_params',
    'get_lib_rt_info',
    'get_lib_fragment_info',
    'write_lib',
]


def filter_inten_neutral_loss_pos(
        modpep,
        intens,
        exclude_mod_in_pep='[Phospho (STY)]',
        exclude_res=('S', 'T'),
        exclude_frag_losstype='H3PO4'
):
    """
    TODO 这里只是对最小和最大可以出现磷酸根丢失的位点进行 filter，如果需要进一步对应磷酸化修饰数量，应该指定 b/y 之后建一个每个位置的数量 list
    TODO 如果目的不止是为了筛选正确的丢失位点，则最好直接产生一条肽段所有可能的 fragments

    *Suspend*

    :param modpep: This should be a phosphopeptide with general format like _XXXXXS[Phospho (STY)]XXXX_
    :param intens: a intensity dict
    """
    strip_pep, mod_pos, mods = rapid_kit.substring_finder(modpep.replace('_', ''))
    phos_mod_pos = [mod_pos[i] for i, mod in enumerate(mods) if mod == exclude_mod_in_pep]
    st_phosmod_pos = [s for s in phos_mod_pos if strip_pep[s - 1] in exclude_res]
    if st_phosmod_pos:
        positive_min_phos_site = min(st_phosmod_pos)
        negetive_min_phos_site = len(strip_pep) - max(st_phosmod_pos) + 1
    else:
        positive_min_phos_site = len(strip_pep) + 1
        negetive_min_phos_site = len(strip_pep) + 1
    new_frag_dict = dict()
    for frag_name, inten in intens.items():
        frag_type, frag_num, frag_charge, frag_losstype = re.findall(r'([by])(\d+)\+(\d)-(.+)', frag_name)[0]
        if ',' in frag_losstype:
            frag_losstype = frag_losstype.split(',')[1]
        if frag_losstype == exclude_frag_losstype:
            if frag_type == 'b' and frag_num < positive_min_phos_site:
                continue
            elif frag_type == 'y' and frag_num < negetive_min_phos_site:
                continue
            else:
                raise
        new_frag_dict[frag_name] = inten


def filter_inten_dict_with_phosloss(inten):
    pass


def sn_modpep_to_unimodpep(x):
    x = x.replace('_', '')
    if '[Acetyl (Protein N-term)]' in x:
        x = x.replace('[Acetyl (Protein N-term)]', '')
        x = f'(UniMod:1){x}'
    for sn_mod, unimod in {
        '[Carbamidomethyl (C)]': '(UniMod:4)',
        '[Oxidation (M)]': '(UniMod:35)',
        '[Phospho (STY)]': '(UniMod:21)',
    }.items():
        x = x.replace(sn_mod, unimod)
    return x


def get_lib_prec(lib_df):
    prec = lib_df.apply(lambda x: x['ModifiedPeptide'] + '.' + str(x['PrecursorCharge']), axis=1)
    return prec


def select_target_run_df(df, region_ident, return_col_list=None):
    colname = 'R.Instrument (parsed from filename)'
    return rapid_kit.extract_df_with_col_ident(df, colname, region_ident, return_col_list)


def get_library_info(lib_path):
    lib_df = pd.read_csv(lib_path, sep='\t', low_memory=False)
    protein_groups_num = len(lib_df['ProteinGroups'].drop_duplicates())
    precursor_num = len((lib_df['PrecursorCharge'].astype(str) + lib_df['ModifiedPeptide']).drop_duplicates())
    modpep_num = len(lib_df['ModifiedPeptide'].drop_duplicates())
    return protein_groups_num, precursor_num, modpep_num


def merge_lib(main_lib, accomp_lib, drop_col=('ProteinGroups',)):
    """
    :param main_lib: main library
    :param accomp_lib: accompanying library. Overlapped precursors with main lib in this lib will be deleted
    :param drop_col:
    :return:
    """
    if not isinstance(main_lib, pd.DataFrame):
        main_lib = pd.read_csv(main_lib, sep='\t')
    if not isinstance(accomp_lib, pd.DataFrame):
        accomp_lib = pd.read_csv(accomp_lib, sep='\t')

    main_prec = set(main_lib.apply(lambda x: x['ModifiedPeptide'] + str(x['PrecursorCharge']), axis=1))
    accomp_lib = accomp_lib[~(accomp_lib['ModifiedPeptide'] + accomp_lib['PrecursorCharge'].astype(str)).isin(main_prec)]

    hybrid_lib = main_lib.append(accomp_lib)
    if drop_col:
        hybrid_lib = hybrid_lib.drop(drop_col, axis=1)
    return hybrid_lib


def norm_params(original_df, params_list, norm_func=np.nanmedian, focus_col='EG.ModifiedPeptide'):
    """
    This function is used to get the median value or others depends on the norm func of given params list when one focus is detected in multi reps
    """
    grouped_df = original_df.groupby(focus_col)
    norm_param_df = grouped_df[params_list].transform(norm_func)
    norm_colname = [_ + '_norm' for _ in params_list]
    norm_param_df.columns = norm_colname
    normed_df = pd.concat([original_df, norm_param_df], axis=1)
    return normed_df


def get_lib_rt_info(lib, pep_col='ModifiedPeptide', rt_col='iRT', return_type='dict'):
    rt_df = lib[[pep_col, rt_col]]
    non_redundant_rt_df = rt_df.drop_duplicates(pep_col)
    rt_dict = dict(non_redundant_rt_df.set_index(pep_col)[rt_col])
    if return_type == 'dict':
        return rt_dict
    elif return_type == 'list':
        return [(k, v) for k, v in rt_dict.items()]
    else:
        raise


def get_lib_fragment_info(lib, norm=False):
    """
    Extract fragment intensity info of precursors from library
    :param lib: spectral library path or dataframe
    :param norm:
    :return: A dict has precursors (modpep.charge) as key, and fragment info (a dict has key-value pair like 'b5+1-noloss': 21.1) as value
    """
    if not isinstance(lib, pd.DataFrame):
        if os.path.isfile(lib):
            lib = pd.read_csv(lib, sep='\t')
        else:
            raise
    if 'Precursor' not in lib.columns:
        lib['Precursor'] = lib.apply(lambda x: x['ModifiedPeptide'] + '.' + str(x['PrecursorCharge']), axis=1)

    def _get_group_frag_data(one_group):
        frags = one_group.apply(lambda x: x['FragmentType'] + str(x['FragmentNumber']) + '+' + str(x['FragmentCharge']) + '-' + x['FragmentLossType'], axis=1)
        intens = one_group['RelativeIntensity']
        if norm:
            calc.normalize_intensity(list(intens), norm)
        return dict(zip(frags, intens))

    frag_info = lib.groupby('Precursor').apply(_get_group_frag_data)
    frag_dict = dict(frag_info)
    return frag_dict


def write_lib(output_path, inten_dict: dict, rt_dict: dict, seq2protein_dict=None):
    """
    This function is based on the precursors in inten_dict.
    Seq not in rt_dict will pass
    Seq not in seq2protein_dict will make protein as ''
    Fragment with no loss type will be noloss
    :param output_path:
    :param inten_dict:
    :param rt_dict:
    :param seq2protein_dict:
    :return:
    """
    if seq2protein_dict:
        title_list = SNLibraryTitle.LibraryMainCol
    else:
        title_list = SNLibraryTitle.LibraryMainColPGOut

    with open(output_path, 'w') as _out:
        lib_title = '\t'.join(title_list)
        _out.write(lib_title + '\n')

        for each_prec, frag_dict in inten_dict.items():
            modpep, charge = rapid_kit.split_prec(each_prec, keep_underscore=True)
            if modpep in rt_dict:
                irt = rt_dict[modpep]
            else:
                continue
            stripped_pep, mod = rapid_kit.split_mod(modpep, mod_ident='bracket')
            mod = mod.split(' ')[0]
            prec_mz = calc.calc_prec_mz(stripped_pep, charge, mod)
            if seq2protein_dict:
                protein_acc = seq2protein_dict[stripped_pep] if stripped_pep in seq2protein_dict else ''
                protein_acc = protein_acc if isinstance(protein_acc, str) else ';'.join(set(protein_acc))
            else:
                protein_acc = ''
            for frag_name, frag_inten in frag_dict.items():
                frag_type, frag_num, frag_charge, frag_loss = rapid_kit.split_fragment_name(frag_name)
                frag_loss = frag_loss if frag_loss else 'noloss'
                fragment_mz = calc.calc_fragment_mz_old(stripped_pep, frag_type, frag_num, frag_charge, mod=mod)
                one_row_list = [charge, modpep, stripped_pep, irt,
                                modpep, prec_mz, frag_loss, frag_num,
                                frag_type, frag_charge, fragment_mz, frag_inten]
                one_row_list = list(map(str, one_row_list))
                if seq2protein_dict:
                    one_row_list.append(protein_acc)
                lib_line = "\t".join(one_row_list)
                _out.write(lib_line + '\n')
