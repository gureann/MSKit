import os


walking_dir = r'.'

kept = []
kept_startswith = []
kept_endswith = []
kept_re = []

excluded = []
excluded_startswith = []
excluded_endswith = []
excluded_re = []

file_size_upper_limit = 50e3
file_size_lower_limit = None


for root, dirs, files in os.walk(walking_dir):
    for file in files:
        file_path = os.path.join(root, file)
        if os.path.getsize(file_path) > file_size_upper_limit:
            if root == '.':
                excluded.append(file)
            else:
                excluded.append(file_path.replace(os.sep, '/').lstrip(r'./'))

# print(exclude_file_list)
with open(os.path.join(walking_dir, '.gitignore'), 'w') as f:
    for row in excluded:
        f.write(row + '\n')
