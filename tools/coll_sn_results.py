import filecmp
import os
import shutil
from pprint import pprint

ddir = r''

col_folder_name = os.path.basename(ddir)
col_folder = os.path.join(ddir, col_folder_name)
try:
    os.makedirs(col_folder, exist_ok=True)

except FileNotFoundError:
    col_folder_name = 'Collection'
    col_folder = os.path.join(ddir, col_folder_name)
    os.makedirs(col_folder, exist_ok=True)

print(f'Used collection folder name: {col_folder_name}')

result_names = [_ for _ in os.listdir(ddir) if _ != 'Collection' and _ != col_folder_name]
print(len(result_names))
pprint(result_names)

for i, name in enumerate(result_names, 1):
    print(f'---- {i}/{len(result_names)}----')

    curr_result_folder = os.path.join(ddir, name)
    try:

        original_file_path = os.path.join(curr_result_folder, 'Report_General-SN15_0 (Normal).xls')

        # target_filename_prefix = '_'.join(name.split('_')[2:])
        target_filename_prefix = name.replace('-Search', '')
        target_file_path = os.path.join(col_folder, f'{target_filename_prefix}-SearchResult.xls')

        if os.path.exists(target_file_path):
            if filecmp.cmp(original_file_path, target_file_path):
                print('Already existed:', _)
                print(os.path.basename(target_file_path))
                continue

        print(f'Copying {original_file_path}')
        print(f'To {target_file_path}')
        shutil.copyfile(original_file_path, target_file_path)

        shutil.copyfile(
            os.path.join(curr_result_folder, f'AnalysisLog.txt'),
            os.path.join(col_folder, f'{target_filename_prefix}-AnalysisLog.txt')
        )

        shutil.copyfile(
            os.path.join(curr_result_folder, f'ExperimentSetupOverview_BGS Factory Settings.txt'),
            os.path.join(col_folder, f'{target_filename_prefix}-ExpSetup.txt')
        )

        shutil.copyfile(
            os.path.join(curr_result_folder, f'ConditionSetup.tsv'),
            os.path.join(col_folder, f'{target_filename_prefix}-ConditionSetup.txt')
        )

        shutil.copyfile(
            os.path.join(curr_result_folder, f'Candidates.tsv'),
            os.path.join(col_folder, f'{target_filename_prefix}-Candidates.txt')
        )

    except FileNotFoundError:
        print(f'File not found')
        pass

print('Done')
