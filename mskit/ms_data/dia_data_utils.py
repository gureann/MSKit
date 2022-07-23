import numpy as np
import pandas as pd
from tqdm import tqdm

__all__ = [
    'extract_dia_window_mzml',
    'extract_tic_raw',
]


def extract_dia_window_mzml(
        mzml_file,
        cut_overlap_at_half: bool = False,
        half_overlap_as_margin: bool = False,
        columns=('lower_offset', 'upper_offset', 'margin'),
        max_iter_spec_num: int = 150,
        sort: bool = True,
        drop_duplicates: bool = True,
) -> pd.DataFrame:
    try:
        import pymzml
        dia_windows = []
        start_record = False
        with pymzml.run.Reader(mzml_file) as mzml:
            for idx, spec in enumerate(mzml):
                if spec.ms_level == 1:
                    if start_record:
                        used_cols = columns[:2]
                        window_df = pd.DataFrame(dia_windows, columns=used_cols)
                        if drop_duplicates:
                            window_df = window_df.drop_duplicates(used_cols)
                        if sort:
                            window_df = window_df.sort_values(list(used_cols))
                        return window_df
                    else:
                        start_record = True
                elif spec.ms_level == 2:
                    if start_record:
                        dia_windows.append((
                            spec.selected_precursors[0]['mz'] - spec['MS:1000828'],
                            spec.selected_precursors[0]['mz'] + spec['MS:1000829']
                        ))
                else:
                    pass  # OR Raise
                if idx > max_iter_spec_num:
                    if start_record:
                        raise ValueError(f'Iterate mzml file for {max_iter_spec_num} spectra but no further MS1 appear')
                    else:
                        raise ValueError(f'Iterate mzml file for {max_iter_spec_num} spectra but no MS1 spectrum appear')
    except ModuleNotFoundError:
        # import pyteomics
        raise ModuleNotFoundError('pymzml is not installed.')


def extract_tic_raw(msfile, out_file, sep='\t'):
    try:
        import pymsfilereader
    except ModuleNotFoundError:
        raise ModuleNotFoundError('pymsfilereader is not installed.')

    msfile = pymsfilereader.MSFileReader(msfile)
    try:
        spec_num = msfile.GetNumSpectra()
        print(f'Spectrum number: {spec_num}')
        with tqdm(range(1, spec_num + 1)) as t, open(out_file, 'w') as f:
            f.write(sep.join([
                'SpecNum', 'MSOrder',
                'RecordSignalNum', 'NonZeroSignalNum',
                'SummedSignal', 'Min', 'Max'
            ]))
            f.write('\n')
            for spec_idx in t:
                ms_order = msfile.GetMSOrderForScanNum(spec_idx)
                intens = np.array(msfile.GetMassListFromScanNum(spec_idx)[0][1])
                f.write(sep.join(map(str, [
                    spec_idx, ms_order,
                    len(intens), (intens > 0.5).sum(),
                    np.sum(intens), np.min(intens), np.max(intens)
                ])))
                f.write('\n')
    finally:
        msfile.Close()


def sum_extracted_tic_raw():
    _record = []
    for fname in my_bench_condition.MBMY_HF_Run_To_CondRepComb.keys():
        df = pd.read_csv(join_path(PATH_MY_Bench_RawTIC_SaveFolder, f'{fname}-AllSpec.txt'), sep='\t')
        ms1 = df[df['MSOrder'] == 1]
        ms2 = df[df['MSOrder'] == 2]
        ms1_tic = ms1['SummedSignal'].sum()
        ms2_tic = ms2['SummedSignal'].sum()
        total_tic = ms1_tic + ms2_tic
        _record.append([fname, len(ms1), len(ms2), ms1_tic, ms2_tic, total_tic])

    HF_TIC = pd.DataFrame(
        _record, columns=['File', 'MS1SpecNum', 'MS2SpecNum', 'MS1TIC', 'MS2TIC', 'MS1MS2TIC'])
    HF_TIC.insert(1, 'CondRep', HF_TIC['File'].map(my_bench_condition.MBMY_HF_Run_To_CondRepComb))
    _p = join_path(PATH_MY_Bench_RawTIC_SaveFolder, 'HF-TIC.txt')
    HF_TIC.to_csv(_p, sep='\t', index=False)
    rk.check_path(_p, shown_path_right_idx=3)


def extract_tic_tims():
    for file_idx, path in enumerate(PATH_RawData_MY_TIMS_DIA, 1):
        name = os.path.splitext(os.path.basename(path))[0]
        print('-' * 5, f'Loading analysis.tdf of {name}', '-' * 5)
        con, df = rk.load_one_sqlite_table(join_path(path, 'analysis.tdf'), 'Frames')
        con.close()

        _p = join_path(PATH_MY_Bench_RawTIC_SaveFolder, f'{name}-Frames.txt')
        print(f'Save to {name}-Frames.txt')
        df.to_csv(_p, sep='\t', index=False)


def sum_extracted_tic_tims():
    _record = []
    for fname in my_bench_condition.MBMY_TIMS_Run_To_CondRepComb.keys():
        df = pd.read_csv(join_path(PATH_MY_Bench_RawTIC_SaveFolder, f'{fname}-Frames.txt'), sep='\t')
        ms1 = df[df['MsMsType'] == 0]
        ms2 = df[df['MsMsType'] == 9]
        ms1_tic = ms1['SummedIntensities'].sum()
        ms2_tic = ms2['SummedIntensities'].sum()
        total_tic = ms1_tic + ms2_tic
        _record.append([
            fname, len(ms1), len(ms2),
            ms1['NumScans'].sum(), ms2['NumScans'].sum(),
            ms1['NumPeaks'].sum(), ms2['NumPeaks'].sum(),
            ms1_tic, ms2_tic, total_tic
        ])

    TIMS_TIC = pd.DataFrame(
        _record, columns=[
            'File', 'MS1FrameNum', 'MS2FrameNum',
            'MS1ScanNum', 'MS2ScanNum',
            'MS1PeakNum', 'MS2PeakNum',
            'MS1TIC', 'MS2TIC', 'MS1MS2TIC'
        ])
    TIMS_TIC.insert(1, 'CondRep', TIMS_TIC['File'].map(my_bench_condition.MBMY_TIMS_Run_To_CondRepComb))
    _p = join_path(PATH_MY_Bench_RawTIC_SaveFolder, 'TIMS-TIC.txt')
    TIMS_TIC.to_csv(_p, sep='\t', index=False)
    rk.check_path(_p, shown_path_right_idx=3)

