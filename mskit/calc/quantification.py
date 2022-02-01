import typing

import numpy as np
import pandas as pd

__all__ = [
    'assemble_topn',
    'norm_quant_by_ref_median'
]


def assemble_topn(
        values: typing.Union[list, tuple, np.ndarray, pd.Series],
        topn: typing.Union[int, None, bool] = 3,
        assemble_func: typing.Union[str, typing.Callable] = np.mean,
        nan_value=np.nan,
        thres: typing.Union[int, float, np.ndarray, pd.Series] = 10
):
    """
    :param values:

    :param topn:
        int to keep top n items or True for top 3, or others with no action
    :param assemble_func:

    :param nan_value:

    :param thres:

    """
    values = np.array(values)
    if isinstance(thres, (int, float, np.ndarray, pd.Series)):
        values = values[values > thres]
    elif thres is True:
        values = values[values > 1]

    if len(values) == 0:
        return nan_value
    if isinstance(topn, bool):
        topn = 3 if topn else 0
    if isinstance(topn, int) and topn >= 1:
        values = np.sort(values)[::-1][:topn]

    if isinstance(assemble_func, str):
        if assemble_func.lower() in ('mean', 'nanmean', 'np.mean', 'np.nanmean', ):
            assemble_func = np.nanmean
        elif assemble_func.lower() in ('median', 'nanmedian', 'np.median', 'np.nanmedian', ):
            assemble_func = np.nanmedian
        elif assemble_func.lower() in ('sum', 'nansum', 'np.sum', 'np.nansum', ):
            assemble_func = np.nansum
        else:
            raise ValueError(f'`assemble_func` should be callable object or string. When is string, should be one of `mean`, `median`, or `sum`')

    return assemble_func(values)


def norm_quant_by_ref_median(
        df: pd.DataFrame,
        run_colname='R.FileName',
        quant_colname='FG.Quantity',
        ref_run_name='Ref',
) -> pd.Series:
    ref_run_median_quant = df[df[run_colname] == ref_run_name][quant_colname].median()
    return df[quant_colname] / df.groupby(run_colname)[quant_colname].transform(np.nanmedian) * ref_run_median_quant
