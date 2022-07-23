from collections import defaultdict


def _sort_prot_by_count(x, _prot_counts):
    _ps = sorted(list(x))
    _pc = [_prot_counts[_p] for _p in _ps]
    return [
        _ps[i] for i in
        [_[0] for _ in sorted(enumerate(_pc), key=lambda x: x[1], reverse=True)]
    ]


def reassign_prot_to_result(
        df,
        peptide_group_col='StrippedPeptide',
        all_potential_protein_col='PotentialProteins',
        added_count_sorted_protein_col='CountSortedPotentialProteins',
        fasta=None,
        ted=None,
):
    # TODO keep first N proteins with same count (at apply step, with two returned values)
    _prot_counts = defaultdict(int)

    if all_potential_protein_col is None:
        df[''] = ...

    for _c in df.drop_duplicates(peptide_group_col)[all_potential_protein_col].values:
        for _p in _c:
            _prot_counts[_p] += 1
    df[added_count_sorted_protein_col] = df[all_potential_protein_col].apply(_sort_prot_by_count, _prot_counts=_prot_counts)
    return df
